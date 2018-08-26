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
    def __init__(self, codigo_producto, nombre_producto, marca_producto, nombre_medida, medida, precio_unitario, margen_ganancia, cantidad):
        self.codigo = codigo_producto
        self.nombre = nombre_producto
        self.marca = marca_producto
        self.nombre_medida = nombre_medida
        self.medida = medida
        self.precio = precio_unitario
        self.margen_ganancia = margen_ganancia
        self.cantidad = cantidad

    def as_json(self):
        return dict(
            codigo_producto=self.codigo,
            nombre_producto=self.nombre,
            marca_producto = self.marca,
            medida = self.medida,
            nombre_medida = self.nombre_medida,
            precio_producto=self.precio,
            margen_ganancia = self.margen_ganancia,
            cantidad = self.cantidad
        )

class DTOListaMovimientoStock:
    def __init__(self, dto_movimiento_stock, dto_detalle):
        self.dto_movimiento_stock = dto_movimiento_stock
        self.dto_detalle = dto_detalle

    def as_json(self):
        return dict(
            combo_cabecera= self.dto_movimiento_stock.as_json(),
            combo_detalles= [detalle.as_json() for
                             detalle in self.dto_detalle]
        )


class DTOMovimientoStock:
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

class DTOCaja:
    def __init__(self,dto_cabecera,*dto_detalles):
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