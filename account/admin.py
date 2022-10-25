from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



class UserAdmin(UserAdmin):
    readonly_fields = ["date_joined"]
    

admin.site.register(User, UserAdmin)

