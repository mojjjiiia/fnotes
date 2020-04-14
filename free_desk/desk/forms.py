from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewPostForm(forms.Form):
    theme = forms.CharField(max_length=60)
    text = forms.CharField(max_length=255, widget=forms.Textarea)


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email"]


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
