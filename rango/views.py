from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

# Create your views here.

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    #context_dict = {'boldmessage' : "Crunchy, creamy, cookie, candy, cupcake!"}
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
    context_dict = {'author' : "Viktor Taskov"}
    return render(request, 'rango/about.html', context=context_dict)
