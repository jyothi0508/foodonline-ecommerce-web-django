from django.http import HttpResponse
from django.shortcuts import render
from vendor.models import *
# Create your views here.
def home(request):
    vendors = Vendor.objects.filter(is_approved= True, user__is_active=True)[:8]
    context = {
        'vendors': vendors
    }
    return render(request,"home.html", context)