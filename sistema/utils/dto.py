class DTOListaCombo:
    def __init__(self, dto_combo, dto_detalle):
        self.dto_combo = dto_combo
        self.dto_detalle = dto_detalle

    def as_json(self):
        return dict(
            combo_cabecera= self.dto_combo.as_json(),
            combo_detalles= [detalle.as_json() for
                             detalle in self.dto_detalle]
        )

class DTOCombo:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    def as_json(self):
        return dict(
            codigo=self.codigo,
            nombre=self.nombre,
            precio=self.precio
        )

class DTOComboDetalle:
    def __init__(self, codigo_producto, nombre_producto, marca_producto, nombre_medida, medida, precio_unitario, margen_ganancia, cantidad,subtotal):
        self.codigo = codigo_producto
        self.nombre = nombre_producto
        self.marca = marca_producto
        self.nombre_medida = nombre_medida
        self.medida = medida
        self.precio = precio_unitario
        self.margen_ganancia = margen_ganancia
        self.cantidad = cantidad
        self.subtotal = subtotal

    def as_json(self):
        return dict(
            codigo_producto=self.codigo,
            nombre_producto=self.nombre,
            marca_producto = self.marca,
            medida = self.medida,
            nombre_medida = self.nombre_medida,
            precio_producto=self.precio,
            margen_ganancia = self.margen_ganancia,
            cantidad = self.cantidad,
            subtotal = self.subtotal
        )

class DTOListaMovimientoStock:
    def __init__(self, dto_movimiento_stock, dto_detalle):
        self.dto_movimiento_stock = dto_movimiento_stock
        self.dto_detalle = dto_detalle

    def as_json(self):
        return dict(
            movimiento_cabecera= self.dto_movimiento_stock.as_json(),
            movimiento_detalles= [detalle.as_json() for
                             detalle in self.dto_detalle]
        )

class DTOCabeceraMovimientoStock:
    def __init__(self, codigo, fecha_creacion, total_parcial, descuento, total_final, usuario, estado, tipo_movimiento):
        self.codigo = codigo
        self.fecha_creacion = fecha_creacion
        self.total_parcial = total_parcial
        self.descuento = descuento
        self.total_final = total_final
        self.usuario = usuario
        self.estado = estado
        self.tipo_movimiento = tipo_movimiento

    def as_json(self):
        return dict(
            codigo=self.codigo,
            fecha_creacion=self.fecha_creacion,
            total_parcial = self.total_parcial,
            descuento = self.descuento,
            total_final = self.total_final,
            usuario = self.usuario,
            estado = self.estado,
            tipo_movimiento = self.tipo_movimiento
        )

class DTOMovimientoStockDetalle:
    def __init__(self, codigo_producto, nombre_producto, marca_producto, nombre_medida, medida, precio_unitario, subtotal, cantidad):
        self.codigo = codigo_producto
        self.nombre = nombre_producto
        self.marca = marca_producto
        self.nombre_medida = nombre_medida
        self.medida = medida
        self.precio = precio_unitario
        self.subtotal = subtotal
        self.cantidad = cantidad

    def as_json(self):
        return dict(
            codigo_producto=self.codigo,
            nombre_producto=self.nombre,
            marca_producto=self.marca,
            medida=self.medida,
            nombre_medida=self.nombre_medida,
            precio_unitario = self.precio,
            subtotal = self.subtotal,
            cantidad = self.cantidad
        )

class DTOMovimientoCapital:
    def __init__(self,codigo, total, fecha_creacion, descripcion, nombre_tipo_movimiento, estado, codigo_movimiento_stock, nombre_forma_pago,usuario):
        self.codigo = codigo
        self.total = total
        self.fecha_creacion = fecha_creacion
        self.descripcion = descripcion
        self.nombre_tipo_movimiento = nombre_tipo_movimiento
        self.estado = estado
        self.codigo_movimiento_stock = codigo_movimiento_stock
        self.nombre_forma_pago = nombre_forma_pago
        self.usuario = usuario

    def as_json(self):
        return dict(
            codigo = self.codigo,
            total = self.total,
            fecha_creacion = self.fecha_creacion,
            descripcion = self.descripcion,
            nombre_tipo_movimiento = self.nombre_tipo_movimiento,
            estado = self.estado,
            codigo_movimiento_stock = self.codigo_movimiento_stock,
            nombre_forma_pago = self.nombre_forma_pago,
            usuario = self.usuario
        )


class DTOCaja:

    def __init__(self,dto_cabecera,dto_detalles):
        self.dto_cabecera = dto_cabecera
        self.dto_detalles = dto_detalles

    def as_json(self):
        return dict(
            caja_cabecera=self.dto_cabecera.as_json(),
            caja_detalles=[detalle.as_json() for
                           detalle in self.dto_detalles]
        )

class DTOCajaCabecera:
    def __init__(self, fecha_apertura, fecha_cierre, total_apertura, total_cierre, estado):
        self.fecha_apertura = fecha_apertura
        self.fecha_cierre = fecha_cierre
        self.total_apertura = total_apertura
        self.total_cierre = total_cierre
        self.estado = estado

    def as_json(self):
        return dict(
            fecha_apertura = self.fecha_apertura,
            fecha_cierre = self.fecha_cierre,
            total_apertura = self.total_apertura,
            total_cierre = self.total_cierre,
            estado = self.estado
        )

class DTOCajaDetalle:
    def __init__(self,fecha_creacion,total,tipo_movimiento,detalle):
        self.fecha_creacion = fecha_creacion
        self.total = total
        self.tipo_movimiento = tipo_movimiento
        self.detalle = detalle

    def as_json(self):
        return dict(
            fecha_creacion = self.fecha_creacion,
            total = self.total,
            tipo_movimiento = self.tipo_movimiento,
            detalle = self.detalle
        )

class DTOListaPrecio:

    def __init__(self,dto_cabecera,dto_detalles):
        self.dto_cabecera = dto_cabecera
        self.dto_detalles = dto_detalles

    def as_json(self):
        return dict(
            lista_precio_cabecera=self.dto_cabecera.as_json(),
            lista_precio_detalles=[detalle.as_json() for
                           detalle in self.dto_detalles]
        )

class DTOListaPrecioCabecera:
    def __init__(self, codigo, nombre, vigencia_desde, vigencia_hasta, estado):
        self.codigo = codigo
        self.nombre = nombre
        self.vigencia_desde = vigencia_desde
        self.vigencia_hasta = vigencia_hasta
        self.estado = estado


    def as_json(self):
        return dict(
            codigo = self.codigo,
            nombre = self.nombre,
            vigencia_desde = self.vigencia_desde,
            vigencia_hasta = self.vigencia_hasta,
            estado = self.estado
        )

class DTOListaPrecioDetalle:
    def __init__(self,codigo,nombre,marca,medida,nombre_medida,precio_compra,precio_venta,stock_deposito,stock_minimo,stock_local):
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.medida = medida
        self.nombre_medida = nombre_medida
        self.precio_venta = round(precio_venta,2)
        self.precio_compra = round(precio_compra,2)
        self.margen_ganancia = round(((precio_venta / precio_compra) - 1),2) * 100
        self.ganancia = precio_venta - precio_compra
        self.stock_deposito = stock_deposito
        self.stock_minimo = stock_minimo
        self.stock_local = stock_local

    def as_json(self):
        return dict(
            codigo_producto=self.codigo,
            nombre_producto=self.nombre,
            marca_producto=self.marca,
            medida=self.medida,
            nombre_medida=self.nombre_medida,
            precio_compra=self.precio_compra,
            precio_venta=self.precio_venta,
            margen_ganancia=self.margen_ganancia,
            ganancia=self.ganancia,
            stock_deposito = self.stock_deposito,
            stock_minimo = self.stock_minimo,
            stock_local = self.stock_local
        )

class DTOProducto:
    def __init__(self,codigo,nombre,marca,medida,nombre_medida,stock_local,stock_deposito,stock_minimo,estado):
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.medida = medida
        self.nombre_medida = nombre_medida
        self.stock_local = stock_local
        self.stock_deposito = stock_deposito
        self.stock_minimo = stock_minimo
        self.estado = estado

    def as_json(self):
        return dict(
            codigo_producto=self.codigo,
            nombre_producto=self.nombre,
            marca_producto=self.marca,
            medida=self.medida,
            nombre_medida=self.nombre_medida,
            stock_local=self.stock_local,
            stock_deposito=self.stock_deposito,
            stock_minimo=self.stock_minimo,
            estado=self.estado
        )

class DTOCliente:
    def __init__(self, codigo,nombre,apellido,dni,telefono,direccion,tipo_cliente,estado):
        self.codigo = codigo
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.direccion = direccion
        self.tipo_cliente = tipo_cliente
        self.estado = estado

    def as_json(self):
        return dict(
            codigo = self.codigo,
            nombre = self.nombre,
            apellido = self.apellido,
            dni = self.dni,
            telefono = self.telefono,
            direccion = self.direccion,
            tipo_cliente = self.tipo_cliente,
            estado = self.estado
        )