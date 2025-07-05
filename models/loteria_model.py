class Loteria:
    def __init__(self, id_loteria, nombre_loteria, fracciones_por_billete, valor_por_fraccion, cantidad_inventario_inicial_por_fracciones):        
        self.id_loteria = id_loteria
        self.nombre_loteria = nombre_loteria
        self.fracciones_por_billete = fracciones_por_billete
        self.valor_por_fraccion = valor_por_fraccion
        self.cantidad_inventario_inicial_por_fracciones = cantidad_inventario_inicial_por_fracciones
        self.cantidad_billetes_iniciales = 0
        self.valor_total_inventario_inicial = 0
        self.valor_por_billete_iniciales = 0
        self._actualizar_calculos() # Llama a los cálculos al inicializar

    def _actualizar_calculos(self):
        """Calcula y actualiza los valores derivados de la lotería."""
        self.cantidad_billetes_iniciales = self.cantidad_inventario_inicial_por_fracciones // self.fracciones_por_billete
        self.valor_total_inventario_inicial = self.cantidad_inventario_inicial_por_fracciones * self.valor_por_fraccion
        self.valor_por_billete_iniciales = self.valor_por_fraccion * self.fracciones_por_billete

    def to_dict(self):
        """Convierte la instancia de Loteria a un diccionario."""
        return {
            "id_loteria": self.id_loteria,
            "nombre_loteria": self.nombre_loteria,
            "fracciones_por_billete": self.fracciones_por_billete,
            "valor_por_fraccion": self.valor_por_fraccion,
            "cantidad_inventario_inicial_por_fracciones": self.cantidad_inventario_inicial_por_fracciones,
            "cantidad_billetes_iniciales": self.cantidad_billetes_iniciales,
            "valor_total_inventario_inicial": self.valor_total_inventario_inicial,
            "valor_por_billete_iniciales": self.valor_por_billete_iniciales
        }

    def set_valor_por_fraccion(self, nuevo_valor):
        if nuevo_valor > 0:
            self.valor_por_fraccion = nuevo_valor
            self._actualizar_calculos()
            return True
        return False

    def set_cantidad_inventario(self, nueva_cantidad):
        if nueva_cantidad >= 0:
            self.cantidad_inventario_inicial_por_fracciones = nueva_cantidad
            self._actualizar_calculos()
            return True
        return False