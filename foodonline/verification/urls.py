from django.urls import  path
# from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('registeruser/', views.registeruser,name="registeruser"),
    path('registervendor/', views.registervendor,name="registervendor"),
    # path('login/', views.login,name="login"),
    # path('logout/', views.logout,name="logout"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('myaccount/', views.myaccount,name="myaccount"),
    path('vendordashboard/', views.vendordashboard,name="vendordashboard"),
    path('custdashboard/', views.custdashboard,name="custdashboard"),
    # path("login/", LoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name="rest_logout"),
] 