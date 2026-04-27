from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout-confirm/', views.logout_confirm, name='logout_confirm'),
    path('logout/', views.logout_view, name='logout'),
    path('view-listings/', views.view_listings, name='view_listings'),
    path('edit-listing/<int:pk>/', views.edit_listing, name='edit_listing'),
    path('add-listing/', views.add_listing, name='add_listing'),
    path('manage-omaha/', views.manage_omaha, name='manage_omaha'),
    path('delete-omaha/<int:resource_id>/', views.delete_omaha_resource, name='delete_omaha_resource'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('omaha/', views.omaha_page, name='omaha_page'),
    path('listings/', views.listings_page, name='listings_page'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)