from django import forms
from .models import Profile, SMScode
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    image = forms.ImageField()
    bio = forms.CharField(widget=forms.Textarea)
    age = forms.IntegerField(max_value=100)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают!")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Такой Логин уже занят, выберите другой")
        return cleaned_data


class SMScodeForm(forms.Form):
    SMS = forms.CharField(max_length=4)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
