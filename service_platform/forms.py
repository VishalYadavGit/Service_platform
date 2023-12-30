from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from .models import ContactMessage


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ["name", "email", "subject", "message"]


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


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )
