import re
import unicodedata

# utils/display_utils.py
def format_currency(value):
    """Formatea un número como moneda colombiana."""
    return '{:,}'.format(value).replace(',', '.')


def clean_text_for_search(text):
    """
    Estandariza un texto para búsqueda:
    - Convierte a minúsculas.
    - Elimina tildes (acentos).
    - Elimina espacios extra.
    """
    if not isinstance(text, str):
        return "" # Aseguramos que solo trabajamos con strings
    text = text.lower() # Convertir a minúsculas
    # Eliminar tildes/acentos
    text = ''.join(c for c in text if c.isalnum() or c.isspace()) # Elimina caracteres no alfanumericos y no espacio
    text = str(unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8'))
    text = re.sub(r'\s+', ' ', text).strip() # Reducir espacios múltiples y eliminar espacios al inicio/final
    return text

def clear_screen():
    """Limpia la consola (depende del sistema operativo)."""
    # Implementación para limpiar la pantalla (opcional)
    pass # Por simplicidad, se deja vacío. En un proyecto real, usarías os.system('cls') o os.system('clear')