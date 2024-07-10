from django.contrib import admin

from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'modified_at')
    search_fields = ('category_name', 'vendor__vendor_name')
    
class FooditemAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('food_title',)}
    list_display = ('food_title','category', 'vendor','price', 'is_available', 'modified_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name','price')
    list_filter = ('is_available',)
    list_editable = ('is_available',)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Fooditem, FooditemAdmin)