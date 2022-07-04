from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null = True, blank = True)



class Blog(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100)
    cuerpo = models.CharField(max_length=2000)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to = 'blogs', null = True, blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Titulo: {self.titulo} - Subtitulo: {self.subtitulo} - Autor: {self.user_id} - Fecha de post: {self.fecha} - Cuerpo: {self.cuerpo} "

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_blog = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    cuerpo = models.CharField(max_length=2000)