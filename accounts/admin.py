from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','last_login','date_joined','is_active')
    list_display_links = ('username','email',)
    readonly_fields = ('last_login','date_joined')
    # ordering = ('-date_joined')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account,AccountAdmin)
