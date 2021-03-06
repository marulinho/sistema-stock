from django.conf.urls import url

from sistema.rest.modulo_seguridad import preguntas
from sistema.rest.modulo_seguridad import usuario
from sistema.rest.modulo_seguridad import cliente
from sistema.rest.modulo_seguridad import respuestas
from sistema.rest.modulo_administracion import categoria
from sistema.rest.modulo_administracion import subcategoria
from sistema.rest.modulo_administracion import producto
from sistema.rest.modulo_administracion import unidad_medida
from sistema.rest.modulo_administracion import combo
from sistema.rest.modulo_administracion import lista_precio
from sistema.rest.modulo_administracion import sorteo
from sistema.rest.modulo_finanzas import compra
from sistema.rest.modulo_finanzas import retiro
from sistema.rest.modulo_finanzas import remito
from sistema.rest.modulo_finanzas import caja
from sistema.rest.modulo_finanzas import ventas
from sistema.rest.modulo_reportes import reporte

urlpatterns = [

    #PREGUNTAS
    url(r'^buscarPreguntas/$', preguntas.buscar_preguntas, name='buscarPreguntas'),
    url(r'^obtenerPreguntaId/(?P<id_pregunta>[0-9]+)/$', preguntas.obtener_pregunta_id, name='obtenerPreguntaId'),
    url(r'^obtenerPreguntaDescripcion/$', preguntas.obtener_pregunta_descripcion, name='obtenerPreguntaDescripcion'),
    url(r'^obtenerUsuarioPregunta/(?P<usuario>[0-9a-zA-Z]+)/$', preguntas.obtener_pregunta_usuario, name='obtenerUsuarioPregunta'),

    #RESPUESTAS
    url(r'^obtenerRespuestaUsuarioPregunta/(?P<id_usuario>[0-9a-zA-Z]+)/(?P<id_pregunta>[0-9a-zA-Z]+)/$', respuestas.obtener_respuesta_pregunta_usuario, name='obtenerRespuestaUsuarioPregunta'),

    #USUARIOS
    url(r'^registrarUsuario/$', usuario.registar_usuario, name='registrarUsuario'),
    url(r'^modificarUsuario/$', usuario.modificar_usuario, name='modificarUsuario'),
    url(r'^eliminarUsuario/$', usuario.eliminar_usuario, name='eliminarUsuario'),
    url(r'^obtenerUsuarioId/(?P<id_usuario>[0-9]+)/$', usuario.obtener_usuario_id, name='obtenerUsuarioId'),
    url(r'^obtenerUsuario/(?P<usuario>[0-9a-zA-z]+)/$', usuario.obtener_usuario_por_usuario, name='obtenerUsuario'),
    url(r'^modificarContrasenia/$', usuario.cambiar_contrasenia, name='modificarContrasenia'),
    url(r'^recuperarCuenta/$', usuario.recuperar_cuenta, name='recuperarCuenta'),
    url(r'^iniciarSesion/$', usuario.iniciar_sesion, name='iniciarSesion'),
    url(r'^finalizarSesion/$', usuario.finalizar_sesion, name='finalizarSesion'),

    #CLIENTES
    url(r'^registrarCliente/$', cliente.registar_cliente, name='registrarCliente'),
    url(r'^modificarCliente/$', cliente.modificar_cliente, name='modificarCliente'),
    url(r'^eliminarCliente/$', cliente.eliminar_cliente, name='eliminarCliente'),
    url(r'^obtenerClientes/$', cliente.obtener_clientes, name='obtenerClientes'),
    url(r'^obtenerClienteId/(?P<id_cliente>[0-9]+)/$', cliente.obtener_cliente_id, name='obtenerClienteId'),

    #CATEGORIAS
    url(r'^registrarCategoria/$', categoria.registrar_categoria, name='registrarCategoria'),
    url(r'^modificarCategoria/$', categoria.modificar_categoria, name='modificarCategoria'),
    url(r'^eliminarCategoria/$', categoria.eliminar_categoria, name='eliminarCategoria'),
    url(r'^obtenerCategorias/$', categoria.obtener_categorias, name='obtenerCategorias'),
    url(r'^obtenerCategoriaId/(?P<id_categoria>[0-9]+)/$', categoria.obtener_categoria_id, name='obtenerCategoriaId'),
    url(r'^habilitarCategoria/(?P<id_categoria>[0-9]+)/$', categoria.habilitar_categoria, name='habilitarCategoria'),
    url(r'^desasignarProductoCategoria/$', categoria.desasignar_producto_categoria, name='desasignarProductoCategoria'),
    url(r'^desasignarSubcategoriaCategoria/$', categoria.desasignar_subcategoria_categoria, name='desasignarSubcategoriaCategoria'),

    #SUBCATEGORIAS
    url(r'^registrarSubCategoria/$', subcategoria.registrar_subcategoria, name='registrarSubCategoria'),
    url(r'^modificarSubCategoria/$', subcategoria.modificar_subcategoria, name='modificarSubCategoria'),
    url(r'^eliminarSubCategoria/$', subcategoria.eliminar_subcategoria, name='eliminarSubCategoria'),
    url(r'^obtenerSubCategorias/$', subcategoria.obtener_subcategorias, name='obtenerSubCategorias'),
    url(r'^obtenerSubCategoriaId/(?P<id_subcategoria>[0-9]+)/$', subcategoria.obtener_subcategoria_id, name='obtenerSubCategoriaId'),
    url(r'^obtenerSubCategoriaCategoria/(?P<id_categoria>[0-9]+)/$', subcategoria.obtener_subcategorias_categoriaid, name='obtenerSubCategoriaCategoria'),
    url(r'^obtenerSubCategoriaNoCategoria/(?P<id_categoria>[0-9]+)/$', subcategoria.obtener_subcategorias_no_categoriaid, name='obtenerSubCategoriaNoCategoria'),
    url(r'^asignarSubcategoriaCategoria/$', subcategoria.asginar_subcategoria_categoria, name='asignarSubcategoriaCategoria'),
    url(r'^desasignarProductoSubCategoria/$', subcategoria.desasignar_producto_subcategoria, name='desasignarProductoSubCategoria'),

    #PRODUCTOS
    url(r'^registrarProducto/$', producto.registrar_producto, name='registrarProducto'),
    url(r'^modificarProducto/$', producto.modificar_producto, name='modificarProducto'),
    url(r'^eliminarProducto/$', producto.eliminar_producto, name='eliminarProducto'),
    url(r'^obtenerProductos/$', producto.obtener_productos, name='obtenerProductos'),
    url(r'^obtenerProductoId/(?P<id_producto>[0-9]+)/$', producto.obtener_producto_id, name='obtenerProductoId'),
    url(r'^obtenerProductoCategoria/(?P<id_categoria>[0-9]+)/$', producto.obtener_productos_categoriaid, name='obtenerProductoCategoria'),
    url(r'^obtenerProductoNoCategoria/(?P<id_categoria>[0-9]+)/$', producto.obtener_productos_no_categoriaid, name='obtenerProductoNoCategoria'),
    url(r'^asignarProductoCategoria/$', producto.asginar_producto_categoria, name='asignarProductoCategoria'),
    url(r'^obtenerProductoSubCategoria/(?P<id_subcategoria>[0-9]+)/$', producto.obtener_productos_subcategoriaid, name='obtenerProductoSubCategoria'),
    url(r'^obtenerProductoNoSubCategoria/(?P<id_subcategoria>[0-9]+)/$', producto.obtener_productos_no_subcategoriaid, name='obtenerProductoNoSubCategoria'),
    url(r'^asignarProductoSubCategoria/$', producto.asiginar_producto_subcategoria, name='asignarProductoSubCategoria'),


    #UNIDAD_MEDIDA
    url(r'^obtenerUnidadMedida/$', unidad_medida.obtener_unidad_medida, name='obtenerUnidadMedida'),
    url(r'^obtenerUnidadMedidaId/(?P<id_unidad_medida>[0-9]+)/$', unidad_medida.obtener_unidad_medida_id, name='obtenerUnidadMedidaId'),

    #COMBO
    url(r'^registrarCombo/$', combo.registrar_combo, name='registrarCombo'),
    url(r'^eliminarCombo/$', combo.eliminar_combo, name='eliminarCombo'),
    url(r'^modificarCombo/$', combo.modificar_combo, name='modificarCombo'),
    url(r'^obtenerComboId/(?P<id_combo>[0-9]+)/$', combo.obtener_combo_id, name='obtenerComboId'),
    url(r'^obtenerCombosVigentes/$', combo.obtener_combos_vigentes, name='obtenerCombosVigentes'),
    url(r'^actualizarPrecioCombo/$', combo.actualizar_precio_combo, name='actualizarPrecioCombo'),

    #LISTA_PRECIO
    url(r'^registrarListaPrecio/$', lista_precio.registrar_lista_precio, name='registrarListaPrecio'),
    url(r'^eliminarListaPrecio/$', lista_precio.eliminar_lista_precio, name='eliminarListaPrecio'),
    url(r'^obtenerListaPrecioVigente/$', lista_precio.obtener_lista_precio, name='obtenerListaPrecioVigente'),
    url(r'^obtenerProductosNoListaVigente/$', lista_precio.obtener_productos_no_lista_precio, name='obtenerProductosNoListaVigente'),

    # COMPRA
    url(r'^obtenerCompras/$', compra.obtener_compras, name='obtenerCompras'),
    url(r'^obtenerCompraId/(?P<id_compra>[0-9]+)/$', compra.obtener_compra_id, name='obtenerCompraId'),
    url(r'^registrarCompra/$', compra.registrar_compra, name='registrarCompra'),
    url(r'^cancelarCompra/$', compra.cancelar_compra, name='cancelarCompra'),
    url(r'^pagarCompra/$', compra.pagar_compra, name='pagarCompra'),
    url(r'^cambiarEstadoCompra/$', compra.cambiar_estado_compra, name='cambiarEstadoCompra'),
    url(r'^generarMovimientoSalidaCapitalStock/$', compra.generar_movimiento_capital_compra_movimiento_stock, name='generarMovimientoSalidaCapitalStock'),

    #RETIRO
    url(r'^obtenerRetiros/$', retiro.obtener_retiros, name='obtenerRetiros'),
    url(r'^obtenerRetiroId/(?P<id_retiro>[0-9]+)/$', retiro.obtener_retiro_id, name='obtenerRetiroId'),
    url(r'^generarRetiroCapital/$', retiro.generar_retiro_capital, name='generarRetiroCapital'),
    url(r'^cancelarRetiroCapital/$', retiro.cancelar_retiro_capital, name='cancelarRetiroCapital'),


    #VENTA
    url(r'^obtenerVentas/$', ventas.obtener_ventas, name='obtenerVentas'),
    url(r'^obtenerVentaId/(?P<id_venta>[0-9]+)/$', ventas.obtener_venta_id, name='obtenerVentaId'),
    url(r'^registrarVenta/$', ventas.registrar_venta, name='registrarVenta'),
    url(r'^cancelarVenta/$', ventas.cancelar_venta, name='cancelarVenta'),
    url(r'^cobrarVenta/$', ventas.cobrar_venta, name='cobrarVenta'),
    url(r'^cambiarEstadoVenta/$', ventas.cambiar_estado_venta, name='cambiarEstadoVenta'),
    url(r'^generarMovimientoEntradaCapitalStock/$', ventas.generar_movimiento_capital_venta_movimiento_stock, name='generarMovimientoEntradaCapitalStock'),


    #CAJA
    url(r'^abrirCaja/$', caja.abrir_caja, name='abrirCaja'),
    url(r'^cerrarCaja/$', caja.cerrar_caja, name='cerrarCaja'),
    url(r'^obtenerCaja/$', caja.obtener_ultima_caja, name='obtenerCaja'),
    url(r'^generarDetalleCaja/$', caja.generar_detalle_caja, name='generarDetalleCaja'),

    # MOVIMIENTO_STOCK_REMITO
    url(r'^obtenerRemitos/$', remito.obtener_remitos, name='obtenerRemitos'),
    url(r'^obtenerRemitoId/(?P<id_remito>[0-9]+)/$', remito.obtener_remito_id, name='obtenerRemitoId'),
    url(r'^registrarRemito/$', remito.registrar_remito, name='registrarRemito'),
    url(r'^cancelarRemito/$', remito.cancelar_remito, name='cancelarRemito'),

    # SORTEO
    url(r'^registrarSorteo/$', sorteo.registrar_sorteo, name='registrarSorteo'),
    url(r'^obtenerSorteos/$', sorteo.obtener_sorteos, name='obtenerSorteos'),
    url(r'^obtenerSorteoId/(?P<id_sorteo>[0-9]+)/$', sorteo.obtener_sorteo_id, name='obtenerSorteoId'),

    # REPORTES
    url(r'^obtenerReporteStockMinimo/$', reporte.obtener_reporte_stock_minimo, name='obtenerReporteStockMinimo'),
    url(r'^obtenerReporteComprasVentas/$', reporte.obtener_reporte_compras_ventas, name='obtenerReporteComprasVentas'),
    url(r'^obtenerReporteGananciaProducto/$', reporte.obtener_reporte_ganancia_producto, name='obtenerReporteGananciaProducto'),
]
