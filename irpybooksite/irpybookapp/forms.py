from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Livro



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        labels = {
            'username': '',  # Define rótulo como vazio para o campo username
            'password1': '',  # Define rótulo como vazio para o campo password1
            'password2': '',  # Define rótulo como vazio para o campo password2
        }
class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'titulo',
            'autor',
            'data',
            'sinopse',
    ]