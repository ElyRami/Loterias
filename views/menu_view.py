# views/menu_view.py
import sys
from services import loteria_service, ventas_service
from utils.display_utils import format_currency

def show_main_menu():
    """Muestra el menú principal y obtiene la opción del usuario."""
    print("\n=== Menú Principal ===")
    print("1. Modificar lotería existente")
    print("2. Agregar nueva lotería")
    print("3. Ver todas las loterías")
    print("4. Buscar Lotería")
    print("5. Registrar ventas")
    print("6. Salir")
    return input("\nSeleccione una opción (1-6): ")

def show_loterias_list(loterias):
    """Muestra una lista numerada de loterías."""
    print("\nLoterías disponibles:")
    for i, loteria in enumerate(loterias):
        print(f"{i + 1}. {loteria.nombre_loteria}")

def get_loteria_selection(loterias):
    """Solicita al usuario que seleccione una lotería por número."""
    while True:
        try:
            indice = int(input("\nIngrese el número de la lotería que desea modificar: ")) - 1
            if 0 <= indice < len(loterias):
                return loterias[indice]
            else:
                print("Por favor ingrese un número válido de lotería")
        except ValueError:
            print("Por favor ingrese un número válido")

def show_modify_options():
    """Muestra las opciones de modificación de lotería."""
    print("\nQué desea modificar?")
    print("1. Valor por fracción")
    print("2. Cantidad de inventario")
    print("3. Agregar nueva información (no recomendado con el modelo de clase)") # Nota: Se podría remover esta opción si el modelo es estricto
    return input("Seleccione una opción (1-3): ")

def get_numeric_input(prompt):
    """Solicita una entrada numérica al usuario con validación."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Por favor ingrese un valor numérico válido")

def display_loteria_info(loteria):
    """Muestra la información detallada de una lotería."""
    print("\nInformación de la lotería:")
    info = loteria.to_dict()
    for clave, valor in info.items():
        if 'valor' in clave:
            print(f"{clave}: {format_currency(valor)}")
        else:
            print(f"{clave}: {valor}")

def display_all_loterias_detailed():
    """Muestra un listado detallado de todas las loterías."""
    print("\nListado de todas las loterías:")
    loterias = loteria_service.get_all_loterias()
    for loteria in loterias:
        print("\n" + "="*50)
        print(f"Nombre Lotería: {loteria.nombre_loteria}")
        print("-"*50)
        display_loteria_info(loteria) # Reutilizamos la función de mostrar información
        print("-"*50)
        print("Cálculos adicionales:")
        print(f"Cantidad de billetes: {loteria.cantidad_billetes_iniciales}")
        print(f"Valor inventario inicial: {format_currency(loteria.valor_total_inventario_inicial)}")
    print("\n" + "="*50)
    print("TOTALES GENERALES:")
    print("-"*50)
    total_billetes, total_inventario = loteria_service.calculate_overall_totals()
    print(f"Total billetes: {total_billetes}")
    print(f"Total valor inventario inicial: {format_currency(total_inventario)}")
    input("\nPresione Enter para continuar...")

def get_new_loteria_data():
    """Solicita los datos para una nueva lotería."""
    print("\n=== Agregar Nueva Lotería ===")
    nombre = input("Ingrese el nombre de la lotería: ")
    fracciones = get_numeric_input("Ingrese número de fracciones por billete: ")
    valor = get_numeric_input("Ingrese valor por fracción: ")
    inventario = get_numeric_input("Ingrese cantidad de inventario por fraccion: ")
    return nombre, fracciones, valor, inventario

def get_loteria_name_to_search():
    """Solicita el nombre de la lotería a buscar."""
    return input("Ingrese el nombre de la lotería a buscar: ")

def display_search_result(loteria):
    """Muestra el resultado de la búsqueda de lotería."""
    if loteria:
        print("\nInformación de la lotería encontrada:")
        display_loteria_info(loteria)
    else:
        print("Lotería no encontrada.")

def show_ventas_menu():
    """Muestra el menú de ventas y obtiene la opción del usuario."""
    print("\n=== Menú de Ventas ===")
    print("1. Registrar nueva venta")
    print("2. Ver todas las ventas")
    print("3. Ver ventas por lotería")
    print("4. Ver total de ventas")
    print("5. Volver al menú principal")
    return input("\nSeleccione una opción (1-5): ")

def get_venta_data():
    """Solicita los datos para una nueva venta."""
    print("\n=== Registrar Nueva Venta ===")
    
    # Mostrar loterías disponibles
    loterias = loteria_service.get_all_loterias()
    print("\nLoterías disponibles:")
    for i, loteria in enumerate(loterias):
        print(f"{i + 1}. {loteria.nombre_loteria} - Valor por fracción: {format_currency(loteria.valor_por_fraccion)}")
    
    # Seleccionar lotería
    while True:
        try:
            indice = int(input("\nIngrese el número de la lotería: ")) - 1
            if 0 <= indice < len(loterias):
                loteria_seleccionada = loterias[indice]
                break
            else:
                print("Por favor ingrese un número válido de lotería")
        except ValueError:
            print("Por favor ingrese un número válido")
    
    # Obtener cantidad de fracciones
    cantidad_fracciones = get_numeric_input("Ingrese la cantidad de fracciones vendidas: ")
    
    # Obtener datos del cliente y vendedor
    nombre_cliente = input("Ingrese el nombre del cliente: ")
    nombre_vendedor = input("Ingrese el nombre del vendedor: ")
    
    return loteria_seleccionada.id_loteria, cantidad_fracciones, nombre_cliente, nombre_vendedor

def display_venta_info(venta):
    """Muestra la información de una venta."""
    print(f"\nID Venta: {venta.id_venta}")
    print(f"ID Lotería: {venta.id_loteria}")
    print(f"Fracciones vendidas: {venta.cantidad_fracciones_vendidas}")
    print(f"Cliente: {venta.nombre_cliente}")
    print(f"Vendedor: {venta.nombre_vendedor}")
    print(f"Fecha: {venta.fecha_venta}")
    print(f"Valor total: {format_currency(venta.valor_venta)}")

def display_all_ventas():
    """Muestra todas las ventas registradas."""
    ventas = ventas_service.get_all_ventas()
    if not ventas:
        print("\nNo hay ventas registradas.")
        return
    
    print("\n=== Todas las Ventas ===")
    for venta in ventas:
        print("\n" + "-"*50)
        display_venta_info(venta)
    print("\n" + "-"*50)
    input("\nPresione Enter para continuar...")

def display_ventas_por_loteria():
    """Muestra las ventas agrupadas por lotería."""
    ventas_por_loteria = ventas_service.calculate_ventas_por_loteria()
    loterias = loteria_service.get_all_loterias()
    
    if not ventas_por_loteria:
        print("\nNo hay ventas registradas.")
        return
    
    print("\n=== Ventas por Lotería ===")
    for id_loteria, total_ventas in ventas_por_loteria.items():
        # Buscar el nombre de la lotería
        nombre_loteria = "Lotería desconocida"
        for loteria in loterias:
            if loteria.id_loteria == id_loteria:
                nombre_loteria = loteria.nombre_loteria
                break
        
        print(f"\n{nombre_loteria} (ID: {id_loteria}): {format_currency(total_ventas)}")
    
    input("\nPresione Enter para continuar...")

def display_total_ventas():
    """Muestra el total de todas las ventas."""
    total = ventas_service.calculate_total_ventas()
    print(f"\n=== Total de Ventas ===")
    print(f"Total general: {format_currency(total)}")
    input("\nPresione Enter para continuar...")

def exit_message():
    """Muestra un mensaje de salida."""
    print("¡Hasta luego!")