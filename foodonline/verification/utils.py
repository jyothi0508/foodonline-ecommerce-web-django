def myaccount_redirect_url(request):
    if request.user.role == 1:
        redirecturl= 'vendordashboard'
    elif request.user.role == 2:
        redirecturl= 'custdashboard'
    elif request.user.role is None and request.user.is_superuser:
        redirecturl = '/admin'
    return redirecturl 


def send_verification_email(request,user):
    pass