import os
import json
from models.loteria_model import Loteria
from data.loteria_data import DEFAULT_LOTERIAS
from utils.display_utils import clean_text_for_search
from models.loteria import crear_tabla_loterias, insertar_loteria, obtener_loterias

# Inicializar las loterías como objetos Loteria
# loterias_list = [Loteria(**data) for data in dic_loterias]

loterias_list = []
LOTERIAS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'loterias.json')

def _load_loterias():
    """Carga las loterías desde el archivo JSON o usa los datos por defecto."""
    global loterias_list # Indicamos que vamos a modificar la variable global
    try:
        rows = obtener_loterias()  # Esperado: lista de tuplas
        # Transformar filas (id, nombre, fracciones, Decimal(valor), inventario, ...) -> objetos Loteria
        loterias_obj = []
        for row in rows or []:
            try:
                id_loteria = int(row[0])
                nombre_loteria = row[1]
                fracciones_por_billete = int(row[2])
                # Convertir Decimal/float/str a int para el modelo
                valor_por_fraccion = int(row[3]) if row[3] is not None else 0
                cantidad_inventario_inicial_por_fracciones = int(row[4])
                loterias_obj.append(
                    Loteria(
                        id_loteria,
                        nombre_loteria,
                        fracciones_por_billete,
                        valor_por_fraccion,
                        cantidad_inventario_inicial_por_fracciones,
                    )
                )
            except Exception as e:
                print(f"Error transformando fila de lotería {row}: {e}")
        loterias_list = loterias_obj
    except Exception as e:
        print(f"Error al cargar loterías desde la BD: {e}. Usando datos por defecto.")
        loterias_list = [Loteria(**data) for data in DEFAULT_LOTERIAS]
    
    # if os.path.exists(LOTERIAS_FILE):
    #     try:
    #         with open(LOTERIAS_FILE, 'r', encoding='utf-8') as f:
    #             data = json.load(f)
    #             for item in data:
    #                 # Solo incluimos los campos que acepta el constructor
    #                 filtered_data = {
    #                     'id_loteria': item['id_loteria'],
    #                     'nombre_loteria': item['nombre_loteria'],
    #                     'fracciones_por_billete': item['fracciones_por_billete'],
    #                     'valor_por_fraccion': item['valor_por_fraccion'],
    #                     'cantidad_inventario_inicial_por_fracciones': item['cantidad_inventario_inicial_por_fracciones']
    #                 }
    #                 loterias_list.append(Loteria(**filtered_data))
                
    #             print(f"Loterías cargadas desde {LOTERIAS_FILE}")
    #     except json.JSONDecodeError:
    #         print(f"Error al decodificar JSON en {LOTERIAS_FILE}. Usando datos por defecto.")
    #         loterias_list = [Loteria(**data) for data in DEFAULT_LOTERIAS]
    #         # _save_loterias()
    #     except Exception as e:
    #         print(f"Ocurrió un error al cargar loterías: {e}. Usando datos por defecto.")
    #         loterias_list = [Loteria(**data) for data in DEFAULT_LOTERIAS]
    #         # _save_loterias()
    # else:
    #     print(f"Archivo {LOTERIAS_FILE} no encontrado. Inicializando con datos por defecto.")
    #     loterias_list = [Loteria(**data) for data in DEFAULT_LOTERIAS]
    #     _save_loterias() # Guardamos los datos por defecto para crear el archivo
    
def _save_loterias():
    """Guarda las loterías actuales en el archivo JSON."""
    # Convertimos los objetos Loteria a diccionarios para poder serializarlos a JSON
    data_to_save = [loteria.to_dict() for loteria in loterias_list]
    with open(LOTERIAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)
    print(f"Loterías guardadas en {LOTERIAS_FILE}")
    
def get_all_loterias():
    """Retorna todas las loterías como objetos Loteria."""
    return loterias_list

def get_all_loterias_json():
    """Retorna todas las loterías en formato JSON (lista de diccionarios)."""
    return [loteria.to_dict() for loteria in loterias_list]

def find_loteria_by_index(index):
    """Encuentra una lotería por su índice en la lista."""
    if 0 <= index < len(loterias_list):
        return loterias_list[index]
    return None

def find_loteria_by_name(name):
    """Busca una lotería por su nombre."""
    cleaned_search_name = clean_text_for_search(name)

    for loteria in loterias_list:
        cleaned_loteria_name = clean_text_for_search(loteria.nombre_loteria)
        
        if cleaned_search_name in cleaned_loteria_name:
            return loteria
    return None

def add_new_loteria(nombre, fracciones, valor, inventario):
    """Agrega una nueva lotería a la lista."""
    try:
        new_id = len(loterias_list) + 1
        nueva_loteria = Loteria(new_id, nombre, fracciones, valor, inventario)
        
        insertar_loteria(nueva_loteria)
        loterias_list.append(nueva_loteria)
        return nueva_loteria
    except Exception as e:
        print(f"Error al agregar la lotería: {e}")
        return None

def update_loteria_value(loteria, new_value):
    """Actualiza el valor por fracción de una lotería y guarda los cambios."""
    if loteria.set_valor_por_fraccion(new_value):
        _save_loterias()
        return True
    return False

def update_loteria_inventory(loteria, new_quantity):
    """Actualiza el inventario de una lotería y guarda los cambios."""
    if loteria.set_cantidad_inventario(new_quantity):
        _save_loterias()
        return True
    return False

def calculate_overall_totals():
    """Calcula los totales generales de todas las loterías."""
    total_billetes = sum(lot.cantidad_billetes_iniciales for lot in loterias_list)
    total_inventario_inicial = sum(lot.cantidad_inventario_inicial_por_fracciones * lot.valor_por_fraccion for lot in loterias_list)
    return total_billetes, total_inventario_inicial

_load_loterias()