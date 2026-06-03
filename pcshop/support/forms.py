from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'rating', 'title', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-cyber text-white',
                'placeholder': 'Your name (or leave blank if logged in)',
                'required': False
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-cyber text-white',
                'placeholder': 'Your email (or leave blank if logged in)',
                'required': False
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control form-cyber text-white',
                'placeholder': 'Feedback title (e.g., Great quality, Fast shipping)',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form-cyber text-white',
                'placeholder': 'Tell us what you think about NOVA TECH...',
                'rows': 4,
                'required': True
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'rating': 'Rate Your Experience',
            'title': 'Feedback Title',
            'message': 'Your Feedback',
        }
