from django.urls import path 
from . import views

urlpatterns = [
    path('store/',views.store,name='store'),
    path('store/<slug:category_slug>/',views.store,name='product_by_category'),
    path('store/<slug:category_slug>/<slug:product_slug>/',views.product_details,name='product_details'),
]
