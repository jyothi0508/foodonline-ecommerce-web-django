from django.http import HttpResponse
from django.shortcuts import redirect, render

from verification.utils import myaccount_redirect_url, send_verification_email
from .models import *
from .forms import *
from vendor.forms import *
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import *
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
            mail_subject = 'please activaye your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, mail_subject, email_template)
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
            # send verification email 
            mail_subject = 'please activaye your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, mail_subject, email_template)
            messages.success(request, 'your account has been registered successfully! Activation link sent to your registered mail.')
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

def activate(request, uidb64,token ):
    #  activate the user by setting the is_active status true
    try:
        user = None
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = NewUser._default_manager.get(pk=uid)
    except(user.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! your account is activated.')
        return redirect('myaccount')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('myaccount')
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
@login_required
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render(request, 'accounts/vendordashboard.html')
@login_required
@user_passes_test(check_role_cust)
def custdashboard(request):
    return render(request, 'accounts/custdashboard.html')

def forgetpassword(request):
    # print(0)
    if request.method == 'POST':
        # print(1)
        email = request.POST['email']
        try:
            user = NewUser.objects.get(email = email)
            if user:
                # user = user.objects.get(email=email)
                # print(user.email)
                mail_subject = 'Reset password link'
                email_template = 'accounts/emails/reset_verification_email.html'
                send_verification_email(request,user, mail_subject, email_template)
                messages.success(request, 'Password rest link has been sent to your email address.')
                return redirect('login')
            else:
                messages.error(request, 'user does not exist')
                return redirect('forget_password') 
        except  NewUser.DoesNotExist:
            messages.error(request, 'user does not exist')
            return redirect('forget_password')
    elif request.method == 'GET':
        return render(request, 'accounts/forgot_password.html')
def reset_password_validate(request, uidb64, token):
    try:
        user = None
        uid = urlsafe_base64_decode(uidb64).decode()
        # print(uid)
        user = NewUser._default_manager.get(pk=uid)
    except(user.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, 'you can reset your password')
        return redirect('reset_password') 
    else :
        messages.error(request, 'This link has been expired!')
        return redirect('myaccount')
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = NewUser.objects.get(pk = uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfull.')
            return redirect('login') 
        else:
            messages.error(request, 'password do not match')
            return redirect('reset_password') 
    return render(request, 'accounts/reset_password.html')

# twilio recovery code ----->      82D15S7ZY1ZPUW6NE34KZN9D