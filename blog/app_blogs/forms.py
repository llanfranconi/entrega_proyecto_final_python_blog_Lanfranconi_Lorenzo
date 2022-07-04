from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Usuario_formulario(UserCreationForm):
    username = forms.CharField(label = 'Nombre de Usuario')
    email = forms.EmailField(label = 'Ingrese su dirección de correo')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repita la contraseña', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class Avatar_formulario(forms.Form):
    imagen = forms.ImageField(required=True)

class Email_formulario(forms.Form):
    email = forms.EmailField(required=True)

class Blog_formulario(forms.Form):
    titulo = forms.CharField(max_length=100, label="Título", required=True)
    subtitulo = forms.CharField(max_length=100, label="Subtitulo", required=True)
    cuerpo =  forms.CharField(max_length=2000, label="Contenido de tu blog", required=True, widget=forms.Textarea)
    imagen = forms.ImageField(label= "Imagen de tu blog", required=True)

class Blog_formulario_editar_texto(forms.Form):
    titulo = forms.CharField(max_length=100, label="Título", required=True)
    subtitulo = forms.CharField(max_length=100, label="Subtitulo", required=True)
    cuerpo =  forms.CharField(max_length=2000, label="Contenido de tu blog", required=True, widget=forms.Textarea)

class Blog_formulario_editar_imagen(forms.Form):
    imagen = forms.ImageField(label= "Imagen de tu blog", required=True)

class Comentario_formulario(forms.Form):
    cuerpo = forms.CharField(max_length=2000, label="Comentario", required=True, widget=forms.Textarea)