from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
def myaccount_redirect_url(request):
    if request.user.role == 1:
        redirecturl= 'vendordashboard'
    elif request.user.role == 2:
        redirecturl= 'custdashboard'
    elif request.user.role is None and request.user.is_superuser:
        redirecturl = '/admin'
    return redirecturl 


def send_verification_email(request,user,  mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    # mail_subject = 'please activaye your account'
    
    message = render_to_string(email_template , {
        'user' : user,
        'domain': current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
        
    })
    to_email = user.email
    mail = EmailMessage(mail_subject,message,from_email, to=[to_email])
    mail.send()
    
def send_is_approval_email(mail_subject, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    # current_site = get_current_site(request)
    # mail_subject = 'please activaye your account'
    
    message = render_to_string( 'accounts/emails/account_is_approval_email.html', context)
    #                            {
    #     'user' : user,
    #     'domain': current_site,
    #     'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
    #     'token' : default_token_generator.make_token(user),
        
    # }
   
    to_email = context['user'].email
    mail = EmailMessage(mail_subject,message,from_email, to=[to_email])
    mail.send()