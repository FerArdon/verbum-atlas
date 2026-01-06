import requests
import os
import sqlite3
import zipfile
import io

# URL directa probable para Torres Amat (formato MyBible es SQLite)
url = "https://www.ph4.org/_dl.php?back=bbl&a=TA&b=mybible&c"
output_zip = "biblia_catolica.zip"
output_db = "biblia_catolica.db"

print(f"Intentando descargar Biblia Católica (Torres Amat)...")

# Headers para parecer un navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.ph4.org/b4_index.php'
}

try:
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(output_zip, 'wb') as f:
            f.write(response.content)
        print(f"Archivo descargado: {output_zip}")
        
        # Los archivos .mybible suelen ser ZIPs o SQLite directos.
        # Intentamos ver si es ZIP primero
        try:
            with zipfile.ZipFile(output_zip, 'r') as zip_ref:
                # Buscar el archivo .sqlite o .db dentro
                file_list = zip_ref.namelist()
                print(f"Contenido del ZIP: {file_list}")
                
                # Extraer el primer archivo (que suele ser la DB)
                target = file_list[0]
                zip_ref.extract(target)
                os.rename(target, output_db)
                print(f"Base de datos extraída como: {output_db}")
        except zipfile.BadZipFile:
            print("El archivo no es ZIP, asumiendo que es SQLite directo...")
            os.rename(output_zip, output_db)
            print(f"Renombrado a: {output_db}")

        # Verificacion rapida
        conn = sqlite3.connect(output_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(f"Tablas en DB Católica: {cursor.fetchall()}")
        conn.close()

    else:
        print(f"Error descarga: {response.status_code}")
except Exception as e:
    print(f"Error crítico: {e}")
