from django.urls import path 
from . import views

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),  
    path('',views.cart,name='cart'),
    path('add_cart/<str:product_id>/',views.add_to_cart,name='add_cart'), 
    path('remove_cart/<str:product_id>/<str:cart_id>/',views.remove_cart,name='remove_cart'),  
    path('remove_cart_item/<str:product_id>/<str:cart_id>/',views.remove_cart_item,name='remove_cart_item'),  
]
