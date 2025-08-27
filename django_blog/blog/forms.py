# blog/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = []  # We'll handle profile separately

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']