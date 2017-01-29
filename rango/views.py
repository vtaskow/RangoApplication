from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


# Create your views here.

def index(request):
    # query the db for most liked categories and most viewed pages
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    # construct context dict
    context_dict = {'categories': category_list, 'pages': pages_list}

    return render(request, 'rango/index.html', context=context_dict)


def show_category(request, category_name_slug):
    # create context dict to be passed to template later
    context_dict = {}

    # find category based on slug param and obtain pages assoc with it
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        # add them to context_dict
        context_dict['pages'] = pages
        context_dict['category'] = category
    # mark them as empty
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    # render the response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)


def about(request):
    context_dict = {'author': "Viktor Taskov"}
    return render(request, 'rango/about.html', context=context_dict)


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


def register(request):
    # A boolean to tell if the reg-n has been successful
    registered = False

    if request.method == 'POST':  # if a form has been submitted
        # Grab info from the submitted form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to db
            user = user_form.save()
            # hash user's password
            user.set_password(user.password)
            user.save()

            # manually save additional info from the form
            profile = profile_form.save(commit=False)
            # link it with this user instance
            profile.user = user

            if 'picture' in request.FILES:  # if picture was provided
                profile.picture = request.FILES['picture']

            profile.save()

            # mark the registration as successful
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # not a post request, so display blank forms
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render it using the context
    return render(request, 'rango/register.html', {'user_form': user_form,
                                                   'profile_form': profile_form, 'registered': registered})
