from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'address', 'home_type', 'city', 'state', 'neighborhood', 
            'zip_code', 'price', 'status', 'visibility', 'description', 
            'bedrooms', 'bathrooms', 'garage', 'year_built'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter property description here ...'}),
            'visibility': forms.Select(choices=[(True, 'Visible'), (False, 'Hidden')]),
        }
