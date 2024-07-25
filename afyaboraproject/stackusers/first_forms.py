from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    accept_terms = forms.BooleanField(required=True, label="I accept the Terms and Conditions and Privacy Policy")
    email = forms.EmailField()  # Use forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  # Use forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)  # Use forms.EmailField()

    class Meta:
        model = Profile  # Use model, not models
        fields = ['bio', 'email', 'image']

