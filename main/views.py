from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage
from .forms import PropertyForm


def home(request):
    return render(request, 'home.html')


def admin_login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('view_listings')
        else:
            error_message = 'Invalid username or password. Please try again.'

    return render(request, 'admin_login.html', {'error_message': error_message})


@login_required
def logout_confirm(request):
    return render(request, 'logout_confirm.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('admin_login')
    return redirect('logout_confirm')


@login_required
def view_listings(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'view_listings.html', {'properties': properties})


@login_required
def edit_listing(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            
            # Handle additional photo uploads
            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(property=property_obj, image=image)
                
            return redirect('view_listings')
    else:
        form = PropertyForm(instance=property_obj)
    
    return render(request, 'edit_listing.html', {
        'form': form,
        'property': property_obj,
    })


@login_required
def add_listing(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save()
            
            # Handle photo uploads
            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(property=property_obj, image=image)
                
            return redirect('view_listings')
    else:
        form = PropertyForm()
        
    return render(request, 'add_listing.html', {'form': form})