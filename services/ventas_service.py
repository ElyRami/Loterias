import os
import json
from datetime import datetime
from models.venta_model import Ventas
from services.loteria_service import get_all_loterias

ventas_list = []
VENTAS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'ventas.json')

def _load_ventas():
    """Carga las ventas desde el archivo JSON."""
    global ventas_list
    if os.path.exists(VENTAS_FILE):
        try:
            with open(VENTAS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    # Convertir la fecha de string a datetime si es necesario
                    fecha_venta = item['fecha_venta']
                    if isinstance(fecha_venta, str):
                        try:
                            fecha_venta = datetime.strptime(fecha_venta, "%Y-%m-%d")
                        except ValueError:
                            fecha_venta = datetime.now()
                    
                    venta = Ventas(
                        id_venta=item['id_venta'],
                        id_loteria=item['id_loteria'],
                        cantidad_fracciones_vendidas=item['cantidad_fracciones_vendidas'],
                        nombre_cliente=item['nombre_cliente'],
                        nombre_vendedor=item['nombre_vendedor'],
                        fecha_venta=fecha_venta,
                        valor_venta=item['valor_venta']
                    )
                    ventas_list.append(venta)
                
                print(f"Ventas cargadas desde {VENTAS_FILE}")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON en {VENTAS_FILE}. Inicializando lista vacía.")
            ventas_list = []
        except Exception as e:
            print(f"Ocurrió un error al cargar ventas: {e}. Inicializando lista vacía.")
            ventas_list = []
    else:
        print(f"Archivo {VENTAS_FILE} no encontrado. Inicializando lista vacía.")
        ventas_list = []

def _save_ventas():
    """Guarda las ventas actuales en el archivo JSON."""
    data_to_save = []
    for venta in ventas_list:
        venta_dict = venta.to_dict()
        # Convertir datetime a string para JSON
        if isinstance(venta_dict['fecha_venta'], datetime):
            venta_dict['fecha_venta'] = venta_dict['fecha_venta'].strftime("%Y-%m-%d")
        data_to_save.append(venta_dict)
    
    with open(VENTAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)
    print(f"Ventas guardadas en {VENTAS_FILE}")

def get_all_ventas():
    """Retorna todas las ventas como objetos Ventas."""
    return ventas_list

def find_venta_by_id(id_venta):
    """Encuentra una venta por su ID."""
    for venta in ventas_list:
        if venta.id_venta == id_venta:
            return venta
    return None

def find_ventas_by_loteria(id_loteria):
    """Encuentra todas las ventas de una lotería específica."""
    return [venta for venta in ventas_list if venta.id_loteria == id_loteria]

def add_new_venta(id_loteria, cantidad_fracciones_vendidas, nombre_cliente, nombre_vendedor):
    """Agrega una nueva venta a la lista."""
    new_id = len(ventas_list) + 1
    fecha_venta = datetime.now()
    
    # Crear la venta - el valor se calculará automáticamente en el constructor
    nueva_venta = Ventas(
        id_venta=new_id,
        id_loteria=id_loteria,
        cantidad_fracciones_vendidas=cantidad_fracciones_vendidas,
        nombre_cliente=nombre_cliente,
        nombre_vendedor=nombre_vendedor,
        fecha_venta=fecha_venta,
        valor_venta=0  # Se calculará automáticamente
    )
    
    ventas_list.append(nueva_venta)
    _save_ventas()
    return nueva_venta

def get_ventas_by_date_range(fecha_inicio, fecha_fin):
    """Obtiene ventas en un rango de fechas."""
    ventas_en_rango = []
    for venta in ventas_list:
        if fecha_inicio <= venta.fecha_venta <= fecha_fin:
            ventas_en_rango.append(venta)
    return ventas_en_rango

def calculate_total_ventas():
    """Calcula el total de todas las ventas."""
    return sum(venta.valor_venta for venta in ventas_list)

def calculate_ventas_por_loteria():
    """Calcula el total de ventas por lotería."""
    ventas_por_loteria = {}
    for venta in ventas_list:
        if venta.id_loteria not in ventas_por_loteria:
            ventas_por_loteria[venta.id_loteria] = 0
        ventas_por_loteria[venta.id_loteria] += venta.valor_venta
    return ventas_por_loteria

# Cargar ventas al importar el módulo
_load_ventas()

# Lineas nuevas para revisar el control de versiones git