from __future__ import unicode_literals

from _iteration_utilities import duplicates
from string import lower
from django.db import transaction
from django.db import IntegrityError
import pytz
import datetime

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *


@transaction.atomic()
@metodos_requeridos([METODO_POST])
def registrar_lista_precio(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = lower(datos[NOMBRE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_LISTA_PRECIO_FALTANTE)

            if LISTA_PRODUCTOS in datos and not (LISTA_PRODUCTOS == []):
                lista_productos = datos[LISTA_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_LISTA_PRECIO_FALTANTE)
            if lista_productos.__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_LISTA_PRECIO_LONGITUD_INSUFICIENTE)
            if list(duplicates(lista_productos)):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_LISTA_PRECIO_PRODUCTOS_REPETIDOS)

            if LISTA_PRECIOS_COMPRA in datos and not (LISTA_PRECIOS_COMPRA == []):
                lista_precios_compra = datos[LISTA_PRECIOS_COMPRA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIOS_COMPRA_LISTA_PRECIO_FALTANTE)
            for x in range(0,lista_precios_compra.__len__()):
                if lista_precios_compra[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIOS_COMPRA_LISTA_PRECIO_INSUFICIENTE)

            if LISTA_PRECIOS_VENTA in datos and not (LISTA_PRECIOS_VENTA == []):
                lista_precios_venta = datos[LISTA_PRECIOS_VENTA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIOS_VENTA_LISTA_PRECIO_FALTANTE)
            for x in range(0,lista_precios_venta.__len__()):
                if lista_precios_venta[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_VENTA_LISTA_PRECIO_INSUFICIENTE)
                else:
                    if lista_precios_venta[x] <= lista_precios_compra[x]:
                        raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_VENTA_COMPRA_LISTA_PRECIO_IGUALES)

            if (lista_productos.__len__() != lista_precios_compra.__len__()) or (lista_productos.__len__() != lista_precios_venta.__len__()) or (lista_precios_compra.__len__() != lista_precios_venta.__len__()):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_LONGITUD_DISTINTA)


            estado_lista_precio_habilitada = EstadoListaPrecio.objects.get(nombre=ESTADO_HABILITADO)
            if ListaPrecio.objects.filter(nombre=nombre, estado=estado_lista_precio_habilitada).__len__() > 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_LISTA_PRECIO_EXISTENTE)

            # creamos la lista de precios
            lista_precio_creada = ListaPrecio(nombre=nombre,
                                             vigencia_desde = datetime.datetime.now(pytz.utc),
                                             estado=estado_lista_precio_habilitada)
            lista_precio_creada.saveNewListaPrecio()

            # verificamos que existan los productos y creamos los detalle_lista_precio
            estado_producto_habilitado = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
            for x in range(0, lista_productos.__len__()):
                if Producto.objects.filter(codigo=lista_productos[x], estado=estado_producto_habilitado).__len__() < 1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
                else:
                    producto_ingresado = Producto.objects.get(codigo=lista_productos[x],
                                                              estado=estado_producto_habilitado)
                    lista_precio_detalle_creada = ListaPrecioDetalle(precio_unitario_compra=lista_precios_compra[x],
                                                                     precio_unitario_venta = lista_precios_venta[x],
                                                                     producto=producto_ingresado,
                                                                     lista_precio=lista_precio_creada)
                    lista_precio_detalle_creada.save()

            response.content = armar_response_content(None, CREACION_LISTA_PRECIO)
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
def eliminar_lista_precio(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                codigo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_LISTA_PRECIO_FALTANTE)

            estado_lista_precio_habilitada = EstadoListaPrecio.objects.get(nombre=ESTADO_HABILITADO)
            if ListaPrecio.objects.filter(codigo=codigo, estado=estado_lista_precio_habilitada).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_LISTA_PRECIO_INEXISTENTE)

            estado_lista_precio_deshabilitada = EstadoListaPrecio.objects.get(nonbre=ESTADO_DESHABILITADO)
            lista_precio_ingresada = ListaPrecio.objects.get(codigo=codigo, estado=estado_lista_precio_habilitada)
            lista_precio_ingresada.estado = estado_lista_precio_deshabilitada
            lista_precio_ingresada.save()
            response.content = armar_response_content(None, ELIMINACION_LISTA_PRECIO)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)
