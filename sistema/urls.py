from django.conf.urls import url

from sistema.rest.modulo_seguridad import preguntas,usuario

urlpatterns = [

    url(r'^buscarPreguntas/$', preguntas.buscar_preguntas, name='buscarPreguntas'),
    url(r'^guardarUsuario/$', usuario.guardar_usuario, name='guardarUsuario'),
    url(r'^modificarUsuario/$', usuario.modificar_usuario, name='modificarUsuario'),
    url(r'^eliminarUsuario/$', usuario.eliminar_usuario, name='eliminarUsuario'),
    url(r'^obtenerUsuario/(?P<id_usuario>[0-9]+)/$', usuario.obtener_usuario, name='obtenerUsuario'),
    url(r'^modificarContrasenia/$', usuario.cambiar_contrasenia, name='modificarContrasenia'),
]
