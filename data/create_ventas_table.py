"""
Script para crear la tabla de ventas en PostgreSQL
"""
import psycopg2
from config.database import DB_URI

def create_ventas_table():
    """Crea la tabla de ventas en la base de datos PostgreSQL"""
    
    # SQL para crear la tabla de ventas
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS ventas (
        id_venta SERIAL PRIMARY KEY,
        id_loteria INTEGER NOT NULL,
        cantidad_fracciones_vendidas INTEGER NOT NULL CHECK (cantidad_fracciones_vendidas > 0),
        nombre_cliente VARCHAR(100) NOT NULL,
        nombre_vendedor VARCHAR(100) NOT NULL,
        fecha_venta DATE NOT NULL DEFAULT CURRENT_DATE,
        valor_venta DECIMAL(10,2) NOT NULL DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # SQL para crear índices para mejorar el rendimiento
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_ventas_id_loteria ON ventas(id_loteria);",
        "CREATE INDEX IF NOT EXISTS idx_ventas_fecha_venta ON ventas(fecha_venta);",
        "CREATE INDEX IF NOT EXISTS idx_ventas_nombre_cliente ON ventas(nombre_cliente);",
        "CREATE INDEX IF NOT EXISTS idx_ventas_nombre_vendedor ON ventas(nombre_vendedor);"
    ]
    
    # SQL para crear un trigger que actualice updated_at automáticamente
    create_trigger_sql = """
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ language 'plpgsql';

    DROP TRIGGER IF EXISTS update_ventas_updated_at ON ventas;
    CREATE TRIGGER update_ventas_updated_at
        BEFORE UPDATE ON ventas
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """
    
    connection = None
    try:
        # Conectar a la base de datos
        connection = psycopg2.connect(DB_URI)
        cursor = connection.cursor()
        
        print("Conectado a la base de datos PostgreSQL...")
        
        # Crear la tabla
        cursor.execute(create_table_sql)
        print("✓ Tabla 'ventas' creada exitosamente")
        
        # Crear índices
        for index_sql in create_indexes_sql:
            cursor.execute(index_sql)
        print("✓ Índices creados exitosamente")
        
        # Crear trigger
        cursor.execute(create_trigger_sql)
        print("✓ Trigger de actualización creado exitosamente")
        
        # Confirmar los cambios
        connection.commit()
        print("✓ Todos los cambios confirmados en la base de datos")
        
    except psycopg2.Error as e:
        print(f"Error al crear la tabla de ventas: {e}")
        if connection:
            connection.rollback()
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Conexión cerrada")
    
    return True

def migrate_existing_data():
    """Migra los datos existentes del archivo JSON a la base de datos"""
    import json
    import os
    from datetime import datetime
    
    ventas_file = os.path.join(os.path.dirname(__file__), 'ventas.json')
    
    if not os.path.exists(ventas_file):
        print("No se encontró el archivo ventas.json para migrar")
        return True
    
    connection = None
    try:
        # Leer datos del archivo JSON
        with open(ventas_file, 'r', encoding='utf-8') as f:
            ventas_data = json.load(f)
        
        if not ventas_data:
            print("No hay datos para migrar")
            return True
        
        # Conectar a la base de datos
        connection = psycopg2.connect(DB_URI)
        cursor = connection.cursor()
        
        # Verificar si ya existen datos
        cursor.execute("SELECT COUNT(*) FROM ventas")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Ya existen {count} registros en la tabla ventas. ¿Desea continuar? (s/n): ", end="")
            response = input().lower()
            if response != 's':
                print("Migración cancelada")
                return True
        
        # Insertar datos
        insert_sql = """
        INSERT INTO ventas (id_venta, id_loteria, cantidad_fracciones_vendidas, 
                           nombre_cliente, nombre_vendedor, fecha_venta, valor_venta)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id_venta) DO NOTHING
        """
        
        for venta in ventas_data:
            # Convertir fecha si es string
            fecha_venta = venta['fecha_venta']
            if isinstance(fecha_venta, str):
                fecha_venta = datetime.strptime(fecha_venta, "%Y-%m-%d").date()
            
            cursor.execute(insert_sql, (
                venta['id_venta'],
                venta['id_loteria'],
                venta['cantidad_fracciones_vendidas'],
                venta['nombre_cliente'],
                venta['nombre_vendedor'],
                fecha_venta,
                venta['valor_venta']
            ))
        
        connection.commit()
        print(f"✓ {len(ventas_data)} registros migrados exitosamente")
        
    except Exception as e:
        print(f"Error al migrar datos: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return True

if __name__ == "__main__":
    print("=== Creación de tabla de ventas en PostgreSQL ===")
    
    # Crear la tabla
    if create_ventas_table():
        print("\n=== Migración de datos existentes ===")
        migrate_existing_data()
        print("\n✓ Proceso completado exitosamente")
    else:
        print("\n✗ Error en el proceso de creación de tabla")
