from __future__ import unicode_literals

from string import lower
from django.db import transaction
from django.db import IntegrityError
from iteration_utilities import duplicates

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.dto import  *
from sistema.utils.error_handler import *


@transaction.atomic()
@metodos_requeridos([METODO_POST])
def registrar_combo(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = lower(datos[NOMBRE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_COMBO_FALTANTE)


            if LISTA_PRODUCTOS in datos and not (datos[LISTA_PRODUCTOS] == []):
                lista_productos = datos[LISTA_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_FALTANTE)
            if lista_productos.__len__() < 2:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_LONGITUD_INSUFICIENTE)
            if list(duplicates(lista_productos)):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_PRODUCTOS_REPETIDOS)

            if CANTIDAD_PRODUCTOS in datos and not (CANTIDAD_PRODUCTOS == []):
                cantidad_productos = datos[CANTIDAD_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_FALTANTE)
            for x in range(0, cantidad_productos.__len__()):
                if cantidad_productos[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_MENOR)

            if MARGEN_GANANCIA_PRODUCTO_COMBO in datos and not (MARGEN_GANANCIA_PRODUCTO_COMBO == []):
                margen_ganancia_productos_combo = datos[MARGEN_GANANCIA_PRODUCTO_COMBO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRECIO_PRODUCTOS_COMBO_FALTANTE)

            for x in range(0, margen_ganancia_productos_combo.__len__()):
                if margen_ganancia_productos_combo[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MARGEN_GANANCIA_PRODUCTOS_COMBO_MENOR)

            if (cantidad_productos.__len__() != lista_productos.__len__()) or (cantidad_productos.__len__() != margen_ganancia_productos_combo.__len__()) or (margen_ganancia_productos_combo.__len__() != lista_productos.__len__()):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_LISTA_PRODUCTO_COMBO_LONGITUD_DISTINTA)

            estado_combo_habilitado = EstadoCombo.objects.get(nombre=ESTADO_HABILITADO)
            if Combo.objects.filter(nombre=nombre, estado=estado_combo_habilitado).__len__() > 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_COMBO_EXISTENTE)

            precio_combo = 0
            # creamos el combo
            combo_creado = Combo(nombre=nombre,
                                 precio = precio_combo,
                                 estado=estado_combo_habilitado)
            combo_creado.saveNewCombo()

            estado_habilitado_lista_precio = EstadoListaPrecio.objects.get(nombre=ESTADO_HABILITADO)
            if ListaPrecio.objects.filter(vigencia_hasta=None, estado=estado_habilitado_lista_precio).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_NO_HABILITADA)

            lista_precio = ListaPrecio.objects.get(vigencia_hasta=None,estado=estado_habilitado_lista_precio)
            if ListaPrecioDetalle.objects.filter(lista_precio=lista_precio).__len__() <1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_SIN_DETALLE)

            # verificamos que existan los productos y creamos los combos_detalle
            estado_producto_habilitado = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)

            for x in range(0, lista_productos.__len__()):
                if Producto.objects.filter(codigo=lista_productos[x], estado=estado_producto_habilitado).__len__() < 1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
                else:
                    producto_ingresado = Producto.objects.get(codigo=lista_productos[x],estado=estado_producto_habilitado)

                    #obtengo el precio del producto

                    if ListaPrecioDetalle.objects.filter(lista_precio = lista_precio, producto = producto_ingresado).__len__()<1:
                        raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE_LISTA)
                    else:
                        precio_producto = ListaPrecioDetalle.objects.get(lista_precio = lista_precio, producto = producto_ingresado).precio_unitario_compra

                    combo_detalle_creado = ComboDetalle(cantidad=cantidad_productos[x],
                                                        precio_unitario_producto_combo = precio_producto,
                                                        subtotal = (precio_producto * (1+(margen_ganancia_productos_combo[x]/100.00))) * cantidad_productos[x],
                                                        margen_ganancia_producto_combo = margen_ganancia_productos_combo[x],
                                                        producto=producto_ingresado,
                                                        combo=combo_creado)
                    precio_combo += combo_detalle_creado.subtotal
                    combo_detalle_creado.save()
            combo_creado.precio = precio_combo
            combo_creado.save()
            response.content = armar_response_content(None, CREACION_COMBO)
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
def eliminar_combo(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                codigo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMBO_FALTANTE)

            estado_combo_habilitado = EstadoCombo.objects.get(nombre=ESTADO_HABILITADO)
            if Combo.objects.filter(codigo=codigo, estado=estado_combo_habilitado).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMBO_INEXISTENTE)

            estado_combo_deshabilitado = EstadoCombo.objects.get(nombre=ESTADO_DESHABILITADO)
            combo_ingresado = Combo.objects.get(codigo=codigo, estado=estado_combo_habilitado)
            combo_ingresado.estado = estado_combo_deshabilitado
            combo_ingresado.save()
            response.content = armar_response_content(None, ELIMINACION_COMBO)
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
def obtener_combo_id(request, id_combo):
    try:
        response = HttpResponse()
        if id_combo != '':
            codigo = id_combo
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMBO_FALTANTE)

        estado_combo_habilitado = EstadoCombo.objects.get(nombre=ESTADO_HABILITADO)
        if Combo.objects.filter(codigo=codigo, estado=estado_combo_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMBO_INEXISTENTE)

        combo_ingresado = Combo.objects.get(codigo=codigo, estado=estado_combo_habilitado)

        dto_cabecera_combo = DTOCombo(combo_ingresado.codigo,
                                      combo_ingresado.nombre,
                                      combo_ingresado.precio)

        if ComboDetalle.objects.filter(combo=combo_ingresado).__len__()<1:
            raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_COMBO_SIN_DETALLE)
        else:
            combo_detalle = ComboDetalle.objects.filter(combo=combo_ingresado)
        dto_lista_detalle_combo = []
        for x in range(0,combo_detalle.__len__()):
            dto_combo_detalle = DTOComboDetalle(combo_detalle[x].producto.codigo,
                                                combo_detalle[x].producto.nombre,
                                                combo_detalle[x].producto.marca,
                                                combo_detalle[x].producto.unidad_medida.nombre,
                                                combo_detalle[x].producto.medida,
                                                combo_detalle[x].precio_unitario_producto_combo,
                                                combo_detalle[x].margen_ganancia_producto_combo,
                                                combo_detalle[x].cantidad,
                                                combo_detalle[x].subtotal,
                                                combo_detalle[x].producto.stock_local)
            dto_lista_detalle_combo.append(dto_combo_detalle)
        dto_lista_combo = DTOListaCombo(dto_cabecera_combo,dto_lista_detalle_combo)
        response.content = armar_response_content(dto_lista_combo)
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
def obtener_combos_vigentes(request):
    try:
        response = HttpResponse()

        estado_combo_habilitado = EstadoCombo.objects.get(nombre=ESTADO_HABILITADO)
        if Combo.objects.filter(estado=estado_combo_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMBO_INEXISTENTE)

        combos_habilitados = Combo.objects.filter(estado=estado_combo_habilitado).order_by('-codigo')

        lista_dto_combo = []

        for x in range(0,combos_habilitados.__len__()):
            lista_dto_combo_detalles = []
            dto_combo = DTOCombo(combos_habilitados[x].codigo,
                                 combos_habilitados[x].nombre,
                                 combos_habilitados[x].precio)
            #lista_dto_combo.append(dto_combo)
            detalle_combo = ComboDetalle.objects.filter(combo = combos_habilitados[x])
            for y in range(0, detalle_combo.__len__()):
                dto_combo_detalle = DTOComboDetalle(detalle_combo[y].producto.codigo,
                                                    detalle_combo[y].producto.nombre,
                                                    detalle_combo[y].producto.marca,
                                                    detalle_combo[y].producto.unidad_medida.nombre,
                                                    detalle_combo[y].producto.medida,
                                                    detalle_combo[y].precio_unitario_producto_combo,
                                                    detalle_combo[y].margen_ganancia_producto_combo,
                                                    detalle_combo[y].cantidad,
                                                    detalle_combo[y].subtotal,
                                                    detalle_combo[y].producto.stock_local)
                lista_dto_combo_detalles.append(dto_combo_detalle)
            dto_lista_combo = DTOListaCombo(dto_combo,lista_dto_combo_detalles)
            lista_dto_combo.append(dto_lista_combo)
            #lista_dto_combo.append(dto_combo)
        response.content = armar_response_list_content(lista_dto_combo)
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
def modificar_combo(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not CODIGO == '':
                codigo_combo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMBO_FALTANTE)

            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = lower(datos[NOMBRE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_COMBO_FALTANTE)

            if LISTA_PRODUCTOS in datos and not (LISTA_PRODUCTOS == []):
                lista_productos = datos[LISTA_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_FALTANTE)
            if lista_productos.__len__() < 2:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_LONGITUD_INSUFICIENTE)
            if list(duplicates(lista_productos)):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_PRODUCTOS_REPETIDOS)

            if CANTIDAD_PRODUCTOS in datos and not (CANTIDAD_PRODUCTOS == []):
                cantidad_productos = datos[CANTIDAD_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_FALTANTE)
            for x in range(0, cantidad_productos.__len__()):
                if cantidad_productos[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_MENOR)

            if MARGEN_GANANCIA_PRODUCTO_COMBO in datos and not (MARGEN_GANANCIA_PRODUCTO_COMBO == []):
                margen_ganancia_productos_combo = datos[MARGEN_GANANCIA_PRODUCTO_COMBO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRECIO_PRODUCTOS_COMBO_FALTANTE)

            for x in range(0, margen_ganancia_productos_combo.__len__()):
                if margen_ganancia_productos_combo[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MARGEN_GANANCIA_PRODUCTOS_COMBO_MENOR)

            if (cantidad_productos.__len__() != lista_productos.__len__()) or (cantidad_productos.__len__() != margen_ganancia_productos_combo.__len__()) or (margen_ganancia_productos_combo.__len__() != lista_productos.__len__()):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_LISTA_PRODUCTO_COMBO_LONGITUD_DISTINTA)

            estado_combo_habilitado = EstadoCombo.objects.get(nombre=ESTADO_HABILITADO)
            if Combo.objects.filter(codigo = codigo_combo, estado = estado_combo_habilitado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMBO_INEXISTENTE)
            else:
                combo_actual = Combo.objects.get(codigo = codigo_combo, estado = estado_combo_habilitado)

            if Combo.objects.filter(nombre=nombre, estado=estado_combo_habilitado).__len__() > 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_COMBO_EXISTENTE)

            estado_habilitado_lista_precio = EstadoListaPrecio.objects.get(nombre=ESTADO_HABILITADO)
            if ListaPrecio.objects.filter(vigencia_hasta=None, estado=estado_habilitado_lista_precio).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_NO_HABILITADA)

            lista_precio = ListaPrecio.objects.get(vigencia_hasta=None,estado=estado_habilitado_lista_precio)
            if ListaPrecioDetalle.objects.filter(lista_precio=lista_precio).__len__() <1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_SIN_DETALLE)

            # verificamos que existan los productos y creamos los combos_detalle
            estado_producto_habilitado = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)

            precio = 0
            for x in range(0, lista_productos.__len__()):

                if Producto.objects.filter(codigo=lista_productos[x], estado=estado_producto_habilitado).__len__() < 1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
                else:
                    producto_ingresado = Producto.objects.get(codigo=lista_productos[x],estado=estado_producto_habilitado)

                if ComboDetalle.objects.filter(combo = combo_actual, producto= producto_ingresado).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_COMBO_DETALLE_INEXISTENTE)
                else:
                    combo_detalle =  ComboDetalle.objects.get(combo = combo_actual, producto= producto_ingresado)

                    combo_detalle.cantidad = cantidad_productos[x]
                    combo_detalle.margen_ganancia_producto_combo = margen_ganancia_productos_combo[x]
                    combo_detalle.subtotal = combo_detalle.precio_unitario_producto_combo * (1+(margen_ganancia_productos_combo[x]/100.00)) * cantidad_productos[x]
                    combo_detalle.subtotal = round(combo_detalle.subtotal,2)
                    precio += combo_detalle.subtotal
                    combo_detalle.save()
            combo_actual.precio = precio
            combo_actual.nombre = nombre
            combo_actual.save()
            response.content = armar_response_content(None, MODIFICACION_COMBO)
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
def actualizar_precio_combo(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            estado_combo_habilitado = EstadoCombo.objects.get(nombre=ESTADO_HABILITADO)
            if Combo.objects.filter(estado=estado_combo_habilitado).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_COMBO_NO_HABILITADO)

            estado_habilitado_lista_precio = EstadoListaPrecio.objects.get(nombre=ESTADO_HABILITADO)
            if ListaPrecio.objects.filter(vigencia_hasta=None, estado=estado_habilitado_lista_precio).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_NO_HABILITADA)

            lista_precio = ListaPrecio.objects.get(vigencia_hasta=None,estado=estado_habilitado_lista_precio)
            if ListaPrecioDetalle.objects.filter(lista_precio=lista_precio).__len__() <1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRECIO_SIN_DETALLE)

            combos_habilitados = Combo.objects.filter(estado=estado_combo_habilitado)

            for x in range(combos_habilitados.__len__()):
                combo_detalles = ComboDetalle.objects.filter(combo = combos_habilitados[x])
                precio_combo = 0
                for y in range(combo_detalles.__len__()):
                    if Producto.objects.filter(codigo = combo_detalles[y].producto.codigo).__len__()<1:
                        raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
                    producto_combo_detalle = Producto.objects.get(codigo = combo_detalles[y].producto.codigo)

                    #buscamos el precio actual del producto
                    if ListaPrecioDetalle.objects.filter(lista_precio = lista_precio, producto = producto_combo_detalle).__len__()<1:
                        combo_detalles[y].precio_unitario_producto_combo = 0
                    else:
                        lista_precio_producto = ListaPrecioDetalle.objects.get(lista_precio = lista_precio, producto = producto_combo_detalle)
                        combo_detalles[y].precio_unitario_producto_combo = lista_precio_producto.precio_unitario_compra
                    combo_detalles[y].subtotal = combo_detalles[y].precio_unitario_producto_combo * combo_detalles[y].cantidad * (1+combo_detalles[y].margen_ganancia_producto_combo /100)
                    precio_combo += combo_detalles[y].subtotal
                    combo_detalles[y].save()
                combos_habilitados[x].precio = precio_combo
                combos_habilitados[x].save()

            response.content = armar_response_content(None, PRECIO_COMBO_ACTUALIZADO)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

