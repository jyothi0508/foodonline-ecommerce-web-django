from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser,UserProfile

# Register your models here.

class customUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ('is_superuser','email')
    fieldsets = ()
    list_display = ('id','first_name','last_name','username','email','role','is_superuser','is_active')
admin.site.register(NewUser,customUserAdmin)
admin.site.register(UserProfile)