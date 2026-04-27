from django import forms
from .models import Property, PropertyImage, AgentProfile

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'address', 'home_type', 'city', 'state', 'neighborhood', 
            'zip_code', 'price', 'status', 'visibility', 'description', 
            'bedrooms', 'bathrooms', 'garage', 'year_built', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter property description here ...'}),
            'visibility': forms.Select(choices=[(True, 'Visible'), (False, 'Hidden')]),
        }

from .models import AgentProfile

class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = ['name', 'office_address', 'phone', 'website', 'email', 'biography', 'portrait']