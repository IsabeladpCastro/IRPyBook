from django.db import models


class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    data = models.DateField()
    sinopse = models.TextField()