# views/menu_view.py
import sys
from services import loteria_service
from utils.display_utils import format_currency

def show_main_menu():
    """Muestra el menú principal y obtiene la opción del usuario."""
    print("\n=== Menú Principal ===")
    print("1. Modificar lotería existente")
    print("2. Agregar nueva lotería")
    print("3. Ver todas las loterías")
    print("4. Buscar Lotería")
    print("5. Salir")
    return input("\nSeleccione una opción (1-5): ")

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

def exit_message():
    """Muestra un mensaje de salida."""
    print("¡Hasta luego!")