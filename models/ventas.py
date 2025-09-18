from data.db_postgreSQL import get_connection

def crear_tabla_ventas():
    print("Creando tabla ventas")
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta SERIAL PRIMARY KEY,
                    id_loteria INTEGER NOT NULL,
                    cantidad_fracciones_vendidas INTEGER NOT NULL, 
                    nombre_cliente VARCHAR(255) NOT NULL,
                    nombre_vendedor VARCHAR(255) NOT NULL,
                    fecha_venta DATE NOT NULL,
                    valor_venta DECIMAL(10, 2) NOT NULL
                );
            """)
            conn.commit()
            cur.close()
            print("Tabla ventas creada exitosamente")
        except Exception as e:
            print(f"Error al crear la tabla ventas: {e}")
        finally:
            conn.close()
            print("Conexión cerrada exitosamente")

def insertar_venta(venta):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO ventas (id_loteria, cantidad_fracciones_vendidas, nombre_cliente, nombre_vendedor, fecha_venta, valor_venta) VALUES (%s, %s, %s, %s, %s, %s)", (venta.id_loteria, venta.cantidad_fracciones_vendidas, venta.nombre_cliente, venta.nombre_vendedor, venta.fecha_venta, venta.valor_venta))
            conn.commit()
            cur.close()
            print("Venta insertada exitosamente")
        except Exception as e:
            print(f"Error al insertar la venta: {e}")
            
def obtener_ventas():
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ventas")
            ventas = cur.fetchall()
            cur.close()
            return ventas
        except Exception as e:
            print(f"Error al obtener las ventas: {e}")
        finally:
            conn.close()
            print("Conexión cerrada exitosamente")

def eliminar_venta(id_venta):   
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
            conn.commit()
            cur.close()
            print("Venta eliminada exitosamente")
        except Exception as e:
            print(f"Error al eliminar la venta: {e}")
        finally:
            conn.close()
            print("Conexión cerrada exitosamente")