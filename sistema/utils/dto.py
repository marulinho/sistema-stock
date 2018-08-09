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
    def __init__(self, codigo_producto, nombre_producto, nombre_medida, medida, precio_unitario, margen_ganancia, cantidad):
        self.codigo = codigo_producto
        self.nombre = nombre_producto
        self.nombre_medida = nombre_medida
        self.medida = medida
        self.precio = precio_unitario
        self.margen_ganancia = margen_ganancia
        self.cantidad = cantidad

    def as_json(self):
        return dict(
            codigo_producto=self.codigo,
            nombre_producto=self.nombre,
            medida = self.medida,
            nombre_medida = self.nombre_medida,
            precio_producto=self.precio,
            margen_ganancia = self.margen_ganancia,
            cantidad = self.cantidad
        )