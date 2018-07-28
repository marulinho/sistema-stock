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
