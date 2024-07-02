from django.urls import  path
from django.contrib.auth.views import LoginView,LogoutView
from . import views

urlpatterns = [
    path('registeruser/', views.registeruser,name="registeruser"),
    path('registervendor/', views.registervendor,name="registervendor"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('myaccount/', views.myaccount,name="myaccount"),
    path('vendordashboard/', views.vendordashboard,name="vendordashboard"),
    path('custdashboard/', views.custdashboard,name="custdashboard"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forget_password/", views.forgetpassword, name="forget_password"),
    path("reset_password_validate/<uidb64>/<token>", views.reset_password_validate, name="reset_password_validate"),
    path("reset_password", views.reset_password, name="reset_password"),
    # path('login/', views.login,name="login"),
    # path('logout/', views.logout,name="logout"),
] 