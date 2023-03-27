from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ["date_joined"]
    

admin.site.register(User, UserAdmin)

