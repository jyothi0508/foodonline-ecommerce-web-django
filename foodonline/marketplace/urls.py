from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.marketplace, name="marketplace"),
    path('<slug:vendor_slug>/', views.vendordetail, name="vendordetail"),
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name="add_to_cart"),
]