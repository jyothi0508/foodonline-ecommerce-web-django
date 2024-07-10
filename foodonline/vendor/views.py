from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from verification.views import check_role_vendor
from verification.forms import *
from .forms import * 
from verification.models import * 
from .models import * 
from menu.models import *
from django.contrib.auth.decorators import login_required,  user_passes_test
from menu.forms import *
from django.template.defaultfilters import slugify
# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor
@login_required
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user= request.user)
    vendor = get_object_or_404(Vendor, user= request.user)
    
    if request.method == 'POST':
        userprofile_form = UserProfileForm(request.POST,request.FILES, instance = profile)
        verder_form = VendorForm(request.POST,request.FILES, instance = vendor)
        if userprofile_form.is_valid() and verder_form.is_valid():
            userprofile_form.save()
            verder_form.save()
            messages.success(request, 'Restuarent details updated successfully.')
            return redirect('vprofile')
        else:
            print(userprofile_form.errors)
            print(verder_form.errors)
    else:
        userprofile_form  = UserProfileForm(instance = profile)
        verder_form = VendorForm(instance = vendor)
    context = {
        'userprofile_form': userprofile_form,
        'verder_form': verder_form,
        'profile': profile,
        'vendor': vendor
    }
    return render(request, 'vendor/vprofile.html', context)
@login_required
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    category = Category.objects.filter(vendor= vendor).order_by('-created_at')
    context = {
        'categories': category
    }
    return render(request, 'vendor/menu_builder.html', context)
@login_required
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = Fooditem.objects.filter(vendor= vendor, category=category).order_by('-created_at')
    # print(fooditems)
    context = {
        'fooditems': fooditems,
        'category' : category
    }
    return render(request, 'vendor/fooditems_by_category.html' , context)
@login_required
@user_passes_test(check_role_vendor)
def add_category(request):
    vendor = get_vendor(request)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, 'Category added successfully')
            return redirect('menu_builder')
    else :
        form = CategoryForm()
    context = {
        'vendor': vendor,
        'form' : form
    }
    return render(request, 'vendor/add_category.html',context)
@login_required
@user_passes_test(check_role_vendor)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk =pk)
    vendor = get_vendor(request)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance = category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, 'Category updated successfully')
            return redirect('menu_builder')
    else :
        form = CategoryForm(instance = category)
    context = {
        'vendor': vendor,
        'form' : form,
        'category' : category
    }
    return render(request, 'vendor/edit_category.html',context)
@login_required
@user_passes_test(check_role_vendor)
def delete_category(request, pk):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully')
    return redirect('menu_builder')
@login_required
@user_passes_test(check_role_vendor)
def add_fooditems(request):
    vendor = get_vendor(request)
    if request.method == "POST":
        form = FoodItemsForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            fooditem = form.save(commit=False)
            fooditem.vendor = vendor
            fooditem.slug = slugify(food_title)
            fooditem.save()
            messages.success(request,'Food item added successfully')
            return redirect('fooditems_by_category', fooditem.category.id)
    else :
        form = FoodItemsForm()
        form.fields['category'].queryset = Category.objects.filter(vendor = vendor)
        
    context = {
        'vendor': vendor,
        'form' : form,
        # 'category' : category
    }
    return render(request, 'vendor/add_fooditems.html',context)
@login_required
@user_passes_test(check_role_vendor)
def edit_fooditems(request, pk):
    fooditem = get_object_or_404(Fooditem, pk =pk)
    vendor = get_vendor(request)
    if request.method == "POST":
        form = FoodItemsForm(request.POST, request.FILES, instance= fooditem)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            fooditem = form.save(commit=False)
            fooditem.vendor = vendor
            fooditem.slug = slugify(food_title)
            fooditem.save()
            messages.success(request,'Food item Updated successfully')
            return redirect('fooditems_by_category', fooditem.category.id)
    else :
        form = FoodItemsForm(instance= fooditem)
        form.fields['category'].queryset = Category.objects.filter(vendor = vendor)
    context = {
        'vendor': vendor,
        'form' : form,
        'fooditem' : fooditem
    }
    return render(request, 'vendor/edit_fooditems.html',context)
@login_required
@user_passes_test(check_role_vendor)
def delete_fooditems(request, pk):
    vendor = get_vendor(request)
    fooditem = get_object_or_404(Fooditem, pk =pk)
    fooditem.delete()
    messages.success(request, 'Fooditem has been deleted successfully')
    return redirect('fooditems_by_category', fooditem.category.id)