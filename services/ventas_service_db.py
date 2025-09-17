"""
Servicio de ventas que utiliza PostgreSQL como almacenamiento
"""
import psycopg2
from datetime import datetime, date
from decimal import Decimal
from models.venta_model import Ventas
from data.db_postgreSQL import get_connection, close_connection
from services.loteria_service import get_all_loterias

class VentasServiceDB:
    """Servicio para manejar operaciones de ventas con PostgreSQL"""
    
    def __init__(self):
        self.connection = None
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        if not self.connection or self.connection.closed:
            self.connection = get_connection()
        return self.connection
    
    def _close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self.connection and not self.connection.closed:
            close_connection(self.connection)
            self.connection = None
    
    def get_all_ventas(self):
        """Retorna todas las ventas como objetos Ventas."""
        connection = self._get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_venta, id_loteria, cantidad_fracciones_vendidas, 
                       nombre_cliente, nombre_vendedor, fecha_venta, valor_venta,
                       created_at, updated_at
                FROM ventas 
                ORDER BY fecha_venta DESC, id_venta DESC
            """)
            
            rows = cursor.fetchall()
            ventas = []
            for row in rows:
                venta = Ventas.from_db_row(row)
                ventas.append(venta)
            
            return ventas
            
        except psycopg2.Error as e:
            print(f"Error al obtener ventas: {e}")
            return []
        finally:
            cursor.close()
    
    def find_venta_by_id(self, id_venta):
        """Encuentra una venta por su ID."""
        connection = self._get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_venta, id_loteria, cantidad_fracciones_vendidas, 
                       nombre_cliente, nombre_vendedor, fecha_venta, valor_venta,
                       created_at, updated_at
                FROM ventas 
                WHERE id_venta = %s
            """, (id_venta,))
            
            row = cursor.fetchone()
            if row:
                return Ventas.from_db_row(row)
            return None
            
        except psycopg2.Error as e:
            print(f"Error al buscar venta por ID: {e}")
            return None
        finally:
            cursor.close()
    
    def find_ventas_by_loteria(self, id_loteria):
        """Encuentra todas las ventas de una lotería específica."""
        connection = self._get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_venta, id_loteria, cantidad_fracciones_vendidas, 
                       nombre_cliente, nombre_vendedor, fecha_venta, valor_venta,
                       created_at, updated_at
                FROM ventas 
                WHERE id_loteria = %s
                ORDER BY fecha_venta DESC, id_venta DESC
            """, (id_loteria,))
            
            rows = cursor.fetchall()
            ventas = []
            for row in rows:
                venta = Ventas.from_db_row(row)
                ventas.append(venta)
            
            return ventas
            
        except psycopg2.Error as e:
            print(f"Error al buscar ventas por lotería: {e}")
            return []
        finally:
            cursor.close()
    
    def add_new_venta(self, id_loteria, cantidad_fracciones_vendidas, nombre_cliente, nombre_vendedor, fecha_venta=None):
        """Agrega una nueva venta a la base de datos."""
        if fecha_venta is None:
            fecha_venta = datetime.now().date()
        
        # Calcular el valor de venta basado en la lotería
        loterias = get_all_loterias()
        loteria_encontrada = None
        
        for loteria in loterias:
            if loteria.id_loteria == id_loteria:
                loteria_encontrada = loteria
                break
        
        if not loteria_encontrada:
            print(f"Error: No se encontró la lotería con ID {id_loteria}")
            return None
        
        valor_venta = cantidad_fracciones_vendidas * loteria_encontrada.valor_por_fraccion
        
        connection = self._get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO ventas (id_loteria, cantidad_fracciones_vendidas, 
                                  nombre_cliente, nombre_vendedor, fecha_venta, valor_venta)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_venta, created_at, updated_at
            """, (id_loteria, cantidad_fracciones_vendidas, nombre_cliente, 
                  nombre_vendedor, fecha_venta, valor_venta))
            
            result = cursor.fetchone()
            connection.commit()
            
            # Crear el objeto Ventas con los datos insertados
            nueva_venta = Ventas(
                id_venta=result[0],
                id_loteria=id_loteria,
                cantidad_fracciones_vendidas=cantidad_fracciones_vendidas,
                nombre_cliente=nombre_cliente,
                nombre_vendedor=nombre_vendedor,
                fecha_venta=fecha_venta,
                valor_venta=valor_venta,
                created_at=result[1],
                updated_at=result[2]
            )
            
            print(f"Venta agregada exitosamente con ID: {nueva_venta.id_venta}")
            return nueva_venta
            
        except psycopg2.Error as e:
            print(f"Error al agregar venta: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
    
    def update_venta(self, id_venta, **kwargs):
        """Actualiza una venta existente."""
        connection = self._get_connection()
        if not connection:
            return False
        
        # Construir la consulta dinámicamente
        set_clauses = []
        values = []
        
        allowed_fields = ['id_loteria', 'cantidad_fracciones_vendidas', 'nombre_cliente', 
                         'nombre_vendedor', 'fecha_venta', 'valor_venta']
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                set_clauses.append(f"{field} = %s")
                values.append(value)
        
        if not set_clauses:
            print("No hay campos válidos para actualizar")
            return False
        
        values.append(id_venta)
        
        try:
            cursor = connection.cursor()
            cursor.execute(f"""
                UPDATE ventas 
                SET {', '.join(set_clauses)}
                WHERE id_venta = %s
            """, values)
            
            if cursor.rowcount > 0:
                connection.commit()
                print(f"Venta {id_venta} actualizada exitosamente")
                return True
            else:
                print(f"No se encontró la venta con ID {id_venta}")
                return False
                
        except psycopg2.Error as e:
            print(f"Error al actualizar venta: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
    
    def delete_venta(self, id_venta):
        """Elimina una venta de la base de datos."""
        connection = self._get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
            
            if cursor.rowcount > 0:
                connection.commit()
                print(f"Venta {id_venta} eliminada exitosamente")
                return True
            else:
                print(f"No se encontró la venta con ID {id_venta}")
                return False
                
        except psycopg2.Error as e:
            print(f"Error al eliminar venta: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
    
    def get_ventas_by_date_range(self, fecha_inicio, fecha_fin):
        """Obtiene ventas en un rango de fechas."""
        connection = self._get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_venta, id_loteria, cantidad_fracciones_vendidas, 
                       nombre_cliente, nombre_vendedor, fecha_venta, valor_venta,
                       created_at, updated_at
                FROM ventas 
                WHERE fecha_venta BETWEEN %s AND %s
                ORDER BY fecha_venta DESC, id_venta DESC
            """, (fecha_inicio, fecha_fin))
            
            rows = cursor.fetchall()
            ventas = []
            for row in rows:
                venta = Ventas.from_db_row(row)
                ventas.append(venta)
            
            return ventas
            
        except psycopg2.Error as e:
            print(f"Error al obtener ventas por rango de fechas: {e}")
            return []
        finally:
            cursor.close()
    
    def calculate_total_ventas(self):
        """Calcula el total de todas las ventas."""
        connection = self._get_connection()
        if not connection:
            return 0
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT SUM(valor_venta) FROM ventas")
            result = cursor.fetchone()
            return float(result[0]) if result[0] else 0
            
        except psycopg2.Error as e:
            print(f"Error al calcular total de ventas: {e}")
            return 0
        finally:
            cursor.close()
    
    def calculate_ventas_por_loteria(self):
        """Calcula el total de ventas por lotería."""
        connection = self._get_connection()
        if not connection:
            return {}
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_loteria, SUM(valor_venta) 
                FROM ventas 
                GROUP BY id_loteria
                ORDER BY id_loteria
            """)
            
            rows = cursor.fetchall()
            ventas_por_loteria = {}
            for row in rows:
                ventas_por_loteria[row[0]] = float(row[1])
            
            return ventas_por_loteria
            
        except psycopg2.Error as e:
            print(f"Error al calcular ventas por lotería: {e}")
            return {}
        finally:
            cursor.close()
    
    def get_ventas_stats(self):
        """Obtiene estadísticas generales de ventas."""
        connection = self._get_connection()
        if not connection:
            return {}
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_ventas,
                    SUM(valor_venta) as total_valor,
                    AVG(valor_venta) as promedio_venta,
                    MIN(fecha_venta) as primera_venta,
                    MAX(fecha_venta) as ultima_venta
                FROM ventas
            """)
            
            result = cursor.fetchone()
            if result:
                return {
                    'total_ventas': result[0],
                    'total_valor': float(result[1]) if result[1] else 0,
                    'promedio_venta': float(result[2]) if result[2] else 0,
                    'primera_venta': result[3],
                    'ultima_venta': result[4]
                }
            return {}
            
        except psycopg2.Error as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}
        finally:
            cursor.close()

# Instancia global del servicio
ventas_service = VentasServiceDB()

# Funciones de conveniencia para mantener compatibilidad
def get_all_ventas():
    return ventas_service.get_all_ventas()

def find_venta_by_id(id_venta):
    return ventas_service.find_venta_by_id(id_venta)

def find_ventas_by_loteria(id_loteria):
    return ventas_service.find_ventas_by_loteria(id_loteria)

def add_new_venta(id_loteria, cantidad_fracciones_vendidas, nombre_cliente, nombre_vendedor, fecha_venta=None):
    return ventas_service.add_new_venta(id_loteria, cantidad_fracciones_vendidas, nombre_cliente, nombre_vendedor, fecha_venta)

def get_ventas_by_date_range(fecha_inicio, fecha_fin):
    return ventas_service.get_ventas_by_date_range(fecha_inicio, fecha_fin)

def calculate_total_ventas():
    return ventas_service.calculate_total_ventas()

def calculate_ventas_por_loteria():
    return ventas_service.calculate_ventas_por_loteria()

def get_ventas_stats():
    return ventas_service.get_ventas_stats()

