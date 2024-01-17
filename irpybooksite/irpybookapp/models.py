from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    data = models.DateField(default=datetime.now)
    sinopse = models.TextField()
    
    
    
    
class RegistroLivro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    favorito = models.BooleanField(default=False)    