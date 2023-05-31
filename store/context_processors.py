from cart.models import Cart,Cart_Items
from cart.views import _cart_id

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    
    else:
        try:
            if request.user.is_authenticated:
                cartItem = Cart_Items.objects.all().filter(user=request.user)
            else:
                cart = Cart.objects.filter(cart_id=_cart_id(request))
                cartItem = Cart_Items.objects.all().filter(cart=cart[:1])

            for cartitem in cartItem:
                item_count += cartitem.quantity

        except Cart.DoesNotExist:
            item_count = 0
        return dict(item_count=item_count)
