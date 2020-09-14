from django import forms
from .models import UserExtend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserExtendForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = UserExtend
        fields = ['mobileno', 'age', 'qualification', 'gender']