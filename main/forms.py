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

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Name',
        'required': True
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email',
        'required': True
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Ask a question or request information...',
        'rows': 4,
        'required': True
    }))