from __future__ import unicode_literals
from django.db import transaction
from django.db import IntegrityError
from django.http import HttpResponse

from sistema.models import Pregunta
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METHOD_GET])
def buscar_preguntas(request):

    response = HttpResponse()

    try:
        preguntas = Pregunta.objects.filter(habilitado = True)
        response.content = armar_response_list_content(preguntas)
        response.status_code = 200
        return response

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)


