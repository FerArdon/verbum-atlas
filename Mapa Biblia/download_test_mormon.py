import sqlite3
import urllib.request
import re
import time
import json

# Configuración de base de datos
db_path = 'libro_mormon.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Asegurar tabla limpia (mantenemos la estructura)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_name TEXT,
        chapter INTEGER,
        verse INTEGER,
        text TEXT
    )
''')

# Mapeo de libros (ID web -> Nombre DB)
# Referencia: https://www.churchofjesuschrist.org/study/scriptures/bofm?lang=spa
books_map = [
    ("1-ne", "1 Nefi", 22),
    ("2-ne", "2 Nefi", 33),
    ("jacob", "Jacob", 7),
    ("enos", "Enós", 1),
    ("jarom", "Jarom", 1),
    ("omni", "Omni", 1),
    ("w-of-m", "Palabras de Mormón", 1),
    ("mosiah", "Mosíah", 29),
    ("alma", "Alma", 63),
    ("hel", "Helamán", 16),
    ("3-ne", "3 Nefi", 30),
    ("4-ne", "4 Nefi", 1),
    ("morm", "Mormón", 9),
    ("ether", "Éter", 15),
    ("moro", "Moroni", 10)
]

def clean_text(html_content):
    # Extraer versículos. El formato suele ser: <p class="verse" id="p1"><span class="verse-number">1 </span>Texto...</p>
    # O similar. Este es un scraper básico.
    
    # Patrón más o menos genérico para encontrar texto de la iglesia
    # Buscamos contenido dentro de <p class="verse"...>
    # Simplificado: buscar por ID="p1", etc.
    
    verses = []
    
    # Dividir por <p
    parts = html_content.split('<p')
    for part in parts:
        if 'class="verse"' in part or 'id="p' in part:
            # Intentar extraer número y texto
            # Limpieza bruta de tags
            clean = re.sub(r'<[^>]+>', '', part).strip()
            # Si empieza con número, es versículo
            match = re.match(r'(\d+)\s+(.*)', clean)
            if match:
                v_num = int(match.group(1))
                v_text = match.group(2)
                verses.append((v_num, v_text))
            elif len(verses) > 0 and clean: # Continuación de texto
                 # A veces el versículo sigue
                 pass
                 
    return verses

def download_book(web_id, db_name, chapters):
    print(f"Descargando {db_name}...")
    for chap in range(1, chapters + 1):
        url = f"https://www.churchofjesuschrist.org/study/scriptures/bofm/{web_id}/{chap}?lang=spa"
        try:
            # Headers para parecer navegador
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8')
                
            verses = clean_text(html)
            
            if verses:
                print(f"  Cap {chap}: {len(verses)} versículos encontrados.")
                # Guardar en DB
                for v_num, v_text in verses:
                    cursor.execute("INSERT OR REPLACE INTO verses (book_name, chapter, verse, text) VALUES (?, ?, ?, ?)",
                                   (db_name, chap, v_num, v_text))
                conn.commit()
            else:
                print(f"  ⚠ Cap {chap}: No se pudo extraer texto. (Posible cambio de estructura web)")
                
            time.sleep(0.5) # Respetar al servidor
            
        except Exception as e:
            print(f"  ⚠ Error downloading {url}: {e}")

# Ejecutar descarga (Solo 1 Nefi 1 y 2 para probar)
# Descomentar línea abajo para descarga completa
# download_book("1-ne", "1 Nefi", 2) 

print("Iniciando prueba de descarga...")
download_book("1-ne", "1 Nefi", 2)
conn.close()
