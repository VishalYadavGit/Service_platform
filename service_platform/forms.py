from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
        label="Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password"}),
        label="Confirm Password",
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise ValidationError("Username must contain at least 6 letters.")
        if username.startswith('@') or username[0].isdigit():
            raise ValidationError("Username cannot start with '@' or a number.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or len(password) > 16:
            raise ValidationError("Password contain a combination of at least 8 characters.")
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            raise ValidationError("Password must be alphanumeric.")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("Please enter a valid Gmail address.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use. Please use a different email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )
