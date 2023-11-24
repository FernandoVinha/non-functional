from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
import uuid

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model =  User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class TokenRegistrationForm(forms.Form):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")

        validate_password(password2)
        return password2
    
class  LoginForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", required=True)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, required=True)

class TokenAndPasswordLoginForm(forms.Form):
    token = forms.CharField(label="Token", required=True)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, required=True)

    def clean_token(self):
        token = self.cleaned_data.get('token')
        try:
            uuid.UUID(token)
        except ValueError:
            raise forms.ValidationError("Formato de token inválido.")
        return token