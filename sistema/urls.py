from django.conf.urls import url

from sistema.rest.modulo_seguridad import preguntas,usuario

urlpatterns = [

    url(r'^buscarPreguntas/$', preguntas.buscar_preguntas, name='buscarPreguntas'),
    url(r'^obtenerPreguntaId/(?P<id_pregunta>[0-9]+)/$', preguntas.obtener_pregunta_id, name='obtenerPreguntaId'),
    url(r'^obtenerPreguntaDescripcion/$', preguntas.obtener_pregunta_descripcion, name='obtenerPreguntaDescripcion'),
    url(r'^registrarUsuario/$', usuario.registar_usuario, name='registrarUsuario'),
    url(r'^modificarUsuario/$', usuario.modificar_usuario, name='modificarUsuario'),
    url(r'^eliminarUsuario/$', usuario.eliminar_usuario, name='eliminarUsuario'),
    url(r'^obtenerUsuarioId/(?P<id_usuario>[0-9]+)/$', usuario.obtener_usuario_id, name='obtenerUsuarioId'),
    url(r'^obtenerUsuario/(?P<usuario>[0-9a-zA-z]+)/$', usuario.obtener_usuario_por_usuario, name='obtenerUsuario'),
    url(r'^modificarContrasenia/$', usuario.cambiar_contrasenia, name='modificarContrasenia'),
    url(r'^recuperarCuenta/$', usuario.recuperar_cuenta, name='recuperarCuenta'),
    url(r'^iniciarSesion/$', usuario.iniciar_sesion, name='iniciarSesion'),
    url(r'^finalizarSesion/$', usuario.finalizar_sesion, name='finalizarSesion'),
]
