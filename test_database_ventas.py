"""
Script de prueba para verificar el funcionamiento del sistema de ventas con PostgreSQL
"""
import sys
import os
from datetime import datetime, date

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ventas_service_db import VentasServiceDB
from services.loteria_service import get_all_loterias

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("=== Probando conexión a la base de datos ===")
    
    ventas_service = VentasServiceDB()
    
    # Probar conexión obteniendo estadísticas
    stats = ventas_service.get_ventas_stats()
    if stats:
        print("✓ Conexión exitosa a la base de datos")
        print(f"  - Total ventas: {stats.get('total_ventas', 0)}")
        print(f"  - Valor total: ${stats.get('total_valor', 0):,.2f}")
        return True
    else:
        print("✗ Error al conectar con la base de datos")
        return False

def test_crud_operations():
    """Prueba las operaciones CRUD básicas"""
    print("\n=== Probando operaciones CRUD ===")
    
    ventas_service = VentasServiceDB()
    
    # Obtener loterías disponibles
    loterias = get_all_loterias()
    if not loterias:
        print("✗ No hay loterías disponibles para la prueba")
        return False
    
    id_loteria = loterias[0].id_loteria
    print(f"Usando lotería ID: {id_loteria}")
    
    # 1. Crear una nueva venta
    print("\n1. Creando nueva venta...")
    nueva_venta = ventas_service.add_new_venta(
        id_loteria=id_loteria,
        cantidad_fracciones_vendidas=2,
        nombre_cliente="Cliente Prueba",
        nombre_vendedor="Vendedor Prueba",
        fecha_venta=date.today()
    )
    
    if nueva_venta:
        print(f"✓ Venta creada con ID: {nueva_venta.id_venta}")
        venta_id = nueva_venta.id_venta
    else:
        print("✗ Error al crear venta")
        return False
    
    # 2. Leer la venta creada
    print("\n2. Leyendo venta creada...")
    venta_leida = ventas_service.find_venta_by_id(venta_id)
    if venta_leida:
        print(f"✓ Venta encontrada: {venta_leida.nombre_cliente} - ${venta_leida.valor_venta}")
    else:
        print("✗ Error al leer venta")
        return False
    
    # 3. Actualizar la venta
    print("\n3. Actualizando venta...")
    success = ventas_service.update_venta(
        venta_id,
        nombre_cliente="Cliente Actualizado",
        cantidad_fracciones_vendidas=3
    )
    
    if success:
        print("✓ Venta actualizada")
        
        # Verificar la actualización
        venta_actualizada = ventas_service.find_venta_by_id(venta_id)
        if venta_actualizada:
            print(f"  - Nuevo cliente: {venta_actualizada.nombre_cliente}")
            print(f"  - Nuevas fracciones: {venta_actualizada.cantidad_fracciones_vendidas}")
            print(f"  - Nuevo valor: ${venta_actualizada.valor_venta}")
    else:
        print("✗ Error al actualizar venta")
        return False
    
    # 4. Eliminar la venta de prueba
    print("\n4. Eliminando venta de prueba...")
    success = ventas_service.delete_venta(venta_id)
    if success:
        print("✓ Venta eliminada")
    else:
        print("✗ Error al eliminar venta")
        return False
    
    return True

def test_queries():
    """Prueba las consultas especializadas"""
    print("\n=== Probando consultas especializadas ===")
    
    ventas_service = VentasServiceDB()
    
    # Obtener todas las ventas
    print("\n1. Obteniendo todas las ventas...")
    todas_ventas = ventas_service.get_all_ventas()
    print(f"✓ Total de ventas: {len(todas_ventas)}")
    
    # Obtener ventas por lotería
    print("\n2. Obteniendo ventas por lotería...")
    loterias = get_all_loterias()
    if loterias:
        ventas_por_loteria = ventas_service.find_ventas_by_loteria(loterias[0].id_loteria)
        print(f"✓ Ventas para lotería {loterias[0].id_loteria}: {len(ventas_por_loteria)}")
    
    # Calcular totales
    print("\n3. Calculando totales...")
    total_ventas = ventas_service.calculate_total_ventas()
    print(f"✓ Total de ventas: ${total_ventas:,.2f}")
    
    ventas_por_loteria = ventas_service.calculate_ventas_por_loteria()
    print(f"✓ Ventas por lotería: {ventas_por_loteria}")
    
    # Consulta por rango de fechas
    print("\n4. Consultando por rango de fechas...")
    fecha_inicio = date(2025, 1, 1)
    fecha_fin = date(2025, 12, 31)
    ventas_rango = ventas_service.get_ventas_by_date_range(fecha_inicio, fecha_fin)
    print(f"✓ Ventas en rango {fecha_inicio} - {fecha_fin}: {len(ventas_rango)}")
    
    return True

def test_performance():
    """Prueba básica de rendimiento"""
    print("\n=== Probando rendimiento ===")
    
    ventas_service = VentasServiceDB()
    
    import time
    
    # Medir tiempo de consulta
    start_time = time.time()
    ventas = ventas_service.get_all_ventas()
    end_time = time.time()
    
    query_time = (end_time - start_time) * 1000  # Convertir a milisegundos
    print(f"✓ Tiempo de consulta: {query_time:.2f}ms para {len(ventas)} ventas")
    
    if query_time < 1000:  # Menos de 1 segundo
        print("✓ Rendimiento aceptable")
    else:
        print("⚠ Rendimiento lento, considere optimizar índices")
    
    return True

def main():
    """Función principal de pruebas"""
    print("=== PRUEBAS DEL SISTEMA DE VENTAS CON POSTGRESQL ===")
    print()
    
    tests = [
        ("Conexión a base de datos", test_database_connection),
        ("Operaciones CRUD", test_crud_operations),
        ("Consultas especializadas", test_queries),
        ("Rendimiento", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Ejecutando: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                print(f"✓ {test_name}: EXITOSO")
                passed += 1
            else:
                print(f"✗ {test_name}: FALLÓ")
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
    
    print(f"\n{'='*50}")
    print(f"RESULTADOS: {passed}/{total} pruebas exitosas")
    print('='*50)
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
    else:
        print("⚠ Algunas pruebas fallaron. Revise los errores antes de usar el sistema en producción.")

if __name__ == "__main__":
    main()
