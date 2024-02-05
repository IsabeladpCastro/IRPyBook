from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Livro



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        labels = {
            'username': '',
            'password1': '',
            'password2': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Digite seu nome de usuário'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Digite novamente sua senha'}),
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
        
class AdicionarLivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'sinopse']        