# coding=utf-8
from json import dumps

from django.core.serializers.json import DjangoJSONEncoder

#Error llamada api call
ERROR_METODO_INCORRECTO = 'ERROR_METODO_INCORRECTO'

#Error datos incompletos al hacer el api call
ERROR_DATOS_INCORRECTOS = 'ERROR_DATOS_INCORRECTOS'
ERROR_DATOS_FALTANTES = 'ERROR_DATOS_FALTANTES'
DETALLE_ERROR_DATOS_INCOMPLETOS = "Faltan ingresar datos"

ERROR_DE_SISTEMA = 'Error de sistema'
DETALLE_ERROR_SISTEMA = "Error procesando llamada"

KEY_ERROR_CODE = 'error_code'
KEY_ERROR_DESCRIPTION = 'error_description'

#Error datos faltantes entidades
DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE = "Debe ingresar el usuario"
DETALLE_ERROR_REGISTRACION_CONTRASENIA_FALTANTE = "Debe ingresar la contraseña"
DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE = "Debe ingresar el nombre del usuario"
DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE = "Debe ingresar el apellido del usuario"
DETALLE_ERROR_REGISTRACION_DNI_FALTANTE = "Debe ingresar el dni del usuario"
DETALLE_ERROR_REGISTRACION_TELEFONO_FALTANTE = "Debe ingresar el telefono del usuario"
DETALLE_ERROR_REGISTRACION_DIRECCION_FALTANTE = "Debe ingresar la direccion del usuario"
DETALLE_ERROR_REGISTRACION_TIPO_CLIENTE_FALTANTE = "Debe ingresar el tipo de cliente"
DETALLE_ERROR_TIPO_CLIENTE_INEXISTENTE = "No existe el tipo de cliente ingresado"
DETALLE_ERROR_CLIENTE_EXISTENTE = "Cliente existente, reintente con otros datos"
DETALLE_ERROR_CLIENTE_INEXISTENTE = "No existe el cliente ingresado"
DETALLE_ERROR_ID_CLIENTE_FALTANTE = "Debe ingresar el identificador del cliente"
DETALLE_ERROR_CLIENTES_INHABILITADOS = "No existen clientes habilitados"
DETALLE_ERROR_REGISTRACION_PREGUNTA_FALTANTE = "Debe seleccionar una pregunta de seguridad"
DETALLE_ERROR_PREGUNTA_FALTANTE = "Debe ingresar el identificador de la pregunta de seguridad"
DETALLE_ERROR_DESCRIPCION_PREGUNTA_FALTANTE = "Debe ingresar la pregunta de seguridad"
DETALLE_ERROR_PREGUNTA_INEXISTENTE = "No existe la pregunta de seguridad ingresada"
DETALLE_ERROR_RESPUESTAS_NO_COINCIDEN = "Las respuestas de seguridad no coinciden"
DETALLE_ERROR_REGISTRACION_PREGUNTA_NO_EXISTE = "Debe seleccionar una pregunta existente"
DETALLE_ERROR_REGISTRACION_USUARIO_EXISTE = "Usuario existente, intente con un nuevo usuario"
DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE = "No existe el usuario ingresado"
DETALLE_ERROR_REGISTRACION_USUARIO_CONTRASENIA_IGUALES = "Debe ingresar una contrasenia distinta al usuario"
DETALLE_ERROR_REGISTRACION_RESPUESTA_DESCRIPCION_FALTANTE = "Debe ingresar una respuesta"
DETALLE_ERROR_ID_USUARIO_FALTANTE = "Debe ingresar el identificador del usuario"
DETALLE_ERROR_CAMBIAR_CONTRASENIA_NUEVA_FALTANTE = "Debe ingresar una contrasenia nueva"
DETALLE_ERROR_CAMBIAR_CONTRASENIA_ACTUAL_FALTANTE = "Debe ingresar la contrasenia actual"
DETALLE_ERROR_CAMBIAR_CONTRASENIA_ACTUAL_NUEVA_IGUALES = "Las contrasenias deben ser diferentes"
DETALLE_ERROR_CREDENCIALES_INCORRECTAS = "Usuario o contraseña incorrecta"
DETALLE_ERROR_LOGOUT_SIN_LOGIN = "Debe iniciar sesion antes de cerrarla"
DETALLE_ERROR_LOGOUT_FALLIDO = "No se pudo cerra sesion, intente de nuevo"
DETALLE_ERROR_LOGOUT_EXITOSO = "Finalizo la sesion correctamente"
DETALLE_ERROR_RESPUESTA_INEXISTENTE = "Debe ingresar un usuario y pregunta que tenga una respuesta"
DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE = 'Debe ingresar un codigo para la categoria'
DETALLE_ERROR_CODIGO_INEXISTENTE = 'Debe ingresar un codigo existente'
DETALLE_ERROR_NOMBRE_CATEGORIA_FALTANTE = 'Debe ingresar el nombre de la categoria'
DETALLE_ERROR_NOMBRE_CATEGORIA_EXISTENTE = 'El nombre de categoria ya existe, intente con otro'
DETALLE_ERROR_CATEGORIA_INEXISTENTE = 'No existe una categoria con el indentificador ingresado'
DETALLE_ERROR_CATEGORIA_HABILITADA_INEXISTENTE = 'No existe una categoria hablitada con el indentificador ingresado'
DETALLE_ERROR_CATEGORIAS_INEXISTENTES = 'No existen categorias habilitadas'
DETALLE_ERROR_PRODUCTO_EXISTENTE = 'Las caracteristicas ingresadas le corresponden a un producto existete'
DETALLE_ERROR_PRODUCTOS_INEXISTENTES = 'No existen productos habilitados'
DETALLE_ERROR_PRODUCTO_INEXISTENTE = 'No existe un producto con el codigo ingresado'
DETALLE_ERROR_NOMBRE_PRODUCTO_FALTANTE = 'Debe ingresar el nombre del producto'
DETALLE_ERROR_MARCA_PRODUCTO_FALTANTE = 'Debe ingresar la marca del producto'
DETALLE_ERROR_NOMBRE_PRODUCTO_EXISTENTE = 'El nombre de producto ya existe, intente con otro'
DETALLE_ERROR_CODIGO_PRODUCTO_FALTANTE = 'Debe ingresar un codigo para el producto'
DETALLE_ERROR_MEDIDA_PRODUCTO_FALTANTE = 'Debe ingresar una medida del producto'
DETALLE_ERROR_UNIDAD_MEDIDA_PRODUCTO_FALTANTE = 'Debe ingresar una unidad de medida del producto'
DETALLE_ERROR_UNIDAD_MEDIDA_PRODUCTO_INEXISTENTE = 'No existe la unidad de medida ingresada'
DETALLE_ERROR_UNIDAD_MEDIDA_HABILITADA = 'No existen unidades de medidas habilitadas'
DETALLE_ERROR_ID_UNIDAD_MEDIDA_FALTANTE = 'Debe ingresar el identificador de la unidad de medida'
DETALLE_ERROR_ID_UNIDAD_MEDIDA_INEXISTENTE = 'No existe una unidad de medida con el identificador ingresado'
DETALLE_ERROR_STOCK_MINIMO_PRODUCTO_FALTANTE = 'Debe ingresar el stock minimo del producto'
DETALLE_ERROR_STOCK_MINIMO_PRODUCTO_INSUFICIENTE = 'El stock minimo debe ser mayor que cero'
DETALLE_ERROR_NOMBRE_SUBCATEGORIA_EXISTENTE = 'El nombre de subcategoria ya existe, intente con otro'
DETALLE_ERROR_CODIGO_SUBCATEGORIA_FALTANTE = 'Debe ingresar el codigo de la subcategoria'
DETALLE_ERROR_NOMBRE_SUBCATEGORIA_FALTANTE = 'Debe ingresar el nombre de la subcategoria'
DETALLE_ERROR_SUBCATEGORIAS_INEXISTENTES = 'No existen subcategorias habilitadas'
DETALLE_ERROR_SUBCATEGORIA_INEXISTENTE = 'No existe un subcategoria con el identificador ingresado'
DETALLE_ERROR_CATEGORIA_SUBCATEGORIA_INEXISTENTE = 'No existen subcategorias habilitadas para la categoria seleccionada'
DETALLE_ERROR_CATEGORIA_PRODUCTO_INEXISTENTE = 'No existen productos habilitados para la categoria seleccionada'
DETALLE_ERROR_SUBCATEGORIA_PRODUCTO_INEXISTENTE = 'No existen productos habilitados para la subcategoria seleccionada'
ASIGNACION_SUBCATEGORIA_EXITOSA = 'La subcategoria se asigno correctamente'
ASIGNACION_PRODUCTO_EXITOSA = 'El producto se asigno correctamente'
DESASIGNACION_PRODUCTO_EXITOSA = 'El producto se desasigno correctamente'
DESASIGNACION_SUBCATEGORIA_EXITOSA = 'La categoria se desasigno correctamente'
DETALLE_ERROR_NOMBRE_COMBO_FALTANTE = 'Debe ingresar el nombre del combo'
DETALLE_ERROR_PRECIO_COMBO_FALTANTE = 'Debe ingresar el precio del combo'
DETALLE_ERROR_PRECIO_COMBO_INSUFICIENTE = 'Debe ingresar un precio mayor que cero'
DETALLE_ERROR_NOMBRE_COMBO_EXISTENTE = 'El nombre del combo ya existe, intente con otro'
DETALLE_ERROR_LISTA_PRODUCTO_COMBO_FALTANTE = 'Debe ingresar una lista de productos'
DETALLE_ERROR_LISTA_PRODUCTO_COMBO_LONGITUD_INSUFICIENTE = 'Debe ingresar dos o más productos'
DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_FALTANTE = 'Debe ingresar una cantidad para cada producto la lista'
DETALLE_ERROR_LISTA_PRODUCTO_COMBO_PRODUCTOS_REPETIDOS = 'No se puede ingresar dos o más veces el mismo producto'
DETALLE_ERROR_LISTA_COMBO_REPETIDOS = 'No se puede ingresar dos o mas veces el mismo combo'
DETALLE_ERROR_CANTIDAD_LISTA_PRODUCTO_COMBO_LONGITUD_DISTINTA = 'Debe ingresar una cantidad y precio por cada producto seleccionado'
DETALLE_ERROR_CANTIDAD_LISTA_PRODUCTO_COMPRA_LONGITUD_DISTINTA = 'Debe ingresar una cantidad para cada producto'
DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_MENOR = 'Debe ingresar cantidades mayores a cero'
DETALLE_ERROR_CODIGO_COMBO_FALTANTE = 'Debe ingresar el codigo del combo'
DETALLE_ERROR_CODIGO_COMBO_INEXISTENTE = 'No existe un combo con el codigo ingresado'
DETALLE_ERROR_NOMBRE_LISTA_PRECIO_FALTANTE = 'Debe ingresar el nombre de la lista de precio'
DETALLE_ERROR_LISTA_PRODUCTO_LISTA_PRECIO_FALTANTE = 'Debe ingresar la lista de productos que van a conformar la lista de precios'
DETALLE_ERROR_LISTA_PRODUCTO_LISTA_PRECIO_LONGITUD_INSUFICIENTE = 'La lista de precios debe contener por lo menos un producto'
DETALLE_ERROR_LISTA_PRODUCTO_LISTA_PRECIO_PRODUCTOS_REPETIDOS = 'No se puede ingresar dos o más veces el mismo producto'
DETALLE_ERROR_LISTA_PRECIOS_COMPRA_LISTA_PRECIO_FALTANTE = 'Debe ingresar la lista de precios de compra de los de productos que van a conformar la lista de precios'
DETALLE_ERROR_LISTA_PRECIOS_COMPRA_LISTA_PRECIO_INSUFICIENTE = 'Debe ingresar un precio de compra mayor a cero'
DETALLE_ERROR_LISTA_PRECIO_VENTA_LISTA_PRECIO_INSUFICIENTE = 'Debe ingresar un precio de venta mayor a cero'
DETALLE_ERROR_LISTA_PRECIO_LONGITUD_DISTINTA = 'Las cantidades ingresadas no se corresponden'
DETALLE_ERROR_NOMBRE_LISTA_PRECIO_EXISTENTE = 'El nombre de la lista ya existe, intente con otro'
DETALLE_ERROR_PRECIO_PRODUCTOS_COMBO_FALTANTE = 'Debe ingresar la lista de precios de los de productos que van a conformar el combo'
DETALLE_ERROR_MARGEN_GANANCIA_PRODUCTOS_COMBO_MENOR = 'Los margenes de ganancia de los productos deben ser mayores a cero'
DETALLE_ERROR_LISTA_PRECIOS_VENTA_LISTA_PRECIO_FALTANTE = 'Debe ingresar la lista de precios de venta de los productos que van a conformar la lista de precios'
DETALLE_ERROR_LISTA_PRECIO_VENTA_COMPRA_LISTA_PRECIO_IGUALES = 'El precio de venta debe ser mayor al precio de compra'
DETALLE_ERROR_CODIGO_LISTA_PRECIO_FALTANTE = 'Debe ingresar el codigo de la lista de precios'
DETALLE_ERROR_CODIGO_LISTA_PRECIO_INEXISTENTE = 'No existe una lista de precios con el codigo ingresado'
DETALLE_ERROR_LISTA_PRECIO_NO_HABILITADA = 'No hay listas de precios habilitadas'
DETALLE_ERROR_LISTA_PRECIO_SIN_DETALLE = 'La lista de precios no tiene detalles'
DETALLE_ERROR_PRODUCTO_INEXISTENTE_LISTA = 'No existe el producto en la lista de precios'
DETALLE_ERROR_PRODUCTOS_DESHABILITADOS = 'No existen productos habilitados'
DETALLE_ERROR_COMBO_DETALLE_INEXISTENTE = 'No existe un detalle asociado al producto'
DETALLE_ERROR_COMBO_SIN_DETALLE = 'El combo no tiene detalles'
DETALLE_ERROR_COMBO_NO_HABILITADO = 'No existen combos habilitados'
DETALLE_ERROR_COMPRA_INEXISTENTE = 'No existe una compra con el codigo ingresado'
DETALLE_ERROR_COMPRA_SIN_DETALLE = 'La compra no tiene asociado detalles'
DETALLE_ERROR_CANTIDAD_NO_DISPONIBLE = 'No puede generar un movimiento de productos mayor al stock disponible'
DETALLE_ERROR_REMITO_INEXISTENTE = 'No existe un remito con el codigo ingresado'
DETALLE_ERROR_REMITOS_INEXISTENTE = 'No ha realizado remitos'
DETALLE_ERROR_REMITO_SIN_DETALLE = 'El remito no tiene asociado detalles'
DETALLE_ERROR_CODIGO_COMPRA_FALTANTE = 'Debe ingresar el codigo de la compra'
DETALLE_ERROR_TIPO_MOVIMIENTO_CAPITAL_FALTANTE = 'Debe ingresar el tipo de movimiento de capital'
DETALLE_ERROR_TIPO_MOVIMIENTO_CAPITAL_INEXISTENTE = 'El tipo de movimiento no existe'
DETALLE_ERROR_CODIGO_MOVIMIENTO_CAPITAL_SALIDA_FALTANTE = 'Debe ingresar el codigo del movimiento de salida de capital'
DETALLE_ERROR_CODIGO_MOVIMIENTO_CAPITAL_ENTRADA_FALTANTE = 'Debe ingresar el codigo del movimiento de entrada de capital'
DETALLE_ERROR_MOVIMIENTO_SALIDA_CAPITAL_INEXISTENTE = 'No existe un movimiento de salida de capital con el codigo ingresado'
DETALLE_ERROR_DESCRIPCION_MOVIMIENTO_CAPITAL_SALIDA_FALTANTE = 'El movimiento debe tener una descripcion'
DETALLE_ERROR_TOTAL_MOVIMIENTO_CAPITAL_SALIDA_FALTANTE = 'El movimiento debe tener un total'
DETALLE_ERROR_TOTAL_MOVIMIENTO_CAPITAL_SALIDA_INSUFICIENTE = 'El movimiento debe tener un total mayor que cero'
DETALLE_ERROR_CODIGO_MOVIMIENTO_CAPITAL_FALTANTE = 'El movimiento debe tener un codigo'
DETALLE_ERROR_MOVIMIENTO_CAPITAL_INEXISTENTE = 'No existe un movimiento de capital con el codigo ingresado'
DETALLE_ERROR_CAJA_CERRADA = 'La caja debe estar abierta'
DETALLE_ERROR_CAJA_ABIERTA = 'No existe una caja abierta'
DETALLE_ERROR_CAJA_ABIERTA_EXISTENTE = 'Debe cerrar la caja antes de volver abrirla'
DETALLE_ERROR_CAJA_SIN_DETALLES = 'La caja no tiene detalles'
DETALLE_ERROR_NO_HAY_CAJA = 'No existen cajas'
DETALLE_ERROR_COMPRAS_INEXISTENTES = 'No ha realizado compras'
DETALLE_ERROR_CODIGO_COMPRA_FALTANTE = 'Debe ingresar el codigo de la compra'
DETALLE_ERROR_STOCK_INSUFICIENTE_CANCELAR_COMPRA = 'No dispone del stock suficiente para cancelar la compra'
DETALLE_ERROR_MOVIMIENTO_CAPITAL_EXISTENTE = 'Ya existe un movimiento de salida de capital asociado al movimiento de stock'
DETALLE_ERROR_ESTADO_INEXISTENTE = 'No existe un estado con el nombre ingresado'
DETALLE_ERROR_CODIGO_REMITO_FALTANTE = 'Debe ingresar el codigo del remito'
DETALLE_ERROR_STOCK_INSUFICIENTE_VENTA = 'No dispone del stock suficiente para realizar la venta'
DETALLE_ERROR_VENTA_INEXISTENTE = 'No existe una venta con el codigo ingresado'
DETALLE_ERROR_VENTA_SIN_DETALLE = 'La venta no tiene asociado detalles'
DETALLE_ERROR_VENTAS_INEXISTENTES = 'No ha realizado ventas'
DETALLE_ERROR_CODIGO_VENTA_FALTANTE = 'Debe ingresar el codigo de venta'
DETALLE_ERROR_VENTA_CANCELADA = 'La venta ya ha sido cancelada'
DETALLE_ERROR_VENTA_SIN_MOVIMIENTO_CAPITAL = 'La venta no tiene asociada un movimiento de entrada de capital'
DETALLE_ERROR_RETIROS_INEXISTENTES = 'No existen retiros de capital'
DETALLE_ERROR_CODIGO_RETIRO_FALTANTE = 'Debe ingresar el codigo del retiro'
DETALLE_ERROR_NOMBRE_SORTEO_EXISTENTE = 'El nombre ingresado ya existe, por favor ingrese otro'
DETALLE_ERROR_CANTIDAD_SORTEO_MAYOR = 'La cantidad de productos a sortear debe ser menor o igual que la disponible'
DETALLE_ERROR_NOMBRE_FALTANTE = 'Debe ingresar el nombre'
DETALLE_ERROR_LISTA_SORTEO_FALTANTE = 'Debe ingresar los ganadores con los respectivos productos'
DETALLE_ERROR_SORTEOS_INEXISTENTES = 'No existen sorteos habilitados'
DETALLE_ERROR_CODIGO_SORTEO_FALTANTE= 'Debe ingresar el codigo del sorteo'
DETALLE_ERROR_SORTEO_INEXISTENTE= 'No existe un sorteo con el codigo ingresado'
DETALLE_ERROR_SORTEO_SIN_DETALLE= 'El sorteo no tiene asociado detalles'
DETALLE_ERROR_CANTIDAD_PRODUCTO_FALTANTE = 'Debe ingresar la cantidad de productos'
DETALLE_ERROR_FECHA_DESDE_FALTANTE = 'Debe ingresar la fecha de origen'
DETALLE_ERROR_FECHA_HASTA_FALTANTE = 'Debe ingresar la fecha de destino'
DETALLE_ERROR_FECHA_DESDE_MAYOR_HASTA = 'La fecha hasta debe ser mayor o igual a la fecha desde'
DETALLE_ERROR_COMPRAS_VENTAS_CERO = 'No se han realizado transacciones en el perído de tiempo seleccionado'
DETALLE_ERROR_LISTA_PRECIO_INEXISTENTE = 'No existe una lista de precio para el periodo seleccionado'
DETALLE_FORMA_PAGO_FALTANTE = 'Debe ingresar el medio de pago'

# Metodos

def build_error(response, error_code, error_descripcion):
    content = {KEY_ERROR_DESCRIPTION: error_descripcion, KEY_ERROR_CODE: error_code}
    response.content = dumps(content, cls=DjangoJSONEncoder)

    return response


def build_bad_request_error(response, error_code, error_descripcion):
    response.status_code = 400
    return build_error(response, error_code, error_descripcion)


def build_unauthorized_error(response, error_code, error_descripcion):
    response.status_code = 401

    return build_error(response, error_code, error_descripcion)


def build_method_not_allowed_error(response, error_code, error_descripcion):
    response.status_code = 405

    return build_error(response, error_code, error_descripcion)


def build_internal_server_error(response, error_code, error_descripcion):
    response.status_code = 500

    return build_error(response, error_code, error_descripcion)
