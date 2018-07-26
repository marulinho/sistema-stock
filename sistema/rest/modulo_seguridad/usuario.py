from __future__ import unicode_literals

import datetime
from string import lower

import pytz
from django.db import transaction
from django.db import IntegrityError
from django.http import HttpResponse

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def registar_usuario(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        #comprobamos que vengan los datos obligatorios
        else:
            if USUARIO in datos and not (USUARIO == ''):
                usuario = datos[USUARIO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE)
            if CONTRASENIA in datos and not (CONTRASENIA == ''):
                contrasenia = datos[CONTRASENIA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_CONTRASENIA_FALTANTE)
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = datos[NOMBRE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE)
            if APELLIDO in datos and not (APELLIDO == ''):
                apellido = datos[APELLIDO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE)
            if ID_PREGUNTA in datos and not (ID_PREGUNTA == ''):
                id_pregunta = datos[ID_PREGUNTA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_PREGUNTA_FALTANTE)
            if RESPUESTA_DESCRIPCION in datos and not (RESPUESTA_DESCRIPCION == ''):
                respuesta_descripcion = datos[RESPUESTA_DESCRIPCION]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_RESPUESTA_DESCRIPCION_FALTANTE)

            #Validamos que la pregunta exista
            if Pregunta.objects.filter(id=id_pregunta,
                                       habilitado=True).__len__() <1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_PREGUNTA_NO_EXISTE)
            else:
                pregunta = Pregunta.objects.get(id=id_pregunta,habilitado=True)

             #Validamos que el usuario no exista
            if Usuario.objects.filter(usuario = usuario).__len__()>=1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_EXISTE)

            #Validamos que el usuario sea distinto a la contrasenia
            if usuario == contrasenia:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_CONTRASENIA_IGUALES)

            estado = EstadoUsuario.objects.get(nombre=ESTADO_HABILITADO)

            #Creamos el usuario
            usuario_creado = Usuario(nombre = nombre,
                                     apellido = apellido,
                                     usuario = usuario,
                                     contrasenia = contrasenia,
                                     fecha_desde = datetime.datetime.now(pytz.utc),
                                     pregunta = pregunta,
                                     estado = estado)
            usuario_creado.save()

            respuesta = RespuestaPregunta(descripcion = lower(respuesta_descripcion),
                                          usuario = usuario_creado,
                                          pregunta = pregunta)
            respuesta.save()
            response.content = armar_response_content(None,CREACION_USUARIO)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def modificar_usuario(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if ID_USUARIO in datos and not (ID_USUARIO == ''):
                usuario_modificar = Usuario.objects.get(id=datos[ID_USUARIO])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = datos[NOMBRE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE)
            if APELLIDO in datos and not (APELLIDO == ''):
                apellido = datos[APELLIDO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE)
            if RESPUESTA_DESCRIPCION in datos and not (RESPUESTA_DESCRIPCION == ''):
                respuesta_descripcion = datos[RESPUESTA_DESCRIPCION]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_RESPUESTA_DESCRIPCION_FALTANTE)

            # Validamos que la pregunta exista
            if Pregunta.objects.filter(id=usuario_modificar.pregunta_id,
                                        habilitado=True).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_PREGUNTA_NO_EXISTE)
            else:
                pregunta = Pregunta.objects.get(id=usuario_modificar.pregunta_id, habilitado=True)

            usuario_modificar.nombre = nombre
            usuario_modificar.apellido = apellido
            usuario_modificar.pregunta = pregunta
            usuario_modificar.save()

            if RespuestaPregunta.objects.filter(usuario = usuario_modificar,
                                                pregunta = pregunta).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_RESPUESTA_INEXISTENTE)
            else:
                respuesta_modificada = RespuestaPregunta.objects.get(usuario = usuario_modificar,
                                                                     pregunta = pregunta)
            respuesta_modificada.descripcion = respuesta_descripcion
            respuesta_modificada.save()
            response.content = armar_response_content(None,MODIFICACION_USUARIO)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def eliminar_usuario(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if ID_USUARIO in datos and not (ID_USUARIO ==''):
                usuario_eliminar = Usuario.objects.get(id=datos[ID_USUARIO])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)

            estado_deshabilitado = EstadoUsuario.objects.get(nombre=ESTADO_DESHABILITADO)
            usuario_eliminar.estado=estado_deshabilitado
            usuario_eliminar.save()
            response.content = armar_response_content(None,ELIMINACION_USUARIO)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_usuario_id(request,id_usuario):
    try:
        response = HttpResponse()
        if id_usuario == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)
        else:
            if Usuario.objects.get(id = id_usuario):
                usuario = Usuario.objects.get(id = id_usuario)
                response.content = armar_response_content(usuario)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_usuario_por_usuario(request,usuario):
    try:
        response = HttpResponse()
        if usuario == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE)
        else:
            if Usuario.objects.get(usuario = usuario):
                usuario_actual = Usuario.objects.get(usuario = usuario)
                response.content = armar_response_content(usuario_actual)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)



@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def cambiar_contrasenia(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CONTRASENIA_NUEVA in datos and not (CONTRASENIA_NUEVA == ''):
                contrasenia_nueva = datos[CONTRASENIA_NUEVA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAMBIAR_CONTRASENIA_NUEVA_FALTANTE)
            if CONTRASENIA_ACTUAL in datos and not (CONTRASENIA_ACTUAL == ''):
                contrasenia_actual = datos[CONTRASENIA_ACTUAL]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAMBIAR_CONTRASENIA_ACTUAL_FALTANTE)
            if contrasenia_actual == contrasenia_nueva:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAMBIAR_CONTRASENIA_ACTUAL_NUEVA_IGUALES)
            if ID_USUARIO in datos and not (ID_USUARIO == ''):
                usuario = Usuario.objects.get(id = datos[ID_USUARIO])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)
            if SesionUsuario.objects.filter(usuario=usuario,
                                            fecha_hora_hasta__isnull=True).__len__() >= 1:
                sesion_usuario = SesionUsuario.objects.get(usuario=usuario, fecha_hora_hasta__isnull=True)
                sesion_usuario.fecha_hora_hasta = datetime.datetime.now(pytz.utc)
                sesion_usuario.save()
                usuario.contrasenia = contrasenia_nueva
                usuario.save()
                response.content = armar_response_content(None, CAMBIO_CONTRASENIA_USUARIO)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LOGOUT_SIN_LOGIN)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def recuperar_cuenta(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if ID_USUARIO in datos and not (ID_USUARIO == ''):
                usuario = Usuario.objects.get(id=datos[ID_USUARIO])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)
            if ID_PREGUNTA in datos and not (ID_PREGUNTA == ''):
               if Pregunta.objects.get(id=datos[ID_PREGUNTA]):
                   pregunta = Pregunta.objects.get(id = datos[ID_PREGUNTA])
               else:
                   raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PREGUNTA_INEXISTENTE)
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PREGUNTA_FALTANTE)
            if RESPUESTA_DESCRIPCION in datos and not (RESPUESTA_DESCRIPCION == ''):
                respuesta_ingresada = datos[RESPUESTA_DESCRIPCION]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_RESPUESTA_DESCRIPCION_FALTANTE)
            respuesta_guardada = RespuestaPregunta.objects.get(usuario = usuario,
                                                               pregunta = pregunta)
            if lower(respuesta_guardada.descripcion) != lower(respuesta_ingresada):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_RESPUESTAS_NO_COINCIDEN)
            if CONTRASENIA_NUEVA in datos and not (CONTRASENIA_NUEVA == ''):
                usuario.contrasenia = datos[CONTRASENIA_NUEVA]
                usuario.save()
                response.content = armar_response_content(None,CAMBIO_CONTRASENIA_USUARIO)
                response.status_code = 200
                return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def iniciar_sesion(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if USUARIO in datos and not (USUARIO == ''):
                usuario_ingresado = datos[USUARIO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE)
            if CONTRASENIA in datos and not (CONTRASENIA == ''):
                contrasenia_ingresada = datos[CONTRASENIA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_CONTRASENIA_FALTANTE)

            #busco el usuario asociado a los parametros ingresados
            estado_habilitado = EstadoUsuario.objects.get(nombre=ESTADO_HABILITADO)

            if Usuario.objects.filter(usuario = usuario_ingresado,
                                   contrasenia = contrasenia_ingresada,
                                   estado = estado_habilitado).__len__() >=1 :
                usuario = Usuario.objects.get(usuario = usuario_ingresado,
                                              contrasenia = contrasenia_ingresada,
                                              estado = estado_habilitado)
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CREDENCIALES_INCORRECTAS)

            #busco que no tenga sesion activa y si tiene la cierro
            if SesionUsuario.objects.filter(usuario = usuario,
                                            fecha_hora_hasta__isnull = True).__len__()>=1:
                sesion_usuario = SesionUsuario.objects.get(usuario = usuario, fecha_hora_hasta__isnull = True)
                sesion_usuario.fecha_hora_hasta = datetime.datetime.now(pytz.utc)
                sesion_usuario.save()
            else:
                sesion_nueva = SesionUsuario(fecha_hora_desde = datetime.datetime.now(pytz.utc),
                                             usuario = usuario)
                sesion_nueva.save()
            response.content = armar_response_content(usuario)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def finalizar_sesion(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if ID_USUARIO in datos and not (ID_USUARIO == ''):
                usuario_ingresado = datos[ID_USUARIO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE)

            # busco el usuario asociado a los parametros ingresados
            estado_habilitado = EstadoUsuario.objects.get(nombre=ESTADO_HABILITADO)

            if Usuario.objects.filter(id=usuario_ingresado,
                                   estado=estado_habilitado).__len__()>=1:
                usuario = Usuario.objects.get(id=usuario_ingresado,
                                              estado=estado_habilitado)
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LOGOUT_FALLIDO)

            # busco sesion activa y la cierro
            if SesionUsuario.objects.filter(usuario=usuario,
                                            fecha_hora_hasta__isnull=True).__len__() >= 1:
                sesion_usuario = SesionUsuario.objects.get(usuario=usuario,fecha_hora_hasta__isnull=True )
                sesion_usuario.fecha_hora_hasta = datetime.datetime.now(pytz.utc)
                sesion_usuario.save()
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LOGOUT_SIN_LOGIN)
            response.content = armar_response_content(None,DETALLE_ERROR_LOGOUT_EXITOSO)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)
