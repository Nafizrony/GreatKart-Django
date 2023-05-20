from django.shortcuts import render,get_object_or_404
from .models import Store
from category.models import Category

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug is not None:
        categories = Category.objects.get(slug=category_slug)
        products = Store.objects.filter(category=categories,is_available=True)
        prodcut_count = products.count()
    else:
        products = Store.objects.all().filter(is_available=True)
        prodcut_count = products.count()
    context = {'products':products,'product_count':prodcut_count}
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        product = Store.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context = {'product':product}
    return render(request,'store/product_details.html',context)


