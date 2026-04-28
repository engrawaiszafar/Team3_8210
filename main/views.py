from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Property, PropertyImage, OmahaResource, AgentProfile, SearchLog
from .forms import PropertyForm, AgentProfileForm, ContactForm


def home(request):
    return render(request, 'home.html')

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    success_message = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send Email to Carlos
            subject = f"Inquiry for Property: {property_obj.address}"
            email_message = f"""
            Hello Carlos,

            You have received a new inquiry regarding the property at {property_obj.address}.

            Visitor Details:
            - Name: {name}
            - Email: {email}

            Message:
            {message}

            Property Reference:
            - Link: http://127.0.0.1:8000/property/{property_obj.pk}/
            """
            
            send_mail(
                subject,
                email_message,
                email, # From visitor
                ['info.carlos@ckrealestate.com'], # To Carlos
                fail_silently=False,
            )
            success_message = "Your inquiry has been sent successfully! Carlos will get in touch with you shortly."
            form = ContactForm() # Reset form
    else:
        form = ContactForm()

    return render(request, 'property_detail.html', {
        'property': property_obj,
        'form': form,
        'success_message': success_message
    })


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
    properties = Property.objects.filter(visibility=True, status='Active')
    
    home_type = request.GET.get('home_type', '').strip()
    neighborhood = request.GET.get('neighborhood', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    # Log non-empty search trigger
    if home_type or neighborhood or min_price or max_price:
        SearchLog.objects.create(
            home_type=home_type if home_type else None,
            neighborhood=neighborhood if neighborhood else None,
            min_price=min_price if min_price else None,
            max_price=max_price if max_price else None
        )

    if home_type:
        properties = properties.filter(home_type__iexact=home_type)
    if neighborhood:
        properties = properties.filter(neighborhood__icontains=neighborhood)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    properties = properties.order_by('-created_at')

    # Get unique choices for the dropdown dynamically based on active listings
    available_home_types = Property.objects.filter(visibility=True, status='Active').values_list('home_type', flat=True).distinct()

    return render(request, 'listings.html', {
        'properties': properties,
        'available_home_types': available_home_types,
        'filters': {
            'home_type': home_type,
            'neighborhood': neighborhood,
            'min_price': min_price,
            'max_price': max_price
        }
    })

def seed_dummy_properties(request):
    from .models import Property
    import random

    home_types = ['House', 'Condo', 'Townhouse', 'Land', 'Ranch', 'Cottage', 'Villa']
    cities = ['Omaha', 'Lincoln', 'Bellevue', 'Council Bluffs']
    neighborhoods = ['Dundee', 'Aksarben', 'Benson', 'Elkhorn', 'Downtown', 'South O']
    states = ['NE', 'IA']
    
    addresses = [
        "1045 N 45th St", "2211 Farnam St", "909 S 72nd St", "1844 Dodge St",
        "5505 Center St", "3201 Pacific St", "7707 L St", "1212 N 90th St",
        "6606 Maple St", "4040 Ames Ave", "3030 Fort St", "1515 Cuming St",
        "8808 West Dodge Rd", "5050 Grover St", "2020 Vinton St"
    ]

    created_count = 0
    for i in range(15):
        addr = addresses[i] if i < len(addresses) else f"{1000 + i} Random St"
        Property.objects.create(
            address=addr,
            home_type=random.choice(home_types),
            city=random.choice(cities),
            state=random.choice(states),
            neighborhood=random.choice(neighborhoods),
            zip_code=str(random.randint(68000, 68500)),
            price=random.randint(150, 850) * 1000,
            status='Active',
            visibility=True,
            bedrooms=random.randint(1, 6),
            bathrooms=random.randint(1, 4),
            garage=random.randint(0, 3),
            year_built=random.randint(1950, 2024),
            description="A beautiful home that has just been listed. Features modern finishes, spacious living areas, and is situated in a great location with access to top-rated amenities."
        )
        created_count += 1

    return HttpResponse(f"Successfully added {created_count} dummy properties! Feel free to visit the listings page.")

def home(request):
    featured_property = Property.objects.filter(
        is_featured=True,
        visibility=True,
        status='Active'
    ).first()

    return render(request, 'home.html', {
        'featured_property': featured_property
    })

def agent_profile(request):
    profile = AgentProfile.objects.first()
    if not profile:
        profile = AgentProfile.objects.create(
            name='Carlos Kosala',
            office_address='CK Real Estate\n10671 Eden Park Street, Room 101\nOmaha, NE 68114',
            phone='(402) 558-6210',
            website='https://www.ckrealestate.com',
            email='info.carlos@ckrealestate.com',
            biography='Carlos Kosala is a real estate professional serving the Omaha area.',
        )
        
    success_message = None
    error_message = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                subject = f"General Inquiry from {name}"
                email_body = f"Visitor Details:\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"
                
                send_mail(
                    subject,
                    email_body,
                    email,
                    [profile.email],
                    fail_silently=False,
                )
                success_message = "Your inquiry has been sent successfully!"
                form = ContactForm() 
            except Exception:
                error_message = "Oops! The email could not be sent. Please try again later."
    else:
        form = ContactForm()

    return render(request, 'agent_profile.html', {
        'profile': profile,
        'form': form,
        'success_message': success_message,
        'error_message': error_message
    })