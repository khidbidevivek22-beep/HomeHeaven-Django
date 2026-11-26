from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'phone', 'preferred_date', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Questions for the owner / manager', 'class': 'form-control', 'rows': 4}),
        }
