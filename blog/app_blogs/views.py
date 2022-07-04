from django.shortcuts import redirect, render, HttpResponse
from django.http.request import QueryDict
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app_blogs.forms import Usuario_formulario, Avatar_formulario, Email_formulario, Blog_formulario, Comentario_formulario, Blog_formulario_editar_texto, Blog_formulario_editar_imagen
from django.contrib import messages
from app_blogs.models import Avatar, Blog, Comentario



# Create your views here.


def inicio(request):
    
 #si el usuario no tiene un avatar, muestro el avatar default en el sitio, si no, muestro el del usuario

    avatar_usuario = ""

    if request.user.is_authenticated:
        usuario_actual = request.user.id
        avatares = Avatar.objects
        existe = False
        for avatar in avatares.all():
            if usuario_actual == avatar.user_id:
                existe = True
        if existe:
            avatar_usuario = avatares.filter(user_id=usuario_actual)[0].imagen.url
        else:
            avatar_usuario = "/media/default_avatar.jpg"

    
    return render(request, "app_blogs/inicio.html", {"avatar_usuario":avatar_usuario})

def sobre_nosotros(request):
    return render(request, "app_blogs/sobre_nosotros.html")

def registrar_usuario(request):
    if request.method == 'POST':
        formulario_registro_usuario = Usuario_formulario(request.POST)
        if formulario_registro_usuario.is_valid():
            usuario = formulario_registro_usuario    
            usuario.save()

            
            
            nombre_usuario = formulario_registro_usuario.cleaned_data['username']
            pass_usuario = formulario_registro_usuario.cleaned_data['password1']
            user = authenticate(username = nombre_usuario, password = pass_usuario)
            login(request,user)
            return redirect("Inicio")
        else:
            formulario_registro_usuario = Usuario_formulario()
            mensaje = "Error en los datos ingresados, por favor, verifiquelos y vuelva a intentar"
            return render(request, "app_blogs/registrar_usuario.html", {"formulario_registro_usuario":formulario_registro_usuario, "mensaje":mensaje})

    else:
        if request.user.is_authenticated:
            return redirect("Inicio")
        else:
            formulario_registro_usuario = Usuario_formulario()
            
            return render(request, "app_blogs/registrar_usuario.html", {"formulario_registro_usuario":formulario_registro_usuario})

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            user = authenticate(username = usuario, password = contra)

            if user is not None:
                login(request, user)

                return redirect("Inicio")
            else:
                mensaje = "Error en los datos ingresados"
                form = AuthenticationForm()
                return render(request, "app_blogs/iniciar_sesion.html", {'form':form, 'mensaje':mensaje})
        else:
            mensaje = "Error en los datos ingresados"
            form = AuthenticationForm()
            return render(request, "app_blogs/iniciar_sesion.html", {'form':form, 'mensaje':mensaje})

    else:
        if request.user.is_authenticated:
            return redirect("Inicio")
        else:
            form = AuthenticationForm()
            return render(request, "app_blogs/iniciar_sesion.html", {'form':form})



@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("Inicio")

@login_required
def panel_usuario(request):
    #si el usuario no tiene un avatar, muestro el avatar default en el sitio, si no, muestro el del usuario

    
    usuario_actual = request.user.id
    avatares = Avatar.objects
    existe = False
    for avatar in avatares.all():
        if usuario_actual == avatar.user_id:
            existe = True
    if existe:
        avatar_usuario = avatares.filter(user_id=usuario_actual)[0].imagen.url
    else:
        avatar_usuario = "/media/default_avatar.jpg"
    return render(request, "app_blogs/panel_usuario.html", {"avatar_usuario":avatar_usuario})

def ver_todos_blogs(request):
    #me traigo la lista de blogs para mostrar
    blogs = Blog.objects.all()
    #me traigo la lista de usuarios, la voy a necesitar para determinar autor del post
    usuarios = User.objects.all()
    mensaje = ""
    #Si no hay blogs creados todavia, debo de informarlo
    if not blogs:
        mensaje = "Todavía no hay ningún blog"
    return render(request, "app_blogs/ver_blogs.html", {"blogs":blogs, "usuarios":usuarios, "mensaje":mensaje})

def ver_blog(request, id_blog):
    #Busco el blog que tenga esa id
    try:
        blog = Blog.objects.get(id =id_blog)
    except:
        return render(request, "app_blogs/blog_no_existe.html")
    else:
        if request.method == "POST":
            formulario_comentario = Comentario_formulario(request.POST)
            if formulario_comentario.is_valid():
                comentario = Comentario(user= request.user, id_blog= id_blog, cuerpo= formulario_comentario.cleaned_data['cuerpo'])
                comentario.save()
                usuarios = User.objects.all()
                autor_id = blog.user_id
                avatares = Avatar.objects
                existe = False
                for avatar in avatares.all():
                    if autor_id == avatar.user_id:
                        existe = True
                if existe:
                    avatar_usuario = avatares.filter(user_id=autor_id)[0].imagen.url
                else:
                    avatar_usuario = "/media/default_avatar.jpg"
                formulario_comentario = Comentario_formulario()
                comentarios = Comentario.objects.filter(id_blog__exact = id_blog)

                return render(request, "app_blogs/ver_blog_detalle.html", {"blog":blog, "usuarios":usuarios, "avatar_usuario":avatar_usuario, "formulario_comentario":formulario_comentario, "comentarios":comentarios})

            else:
                mensaje = "Error en el comentario"
                usuarios = User.objects.all()
                autor_id = blog.user_id
                avatares = Avatar.objects
                existe = False
                for avatar in avatares.all():
                    if autor_id == avatar.user_id:
                        existe = True
                if existe:
                    avatar_usuario = avatares.filter(user_id=autor_id)[0].imagen.url
                else:
                    avatar_usuario = "/media/default_avatar.jpg"
                formulario_comentario = Comentario_formulario()
                comentarios = Comentario.objects.filter(id_blog__exact = id_blog)

                return render(request, "app_blogs/ver_blog_detalle.html", {"blog":blog, "usuarios":usuarios, "avatar_usuario":avatar_usuario, "formulario_comentario":formulario_comentario, "mensaje":mensaje, "comentarios":comentarios})
        else:
            usuarios = User.objects.all()
            autor_id = blog.user_id
            avatares = Avatar.objects
            existe = False
            for avatar in avatares.all():
                if autor_id == avatar.user_id:
                    existe = True
            if existe:
                avatar_usuario = avatares.filter(user_id=autor_id)[0].imagen.url
            else:
                avatar_usuario = "/media/default_avatar.jpg"
            formulario_comentario = Comentario_formulario()
            comentarios = Comentario.objects.filter(id_blog__exact = id_blog)
            
            return render(request, "app_blogs/ver_blog_detalle.html", {"blog":blog, "usuarios":usuarios, "avatar_usuario":avatar_usuario, "formulario_comentario":formulario_comentario, "comentarios":comentarios})

@login_required
def crear_blog(request):
    if request.method == "POST":
        mi_formulario = Blog_formulario(request.POST, request.FILES)

        if mi_formulario.is_valid():
            usuario = User.objects.get(username=request.user)
            blog = Blog(user=usuario, titulo= mi_formulario.cleaned_data['titulo'], subtitulo = mi_formulario.cleaned_data['subtitulo'], cuerpo = mi_formulario.cleaned_data['cuerpo'], imagen = mi_formulario.cleaned_data['imagen'])
            blog.save()
            return redirect("Ver Blogs")
        else:
            mensaje = "Hubo un error en el formulario, vuelva a intentarlo"
            mi_formulario= Blog_formulario()
            return render(request, "app_blogs/crear_blog.html", {"mi_formulario":mi_formulario, "mensaje":mensaje} )
    else:
        mi_formulario = Blog_formulario()
        return render(request, "app_blogs/crear_blog.html", {"mi_formulario":mi_formulario} )


@login_required
def editar_avatar_usuario(request):
    if request.method == "POST":

        mi_formulario = Avatar_formulario(request.POST, request.FILES)

        if mi_formulario.is_valid():
            
            usuario = User.objects.get(username=request.user)

            #me fijo si el usuario ya tenia un avatar
            avatares = Avatar.objects.all()
            tiene_avatar = False
            for av in avatares:
                if av.user_id == usuario.id:
                    tiene_avatar =True
            
            if tiene_avatar:
                #el usuario ya tiene un avatar, por lo que recupero el objeto avatar y lo edito
                avatar = avatares.filter(user_id = usuario.id)[0]
                avatar.imagen = mi_formulario.cleaned_data['imagen']
                avatar.save()
                return redirect("Panel Usuario")
            else:
                #el usuario no tiene avatar, por lo que creo un nuevo objeto avatar y lo agrego
                avatar = Avatar(user=usuario, imagen = mi_formulario.cleaned_data['imagen'])
                avatar.save()
                return redirect("Panel Usuario") 

    else:
        #si el usuario no tiene un avatar, muestro el avatar default en el sitio, si no, muestro el del usuario
        usuario_actual = request.user.id
        avatares = Avatar.objects
        existe = False
        for avatar in avatares.all():
            if usuario_actual == avatar.user_id:
                existe = True
        if existe:
            avatar_usuario = avatares.filter(user=usuario_actual)[0].imagen.url
        else:
            avatar_usuario = "/media/default_avatar.jpg"

        mi_formulario = Avatar_formulario()
        return render(request, "app_blogs/editar_avatar.html", {"avatar_usuario":avatar_usuario, "mi_formulario":mi_formulario})

@login_required
def borrar_avatar_usuario(request):
    usuario = User.objects.get(username=request.user)
    avatares = Avatar.objects.all()
    tiene_avatar = False
    for av in avatares:
        if av.user_id == usuario.id:
            tiene_avatar =True

    if tiene_avatar:
        #el usuario ya tiene un avatar, por lo que recupero el objeto avatar y lo edito
        avatar = avatares.filter(user_id = usuario.id)[0]
        avatar.delete()
        return redirect("Panel Usuario")
    else:
        return redirect("Panel Usuario") 

@login_required
def editar_email_usuario(request):
    usuario = User.objects.get(username=request.user)
    if request.method == "POST":
        mi_formulario = Email_formulario(request.POST)
        if mi_formulario.is_valid():
            usuario.email = mi_formulario.cleaned_data['email']
            usuario.save()
            return redirect("Panel Usuario")
        else:
            mensaje = "No ingresaste un mail valido"
            mi_formulario=Email_formulario(initial={'email':usuario.email})
            return render(request, "app_blogs/editar_email.html", {"mi_formulario":mi_formulario, "mensaje":mensaje}  )
    else:
        mi_formulario = Email_formulario(initial={"email":usuario.email})
        return render(request, "app_blogs/editar_email.html", {"mi_formulario":mi_formulario}  )


@login_required
def cambiar_pass(request):
    if request.method == "POST":
        formulario = PasswordChangeForm(request.user, request.POST)
        if formulario.is_valid():
            usuario= formulario.save()
            update_session_auth_hash(request, usuario)
            return redirect("Panel Usuario")
        else:
            mensaje = "Cometiste un error en el formulario"
            formulario = PasswordChangeForm(request.user)
            return render(request,"app_blogs/cambiar_pass.html", {"formulario":formulario, "mensaje":mensaje})
    else:
        formulario = PasswordChangeForm(request.user)
        return render(request,"app_blogs/cambiar_pass.html", {"formulario":formulario})



@login_required
def administrar_blogs_usuario(request):
    blogs_usuario = Blog.objects.filter(user_id = request.user.id)
    if not blogs_usuario:
        #Si el usuario todavía no creo ningún blog, le aviso que no hay nada para administrar
        return render(request, "app_blogs/administracion_blogs_usuario_vacio.html")
    return render(request, "app_blogs/administracion_blogs_usuario.html", {"blogs_usuario":blogs_usuario})

@login_required
def editar_blog_usuario_texto(request, id_blog):
    blog_a_editar = Blog.objects.get(id=id_blog)
    if blog_a_editar.user_id == request.user.id:
        if request.method == "POST":
            mi_formulario =  Blog_formulario_editar_texto(request.POST)

            if mi_formulario.is_valid():
                blog_a_editar.titulo = mi_formulario.cleaned_data['titulo']
                blog_a_editar.subtitulo = mi_formulario.cleaned_data['subtitulo']
                blog_a_editar.cuerpo = mi_formulario.cleaned_data['cuerpo']

                blog_a_editar.save()

                return redirect("Administrar Blogs")
            else:
                mensaje = "Hubo un error en los campos ingresados"
                mi_formulario= Blog_formulario_editar_texto(initial={"titulo":blog_a_editar.titulo, "subtitulo":blog_a_editar.subtitulo, "cuerpo":blog_a_editar.cuerpo})
                return render(request, "app_blogs/editar_blog.html", {"mi_formulario":mi_formulario, "mensaje":mensaje}  )
        else:
            mi_formulario =  Blog_formulario_editar_texto(initial={"titulo":blog_a_editar.titulo, "subtitulo":blog_a_editar.subtitulo, "cuerpo":blog_a_editar.cuerpo})
            return render(request, "app_blogs/editar_blog.html", {"mi_formulario":mi_formulario}  )
    else:
         #si el usuario no es el dueño del blog, lo mando a inicio
        return redirect("Inicio")

@login_required
def editar_blog_usuario_imagen(request, id_blog):
    blog_a_editar = Blog.objects.get(id=id_blog)
    #checkeo que sea el usuario correcto y no sea alguien ingresando por url
    if blog_a_editar.user_id == request.user.id:
        if request.method == "POST":
            mi_formulario =  Blog_formulario_editar_imagen(request.POST, request.FILES)

            if mi_formulario.is_valid():
                blog_a_editar.imagen = mi_formulario.cleaned_data['imagen']
                blog_a_editar.save()

                return redirect("Administrar Blogs")
            else:
                mensaje = "Hubo un error en los campos ingresados"
                mi_formulario= Blog_formulario_editar_imagen()
                imagen_actual = blog_a_editar.imagen.url
                return render(request, "app_blogs/editar_blog_imagen.html", {"mi_formulario":mi_formulario, "mensaje":mensaje, "imagen_actual":imagen_actual}  )
        else:
            mi_formulario =  Blog_formulario_editar_imagen()
            imagen_actual = blog_a_editar.imagen.url

            return render(request, "app_blogs/editar_blog_imagen.html", {"mi_formulario":mi_formulario, "imagen_actual":imagen_actual}  )
    else:
        #si el usuario no es el dueño del blog, lo mando a inicio
        return redirect("Inicio")

@login_required
def borrar_blog(request, id_blog):
    blog_a_borrar = Blog.objects.get(id=id_blog)
    if blog_a_borrar.user_id == request.user.id:
        if request.method == "POST":
            blog_a_borrar.delete()
            return redirect("Administrar Blogs")
        else:
            return render(request, "app_blogs/borrar_blog.html")
    else:
        #si el usuario no es el dueño del blog, lo mando a inicio
        return redirect("Inicio")

