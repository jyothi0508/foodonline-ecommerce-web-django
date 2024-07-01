from django.http import HttpResponse
from django.shortcuts import redirect, render

from verification.utils import myaccount_redirect_url, send_verification_email
from .models import *
from .forms import *
from vendor.forms import *
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

def check_role_vendor(user):
    if user.role == 1:
        return True
    else :
        raise PermissionDenied

def check_role_cust(user):
    if user.role == 2:
        return True
    else :
        raise PermissionDenied
    
# Create your views here.
def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already Registered.')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # using the form  data
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = NewUser.CUSTOMER
            # user.save()
            
            # using the create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = NewUser.objects.create_user(first_name = first_name, last_name = last_name, username= username, email= email, password= password)
            user.role = NewUser.CUSTOMER
            user.save()
            # send verification email 
            send_verification_email(request,user)
            messages.success(request, 'your account was registered successfully')
            return redirect('registeruser')
        else:
            print(form.errors)
    else:
        form = RegisterUserForm()
    context = { "form" : form}
    return render(request, 'accounts/registeruser.html', context)
@login_required
def myaccount(request):
    redirectpath = myaccount_redirect_url(request)
    return redirect(redirectpath)
def registervendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already Registered.')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = RegisterUserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid() :
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = NewUser.objects.create_user(first_name = first_name, last_name = last_name, username= username, email= email, password= password)
            user.role = NewUser.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user = user)
            vendor.user_profile = user_profile
            vendor.save() 
            messages.success(request, 'your account has been registered successfully! please wait for the approval.')
            return redirect('registervendor')
        else :
            print(form.errors)
    else :
        form = RegisterUserForm()
        v_form = VendorForm()
    context = {
        'form' : form,
        'v_form' : v_form
    }
    return render(request, 'accounts/registervendor.html', context)

# def login(request):
#     if request.user.is_authenticated:
#         messages.warning(request, 'you are already logged in.')
#         return redirect('dashboard')
#     elif request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = auth.authenticate(email=email,password=password)
#         if user is not None:
#             auth.login(request,user)
#             # messages.success(request, 'your are now logged in.')
#             print(user.role)
#             redirectpath = myaccount_redirect_url(user)
#             return redirect(redirectpath)
#         else:
#             messages.error(request, 'Invalid credentitals.')
#             return redirect('login')
#     return render(request, 'accounts/login.html')
# def logout(request):
#     auth.logout(request)
#     messages.info(request, 'you are logged out.')
#     return redirect('login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render(request, 'accounts/vendordashboard.html')
@login_required(login_url='login')
@user_passes_test(check_role_cust)
def custdashboard(request):
    return render(request, 'accounts/custdashboard.html')



# twilio recovery code ----->      82D15S7ZY1ZPUW6NE34KZN9D