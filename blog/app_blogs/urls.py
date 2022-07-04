from django.urls import path
from app_blogs import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('registrar_usuario', views.registrar_usuario, name="Registrar Usuario"),
    path('iniciar_sesion', views.iniciar_sesion, name="Iniciar Sesion"),
    path('cerrar_sesion', views.cerrar_sesion, name="Cerrar Sesion"),
    path('panel_usuario', views.panel_usuario, name="Panel Usuario"),
    path('editar_avatar_usuario', views.editar_avatar_usuario, name="Editar Avatar"),
    path('borrar_avatar_usuario', views.borrar_avatar_usuario, name="Borrar Avatar"),
    path('editar_email_usuario', views.editar_email_usuario, name="Editar Email"),
    path('cambiar_pass', views.cambiar_pass, name="Cambiar Pass"),
    path('administrar_blogs_usuario', views.administrar_blogs_usuario, name="Administrar Blogs"),
    path('editar_blog_usuario_texto/<id_blog>', views.editar_blog_usuario_texto, name="Editar Blog"),
    path('editar_blog_usuario_imagen/<id_blog>', views.editar_blog_usuario_imagen, name="Editar Imagen Blog"),
    path('borrar_blog/<id_blog>', views.borrar_blog, name="Borrar Blog"),
    path('ver_blogs', views.ver_todos_blogs, name="Ver Blogs"),
    path('ver_blogs/<id_blog>', views.ver_blog, name="Ver Blog ID"),
    path('crear_blog', views.crear_blog, name="Crear Blog"),
    path('sobre_nosotros', views.sobre_nosotros, name="Sobre Nosotros")
]

urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
