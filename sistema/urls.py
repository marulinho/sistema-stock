from django.conf.urls import url

from rest.modulo_seguridad import preguntas

urlpatterns = [

    url(r'^buscarPreguntas/$', preguntas.buscar_preguntas, name='buscarPreguntas'),
]
