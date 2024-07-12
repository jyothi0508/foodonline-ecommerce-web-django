from django.contrib import admin
from .models import cart
# Register your models here.

class cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'modified_at')
    
admin.site.register(cart, cartAdmin)