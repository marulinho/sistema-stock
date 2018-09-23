from __future__ import unicode_literals

from django.db import transaction
from django.db import IntegrityError

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *
from sistema.utils.dto import *

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def registar_cliente(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        #comprobamos que vengan los datos obligatorios
        else:
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = datos[NOMBRE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE)
            if APELLIDO in datos and not (APELLIDO == ''):
                apellido = datos[APELLIDO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE)
            if DNI in datos and not (DNI == ''):
                dni = datos[DNI]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_DNI_FALTANTE)
            if TELEFONO in datos and not (TELEFONO == ''):
                telefono = datos[TELEFONO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_TELEFONO_FALTANTE)
            if DIRECCION in datos and not (DIRECCION == ''):
                direccion = datos[DIRECCION]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_DIRECCION_FALTANTE)
            if TIPO_CLIENTE in datos and not (TIPO_CLIENTE == ''):
                tipo_cliente_ingresado = datos[TIPO_CLIENTE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_TIPO_CLIENTE_FALTANTE)

            estado_tipo_cliente = EstadoTipoCliente.objects.get(nombre = ESTADO_HABILITADO)

            if TipoCliente.objects.filter(nombre = tipo_cliente_ingresado,estado = estado_tipo_cliente).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TIPO_CLIENTE_INEXISTENTE)

            tipo_cliente = TipoCliente.objects.get(nombre = tipo_cliente_ingresado,estado = estado_tipo_cliente)

            estado_cliente_habilitado = EstadoCliente.objects.get(nombre = ESTADO_HABILITADO)

            if Cliente.objects.filter(dni = dni, estado = estado_cliente_habilitado, tipo_cliente = tipo_cliente).__len__()>=1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CLIENTE_EXISTENTE)

            cliente = Cliente(nombre=nombre,
                              apellido=apellido,
                              dni=dni,
                              telefono=telefono,
                              direccion=direccion,
                              estado=estado_cliente_habilitado,
                              tipo_cliente=tipo_cliente)
            cliente.saveNewCliente()
            response.content = armar_response_content(None,CREACION_CLIENTE)
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
def modificar_cliente(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if ID_CLIENTE in datos and not (ID_CLIENTE == ''):
                cliente_modificar = Cliente.objects.get(codigo=datos[ID_CLIENTE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_CLIENTE_FALTANTE)
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = datos[NOMBRE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE)
            if APELLIDO in datos and not (APELLIDO == ''):
                apellido = datos[APELLIDO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE)
            if TELEFONO in datos and not (TELEFONO == ''):
                telefono = datos[TELEFONO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_TELEFONO_FALTANTE)
            if DIRECCION in datos and not (DIRECCION == ''):
                direccion = datos[DIRECCION]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_DIRECCION_FALTANTE)

            cliente_modificar.nombre = nombre
            cliente_modificar.apellido = apellido
            cliente_modificar.telefono = telefono
            cliente_modificar.direccion = direccion
            cliente_modificar.save()

            response.content = armar_response_content(None,MODIFICACION_CLIENTE)
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
def eliminar_cliente(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if ID_CLIENTE in datos and not (ID_CLIENTE ==''):
                cliente_eliminar = Cliente.objects.get(codigo=datos[ID_CLIENTE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_CLIENTE_FALTANTE)

            estado_deshabilitado = EstadoCliente.objects.get(nombre=ESTADO_DESHABILITADO)
            cliente_eliminar.estado=estado_deshabilitado
            cliente_eliminar.save()
            response.content = armar_response_content(None,ELIMINACION_CLIENTE)
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
def obtener_cliente_id(request,id_cliente):
    try:
        response = HttpResponse()
        if id_cliente == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_CLIENTE_FALTANTE)
        else:
            if Cliente.objects.filter(codigo = id_cliente).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE)


            cliente = Cliente.objects.get(codigo=id_cliente)

            dto_cliente = DTOCliente(cliente.codigo,
                                     cliente.nombre,
                                     cliente.apellido,
                                     cliente.dni,
                                     cliente.telefono,
                                     cliente.direccion,
                                     cliente.tipo_cliente.nombre,
                                     cliente.estado.nombre)
            response.content = armar_response_content(dto_cliente)
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
def obtener_clientes(request):
    try:
        response = HttpResponse()

        estado_habilitado = EstadoCliente.objects.get(nombre = ESTADO_HABILITADO)

        if Cliente.objects.filter(estado = estado_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CLIENTES_INHABILITADOS)

        cliente = Cliente.objects.filter(estado = estado_habilitado)

        lista_dto_cliente = []
        for x in range(0,cliente.__len__()):
            dto_cliente = DTOCliente(cliente[x].codigo,
                                     cliente[x].nombre,
                                     cliente[x].apellido,
                                     cliente[x].dni,
                                     cliente[x].telefono,
                                     cliente[x].direccion,
                                     cliente[x].tipo_cliente.nombre,
                                     cliente[x].estado.nombre)
            lista_dto_cliente.append(dto_cliente)
        response.content = armar_response_list_content(lista_dto_cliente)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)