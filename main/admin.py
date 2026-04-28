from django.contrib import admin
from .models import Property, PropertyImage, OmahaResource, AgentProfile

admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(OmahaResource)
admin.site.register(AgentProfile)