from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.IntegerField()
    class Meta:
        model = User
        fields = ('username','email','phone_number','password1', 'password2')