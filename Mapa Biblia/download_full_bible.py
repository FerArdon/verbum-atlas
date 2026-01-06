import requests
import os
import sqlite3

# URL de la Biblia Reina Valera 1909 (SpaRV)
url = "https://github.com/scrollmapper/bible_databases/raw/master/formats/sqlite/SpaRV.db"
output_file = "biblia.db"

print(f"Descargando Biblia Completa (SpaRV 1909) desde: {url}")

try:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"¡Éxito! Biblia guardada (Tamaño: {len(response.content)/1024/1024:.2f} MB)")
        
        # Verificar estructura interna para asegurar compatibilidad
        conn = sqlite3.connect(output_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tablas encontradas en la nueva DB: {tables}")
        
        # Ver columnas de la tabla principal (usualmente 'bible' o 't_bible')
        if tables:
            first_table = tables[0][0]
            cursor.execute(f"PRAGMA table_info({first_table})")
            columns = cursor.fetchall()
            print(f"Columnas en '{first_table}': {[col[1] for col in columns]}")
            
        conn.close()
        
    else:
        print(f"Error descarga: {response.status_code}")
except Exception as e:
    print(f"Error crítico: {e}")
