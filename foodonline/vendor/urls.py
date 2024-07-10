from django.urls import  path, include
from . import views
from verification import views as verificationview
urlpatterns = [
    path('', verificationview.vendordashboard, name="vdashboard"),
    path('profile/', views.vprofile,name="vprofile"),
    path('menu-builder/', views.menu_builder,name="menu_builder"),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category,name="fooditems_by_category"),
    # category CRUD operations 
    path('menu-builder/category/add/', views.add_category,name="add_category"),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category,name="edit_category"),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category,name="delete_category"),
    
    # fooditems CRUD operations 
    path('menu-builder/fooditems/add/', views.add_fooditems,name="add_fooditems"),
    path('menu-builder/fooditems/edit/<int:pk>/', views.edit_fooditems,name="edit_fooditems"),
    path('menu-builder/fooditems/delete/<int:pk>/', views.delete_fooditems,name="delete_fooditems"),
] 