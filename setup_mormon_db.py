import sqlite3
import re
import os

def crear_base_datos():
    # 1. Conexión a la base de datos (se crea si no existe)
    nombre_db = "libro_mormon.db"
    
    # Eliminar si existe para empezar de cero (opcional)
    if os.path.exists(nombre_db):
        os.remove(nombre_db)
        
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()

    print(f"Creando base de datos: {nombre_db}...")

    # 2. Definición del Esquema (DDL)
    # Tabla: Libros (ej. 1 Nefi, Alma)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')

    # Tabla: Capítulos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capitulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER,
            numero_capitulo INTEGER,
            resumen TEXT,
            FOREIGN KEY(libro_id) REFERENCES libros(id)
        )
    ''')

    # Tabla: Versículos (Texto contenido)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS versiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capitulo_id INTEGER,
            numero_versiculo INTEGER,
            texto_contenido TEXT,
            FOREIGN KEY(capitulo_id) REFERENCES capitulos(id)
        )
    ''')

    conn.commit()
    print("Esquema creado exitosamente.")
    return conn

def poblar_base_datos(conn, archivo_texto):
    cursor = conn.cursor()
    
    try:
        with open(archivo_texto, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        print("Procesando texto e insertando datos...")
        
        # Nota técnica: Este es un ejemplo de lógica de parseo básica.
        # Dado que el formato de texto puede variar, este script busca patrones
        # como "EL PRIMER LIBRO DE NEFI" o "CAPÍTULO 1".
        
        # Ejemplo simplificado de inserción manual para demostración
        # Si tienes el texto completo parseado, aquí iría el bucle de lectura.
        
        # Inserción de prueba basada en los documentos analizados:
        lista_libros = ["1 Nefi", "2 Nefi", "Jacob", "Enós", "Jarom", "Omni", "Palabras de Mormón", "Mosíah", "Alma", "Helamán", "3 Nefi", "4 Nefi", "Mormón", "Éter", "Moroni"]
        
        for libro in lista_libros:
            cursor.execute("INSERT OR IGNORE INTO libros (nombre) VALUES (?)", (libro,))
            
        conn.commit()
        print("Datos de estructura base insertados.")
        
        # Verificación de integridad (Conteo)
        cursor.execute("SELECT Count(*) FROM libros")
        conteo = cursor.fetchone()[0]
        print(f"Total de libros registrados: {conteo}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_texto}'. Asegúrate de crearlo con el contenido del libro.")
    except Exception as e:
        print(f"Error al procesar: {e}")

    conn.close()

if __name__ == "__main__":
    # Nombre del archivo de texto fuente
    archivo_fuente = "texto_mormon.txt" 
    
    conexion = crear_base_datos()
    poblar_base_datos(conexion, archivo_fuente)
    print("Proceso finalizado. La base de datos 'libro_mormon.db' está lista.")