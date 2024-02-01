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

class LivroAdicionado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    
    

class AtividadeUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_atividade = models.CharField(max_length=255)  # Pode ser 'registro_livro', 'exclusao_livro', etc.
    livro_relacionado = models.ForeignKey(Livro, null=True, blank=True, on_delete=models.CASCADE)
    data_atividade = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo_atividade} - {self.data_atividade}'