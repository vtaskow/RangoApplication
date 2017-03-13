from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhose_search import run_query


# Create your views here.


def index(request):
    # query the db for most liked categories and most viewed pages
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    # construct context dict
    context_dict = {'categories': category_list, 'pages': pages_list}

    # handle cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # obtain response obj to add cookies info
    response = render(request, 'rango/index.html', context=context_dict)

    return response


def search(request):
    result_list = []
    query = ""
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    return render(request, "rango/search.html", {'result_list': result_list, 'query': query})


def show_category(request, category_name_slug):
    # create context dict to be passed to template later
    context_dict = {}

    # find category based on slug param and obtain pages assoc with it
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')

        # update number of views of this category
        category.views += 1
        category.save()

        # add them to context_dict
        context_dict['pages'] = pages
        context_dict['category'] = category
    # mark them as empty
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    result_list = []
    context_dict['query'] = category.name  # default query
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list

    # render the response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)


def about(request):
    context_dict = {'author': "Viktor Taskov"}

    # handle cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # obtain response obj to add cookies info
    response = render(request, 'rango/about.html', context=context_dict)

    return response


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            # cat = form.save(commit=True)
            form.save(commit=True)
            # print(cat, cat.slug)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {"form": form, "category": category}
    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#     # A boolean to tell if the reg-n has been successful
#     registered = False
#
#     if request.method == 'POST':  # if a form has been submitted
#         # Grab info from the submitted form
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             # save the user's form data to db
#             user = user_form.save()
#             # hash user's password
#             user.set_password(user.password)
#             user.save()
#
#             # manually save additional info from the form
#             profile = profile_form.save(commit=False)
#             # link it with this user instance
#             profile.user = user
#
#             if 'picture' in request.FILES:  # if picture was provided
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             # mark the registration as successful
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         # not a post request, so display blank forms
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     # render it using the context
#     return render(request, 'rango/register.html', {'user_form': user_form,
#                                                    'profile_form': profile_form, 'registered': registered})
#
#
# def user_login(request):
#     # if Submit button was clicked
#     if request.method == 'POST':
#         # gather info provided by the user
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # check if valid credentials, obtain User object or None
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 # if user is valid and active, redirect to index
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             # could not authenticate user
#             # print("Invalid login details: {0}, {1}".format(username, password))
#             return render(request, 'rango/login.html', {'invalid': "Invalid login details supplied."})
#     else:
#         # not a POST request, display login form
#         return render(request, 'rango/login.html', {})


# decorator redirects to url that's been set up in settings.py
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))


def get_server_side_cookie(request, cookie, default_val=None):
    # request data about a cookie, return None if cookie does not exist
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    # 2017 - 02 - 05 01:19:01.768357
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    # 2017 - 02 - 04 23:50:28

    # if a day has elapsed, update visits
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    # create/update cookie
    request.session['visits'] = visits


def track_url(request):
    page_id = None
    url = '/rango/'

    # if this is a get request
    if request.method == 'GET':
        # if there we clicked on a page
        if 'page_id' in request.GET:
            # get it id of that page
            page_id = request.GET['page_id']

            # try to get this Page instance and update its views field, otherwise do nothing
            try:
                page = Page.objects.get(pk=page_id)
                page.views += 1
                page.save()
                # redirect the user to the page.url
                url = page.url
            except:
                pass
    return redirect(url)
