from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from menu.models import *
from vendor.models import *
from django.db.models import Prefetch
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved= True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count' : vendor_count
    }
    return render(request, 'marketplace/listings.html', context)
def vendordetail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug = vendor_slug)
    categories = Category.objects.filter(vendor = vendor).prefetch_related(
        Prefetch(
           'fooditems',
           queryset=  Fooditem.objects.filter(is_available=True)
        )
    )
    context = {
        'vendor' : vendor,
        'vendor_slug': vendor_slug,
        'categories' : categories,
    }
    return render(request, 'marketplace/vendordetail.html', context)
def add_to_cart(request, food_id):
    return HttpResponse('testing')