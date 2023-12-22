from django import forms
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        labels = {
            'username': '',  # Define rótulo como vazio para o campo username
            'password1': '',  # Define rótulo como vazio para o campo password1
            'password2': '',  # Define rótulo como vazio para o campo password2
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Digite um email valido')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']