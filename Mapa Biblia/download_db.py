import requests
import os

# URL del archivo SQLite de la Biblia Reina Valera 1960
url = "https://github.com/scrollmapper/bible_databases/raw/master/sqlite/SF_2014-01-21_RVR1960_Spanish_Reina-Valera_1960.sqlite"
output_file = "biblia.db"

print(f"Descargando base de datos desde: {url}")

try:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Éxito: Base de datos guardada como '{output_file}'")
    else:
        print(f"Error: No se pudo descargar (Status code: {response.status_code})")
except Exception as e:
    print(f"Error crítico: {e}")
