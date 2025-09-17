"""
Script de migración para cambiar del almacenamiento JSON a PostgreSQL
"""
import os
import sys
import json
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.create_ventas_table import create_ventas_table, migrate_existing_data
from services.ventas_service_db import VentasServiceDB
from services.ventas_service import get_all_ventas as get_ventas_json

def backup_json_data():
    """Crea una copia de seguridad de los datos JSON existentes"""
    ventas_file = os.path.join('data', 'ventas.json')
    backup_file = os.path.join('data', f'ventas_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    if os.path.exists(ventas_file):
        try:
            with open(ventas_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"✓ Copia de seguridad creada: {backup_file}")
            return True
        except Exception as e:
            print(f"Error al crear copia de seguridad: {e}")
            return False
    return True

def verify_migration():
    """Verifica que la migración se haya realizado correctamente"""
    print("\n=== Verificando migración ===")
    
    # Obtener datos del JSON
    ventas_json = get_ventas_json()
    print(f"Datos en JSON: {len(ventas_json)} ventas")
    
    # Obtener datos de la base de datos
    ventas_service = VentasServiceDB()
    ventas_db = ventas_service.get_all_ventas()
    print(f"Datos en DB: {len(ventas_db)} ventas")
    
    # Comparar totales
    total_json = sum(v.valor_venta for v in ventas_json)
    total_db = sum(v.valor_venta for v in ventas_db)
    
    print(f"Total ventas JSON: ${total_json:,.2f}")
    print(f"Total ventas DB: ${total_db:,.2f}")
    
    if abs(total_json - total_db) < 0.01:  # Tolerancia para decimales
        print("✓ Migración verificada exitosamente")
        return True
    else:
        print("✗ Error en la verificación de migración")
        return False

def update_imports():
    """Actualiza los archivos que importan el servicio de ventas"""
    print("\n=== Actualizando imports ===")
    
    # Archivos que probablemente importan el servicio de ventas
    files_to_update = [
        'main.py',
        'views/menu_view.py'
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Reemplazar import del servicio de ventas
                old_import = "from services.ventas_service import"
                new_import = "from services.ventas_service_db import"
                
                if old_import in content:
                    content = content.replace(old_import, new_import)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✓ Actualizado: {file_path}")
                else:
                    print(f"- Sin cambios necesarios: {file_path}")
                    
            except Exception as e:
                print(f"Error al actualizar {file_path}: {e}")

def main():
    """Función principal de migración"""
    print("=== MIGRACIÓN A POSTGRESQL ===")
    print("Este script migrará el sistema de ventas de JSON a PostgreSQL")
    print()
    
    # Confirmar con el usuario
    response = input("¿Desea continuar con la migración? (s/n): ").lower()
    if response != 's':
        print("Migración cancelada")
        return
    
    print("\n1. Creando copia de seguridad...")
    if not backup_json_data():
        print("Error al crear copia de seguridad. Abortando migración.")
        return
    
    print("\n2. Creando tabla de ventas...")
    if not create_ventas_table():
        print("Error al crear tabla. Abortando migración.")
        return
    
    print("\n3. Migrando datos existentes...")
    if not migrate_existing_data():
        print("Error al migrar datos. Abortando migración.")
        return
    
    print("\n4. Verificando migración...")
    if not verify_migration():
        print("Error en la verificación. Revise los datos.")
        return
    
    print("\n5. Actualizando imports...")
    update_imports()
    
    print("\n=== MIGRACIÓN COMPLETADA ===")
    print("✓ El sistema ahora usa PostgreSQL para almacenar ventas")
    print("✓ Los datos existentes han sido migrados")
    print("✓ Se ha creado una copia de seguridad de los datos JSON")
    print("\nPuede eliminar el archivo ventas.json después de verificar que todo funciona correctamente.")
    
    # Mostrar estadísticas finales
    ventas_service = VentasServiceDB()
    stats = ventas_service.get_ventas_stats()
    
    if stats:
        print(f"\n=== ESTADÍSTICAS FINALES ===")
        print(f"Total de ventas: {stats['total_ventas']}")
        print(f"Valor total: ${stats['total_valor']:,.2f}")
        print(f"Promedio por venta: ${stats['promedio_venta']:,.2f}")
        print(f"Primera venta: {stats['primera_venta']}")
        print(f"Última venta: {stats['ultima_venta']}")

if __name__ == "__main__":
    main()
