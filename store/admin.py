from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.
class StoreAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html(f'<img src="{object.product_images.url}" width="70" style="border-radius:50%;border:1px solid #cee" >')
    list_display = ('product_name','slug','thumbnail','price','stock','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    list_editable = ('is_available',)
admin.site.register(Store,StoreAdmin)
