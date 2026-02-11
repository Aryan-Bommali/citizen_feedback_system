from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'issue_type',
            'severity',
            'location',
            'landmark',
            'city',
            'pincode',
            'description',
            'image',
        ]
        widgets = {
            'issue_type': forms.Select(attrs={'class': 'form-select',}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter road or area name'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nearby landmark'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city or town'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter area pincode'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue in detail'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
