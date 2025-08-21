from datetime import datetime
from services.loteria_service import get_all_loterias

class Ventas:
    def __init__(self, id_venta, id_loteria, cantidad_fracciones_vendidas, nombre_cliente, nombre_vendedor, fecha_venta, valor_venta):        
        self.id_venta = id_venta
        self.id_loteria = id_loteria
        self.cantidad_fracciones_vendidas = cantidad_fracciones_vendidas
        self.nombre_cliente = nombre_cliente
        self.nombre_vendedor = nombre_vendedor
        self.fecha_venta = fecha_venta
        self.valor_venta = valor_venta
        self._actualizar_calculos() # Llama a los cálculos al inicializar

    def _actualizar_calculos(self):
        """Calcula y actualiza los valores derivados de la venta."""
        # Buscar la lotería por id_loteria
        loterias = get_all_loterias()
        loteria_encontrada = None
        
        for loteria in loterias:
            if loteria.id_loteria == self.id_loteria:
                loteria_encontrada = loteria
                break
        
        if loteria_encontrada:
            # Calcular el valor de venta basado en el valor por fracción de la lotería
            self.valor_venta = self.cantidad_fracciones_vendidas * loteria_encontrada.valor_por_fraccion
        else:
            # Si no se encuentra la lotería, mantener el valor actual o establecer en 0
            print(f"Advertencia: No se encontró la lotería con ID {self.id_loteria}")
            if not hasattr(self, 'valor_venta') or self.valor_venta is None:
                self.valor_venta = 0

    def to_dict(self):
        """Convierte la instancia de Ventas a un diccionario."""
        return {
            "id_venta": self.id_venta,
            "id_loteria": self.id_loteria,
            "cantidad_fracciones_vendidas": self.cantidad_fracciones_vendidas,
            "nombre_cliente": self.nombre_cliente,
            "nombre_vendedor": self.nombre_vendedor,
            "fecha_venta": self.fecha_venta,
            "valor_venta": self.valor_venta
        }

    def set_valor_venta(self, nuevo_valor):
        if nuevo_valor > 0:
            self.valor_venta = nuevo_valor
            return True
        return False