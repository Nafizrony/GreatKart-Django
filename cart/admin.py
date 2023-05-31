from django.contrib import admin
from .models import Cart,Cart_Items
#  Register your models here.
class AdminCart(admin.ModelAdmin):
    list_display = ('cart_id','created')
    readonly_fields = ('cart_id',)
#     # list_editable = False

class AdminCartItem(admin.ModelAdmin):
     list_display = ('product','cart','quantity','is_active')
admin.site.register(Cart)
admin.site.register(Cart_Items)