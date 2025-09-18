from data.db_postgreSQL import get_connection

def crear_tabla_loterias():
 conn = get_connection()
 if conn:
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS loterias (
            id_loteria SERIAL PRIMARY KEY,
            nombre_loteria VARCHAR(255) NOT NULL,
            fracciones_por_billete INTEGER NOT NULL,
            valor_por_fraccion DECIMAL(10, 2) NOT NULL,
            cantidad_inventario_inicial_por_fracciones INTEGER NOT NULL,
            cantidad_billetes_iniciales INTEGER NOT NULL,
            valor_total_inventario_inicial DECIMAL(10, 2) NOT NULL,
            valor_por_billete_iniciales DECIMAL(10, 2) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        print("Tabla loterias creada exitosamente")
    except Exception as e:
        print(f"Error al crear la tabla loterias: {e}")
    finally:
        conn.close()
        print("Conexión cerrada exitosamente")

def insertar_loteria(loteria):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO loterias (nombre_loteria, fracciones_por_billete, valor_por_fraccion, cantidad_inventario_inicial_por_fracciones, cantidad_billetes_iniciales, valor_total_inventario_inicial, valor_por_billete_iniciales)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (loteria.nombre_loteria, loteria.fracciones_por_billete, loteria.valor_por_fraccion, loteria.cantidad_inventario_inicial_por_fracciones, loteria.cantidad_billetes_iniciales, loteria.valor_total_inventario_inicial, loteria.valor_por_billete_iniciales))
            
            conn.commit()
            cur.close()
            print("Loteria insertada exitosamente")
        except Exception as e:
            print(f"Error al insertar la loteria: {e}")
        finally:
            conn.close()
            print("Conexión cerrada exitosamente")

def obtener_loterias():
 conn = get_connection()
 if conn:
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM loterias;")
        loterias = cur.fetchall()
        cur.close()
        return loterias
    except Exception as e:
       print(f"Error al obtener loterías: {e}")
    finally:
        conn.close()
    return []