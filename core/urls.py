from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout-confirm/', views.logout_confirm, name='logout_confirm'),
    path('logout/', views.logout_view, name='logout'),
    path('view-listings/', views.view_listings, name='view_listings'),
    path('edit-property/', views.edit_property, name='edit_property'),
]