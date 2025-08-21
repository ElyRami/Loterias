import psycopg2
from config.database import DB_URI

def get_connection():
    try:
        connection = psycopg2.connect(DB_URI)
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    return connection

def close_connection(connection):
    if connection is None:
        return
    try:
        connection.close()
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")