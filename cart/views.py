from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store.models import Store,Variation
from .models import Cart,Cart_Items
from django.contrib.auth.decorators import login_required
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request,product_id):
    product = Store.objects.get(id=product_id)
    product_variation = []
    current_user = request.user
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(product=product,variation_type__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    print(variation)
                except:
                    pass
        existing_cart_items = Cart_Items.objects.filter(user=current_user,product=product).exists()
        if existing_cart_items:
            cartitem = Cart_Items.objects.filter(product=product,user=current_user)
            ex_variation = []
            id = []
            for item in cartitem:
                existing_variation = item.item_variation.all()
                ex_variation.append(list(existing_variation))
                id.append(item.id)
            print(ex_variation)
            if product_variation in ex_variation:
                index = ex_variation.index(product_variation)
                item_id = id[index]
                item = Cart_Items.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()
            else:
                item = Cart_Items.objects.create(product=product,user=current_user,quantity=1)
                if len(product_variation) > 0:
                    item.item_variation.clear()
                    item.item_variation.add(*product_variation)
                item.save()
        else:
            cartitem = Cart_Items.objects.create(
                product = product,
                user=current_user,
                quantity = 1
            )
            if len(product_variation) > 0:
                cartitem.item_variation.clear()
                cartitem.item_variation.add(*product_variation)
            cartitem.save()
        # return HttpResponse(cartitem.quantity)
        return redirect('cart')
    else:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(product=product,variation_type__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    print(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        existing_cart_items = Cart_Items.objects.filter(cart=cart,product=product).exists()
        if existing_cart_items:
            cartitem = Cart_Items.objects.filter(product=product,cart=cart)
            ex_variation = []
            id = []
            for item in cartitem:
                existing_variation = item.item_variation.all()
                ex_variation.append(list(existing_variation))
                id.append(item.id)
            print(ex_variation)
            if product_variation in ex_variation:
                index = ex_variation.index(product_variation)
                item_id = id[index]
                item = Cart_Items.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()
            else:
                item = Cart_Items.objects.create(product=product,cart=cart,quantity=1)
                if len(product_variation) > 0:
                    item.item_variation.clear()
                    item.item_variation.add(*product_variation)
                item.save()
        else:
            cartitem = Cart_Items.objects.create(
                product = product,
                cart = cart,
                quantity = 1
            )
            if len(product_variation) > 0:
                cartitem.item_variation.clear()
                cartitem.item_variation.add(*product_variation)
            cartitem.save()
    # return HttpResponse(cartitem.quantity)
        return redirect('cart')
def cart(request,quantity=0,total=0,cart_items=0):
    tax = None
    grand_total = None
    try:
        if request.user.is_authenticated:
            cart_items = Cart_Items.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_Items.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += (cart_item.quantity)
        tax = (2*total)/100
        grand_total = (total+tax)
    except ObjectDoesNotExist:
        pass
    context = {'total':total,'quantity':quantity,'cart_items':cart_items,'tax':tax,'grand_total':grand_total}
    return render(request,'cart/cart.html',context)


def remove_cart(request, product_id,cart_id):
    product = get_object_or_404(Store, id=product_id)
    try:
        if request.user.is_authenticated:
            cartitem = Cart_Items.objects.get(product=product,user=request.user,id=cart_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cartitem = Cart_Items.objects.get(product=product,cart=cart,id=cart_id)
        if cartitem.quantity > 1:
            cartitem.quantity -= 1
            cartitem.save()
        else:
            cartitem.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request,product_id,cart_id):
    product = Store.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = Cart_Items.objects.get(user=request.user,product=product,id=cart_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cart_Items.objects.get(cart=cart,product=product,id=cart_id)
    
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def checkout(request,total=0,cart_items=0,quantity=0):
    tax = None
    grand_total = None
    cart = None
    try:
        if request.user.is_authenticated:
            cart_items = Cart_Items.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_Items.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += (cart_item.quantity)
        tax = (2*total)/100
        grand_total = (total+tax)
    except ObjectDoesNotExist:
        pass
    context = {'total':total,'quantity':quantity,'cart_items':cart_items,'tax':tax,'grand_total':grand_total}
    return render(request,'cart/checkout.html',context)



