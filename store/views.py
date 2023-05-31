from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import Store
from cart.models import Cart,Cart_Items
from category.models import Category
from cart.views import _cart_id
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q


# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug is not None:
        categories = Category.objects.get(slug=category_slug)
        products = Store.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        products_page = paginator.get_page(page)
        prodcut_count = products.count()
    else:
        products = Store.objects.all().filter(is_available=True)
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        products_page = paginator.get_page(page)
        prodcut_count = products.count()
    context = {'products':products_page,'product_count':prodcut_count}
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    
    try:
        product = Store.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = Cart_Items.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e
    context = {'product':product,'in_cart':in_cart}
    return render(request,'store/product_details.html',context)

def search(request):
    keyword = request.GET.get('keyword') if request.GET.get('keyword') != None else ''
    products = Store.objects.filter(
        Q(product_name__icontains=keyword)|
        Q(description__icontains=keyword)

    )
    prodcut_count = products.count()
    context = {'products':products,'product_count':prodcut_count}
    return render(request,'store/store.html',context)

