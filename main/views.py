from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage, OmahaResource, AgentProfile
from .forms import PropertyForm, AgentProfileForm


def home(request):
    return render(request, 'home.html')

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'property_detail.html', {'property': property_obj})


def admin_login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
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
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)

        if form.is_valid():
            property_obj = form.save(commit=False)

            # ✅ Ensure ONLY ONE featured property
            if property_obj.is_featured:
                Property.objects.filter(is_featured=True).exclude(pk=property_obj.pk).update(is_featured=False)

            property_obj.save()

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

            images = request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(property=property_obj, image=image)

            return redirect('view_listings')
    else:
        form = PropertyForm()

    return render(request, 'add_listing.html', {'form': form})


@login_required
def manage_omaha(request):
    if request.method == "POST":
        category = request.POST.get("category")
        title = request.POST.get("title")
        link = request.POST.get("link")
        description = request.POST.get("description")

        if not category or not title or not link:
            messages.error(request, "Please complete all required fields.")
        else:
            OmahaResource.objects.create(
                category=category,
                title=title,
                link=link,
                description=description
            )
            messages.success(request, "Omaha resource saved successfully.")
            return redirect('manage_omaha')

    resources = OmahaResource.objects.all().order_by('category', 'title')
    return render(request, "manage_omaha.html", {"resources": resources})


@login_required
def delete_omaha_resource(request, resource_id):
    resource = get_object_or_404(OmahaResource, id=resource_id)
    resource.delete()
    messages.success(request, "Resource removed successfully.")
    return redirect("manage_omaha")

@login_required
def admin_dashboard(request):
    profile, created = AgentProfile.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Carlos Kosala',
            'office_address': 'CK Real Estate\n10671 Eden Park Street, Room 101\nOmaha, NE 68114',
            'phone': '(402) 558-6210',
            'website': 'https://www.ckrealestate.com',
            'email': 'info.carlos@ckrealestate.com',
            'biography': 'Carlos Kosala is a real estate professional serving the Omaha area.',
        }
    )

    return render(request, 'admin_dashboard.html', {'profile': profile})

@login_required
def update_profile(request):
    profile, created = AgentProfile.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = AgentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AgentProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form, 'profile': profile})

def omaha_page(request):
    resources = OmahaResource.objects.all().order_by('category')
    return render(request, 'omaha.html', {'resources': resources})

def listings_page(request):
    properties = Property.objects.filter(
        visibility=True,
        status='Active'
    ).order_by('-created_at')

    return render(request, 'listings.html', {'properties': properties})

def home(request):
    featured_property = Property.objects.filter(
        is_featured=True,
        visibility=True,
        status='Active'
    ).first()

    return render(request, 'home.html', {
        'featured_property': featured_property
    })