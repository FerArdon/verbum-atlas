import fitz
import sqlite3
import re

pdf_path = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\83806_spa.pdf"
db_path = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\libro_mormon.db"

print("📖 Extrayendo texto completo del Libro de Mormón...")

# Crear base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Eliminar tabla si existe y recrearla
cursor.execute('DROP TABLE IF EXISTS verses')
cursor.execute('''
CREATE TABLE verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    book_name TEXT,
    chapter INTEGER,
    verse INTEGER,
    text TEXT
)
''')

doc = fitz.open(pdf_path)
print(f"Total de páginas: {len(doc)}")

# Estructura del Libro de Mormón (páginas aproximadas)
mormon_books = [
    {"id": 1, "name": "1 Nefi", "start": 10, "end": 100},
    {"id": 2, "name": "2 Nefi", "start": 100, "end": 200},
    {"id": 3, "name": "Jacob", "start": 200, "end": 250},
    {"id": 4, "name": "Enós", "start": 250, "end": 260},
    {"id": 5, "name": "Jarom", "start": 260, "end": 270},
    {"id": 6, "name": "Omni", "start": 270, "end": 280},
    {"id": 7, "name": "Palabras de Mormón", "start": 280, "end": 290},
    {"id": 8, "name": "Mosíah", "start": 290, "end": 450},
    {"id": 9, "name": "Alma", "start": 450, "end": 900},
    {"id": 10, "name": "Helamán", "start": 900, "end": 1050},
    {"id": 11, "name": "3 Nefi", "start": 1050, "end": 1250},
    {"id": 12, "name": "4 Nefi", "start": 1250, "end": 1280},
    {"id": 13, "name": "Mormón", "start": 1280, "end": 1380},
    {"id": 14, "name": "Éter", "start": 1380, "end": 1550},
    {"id": 15, "name": "Moroni", "start": 1550, "end": 1700}
]

verse_count = 0
current_chapter = 1
current_verse = 1

# Procesar todas las páginas
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    
    # Buscar patrones de capítulo (CAPÍTULO X)
    chapter_match = re.search(r'CAPÍTULO\s+(\d+)', text, re.IGNORECASE)
    if chapter_match:
        current_chapter = int(chapter_match.group(1))
        current_verse = 1
        print(f"📄 Capítulo {current_chapter} encontrado en página {page_num + 1}")
    
    # Buscar versículos (número seguido de texto)
    verse_pattern = r'(\d+)\s+([A-ZÁÉÍÓÚÑ][^\d]+?)(?=\d+\s+[A-ZÁÉÍÓÚÑ]|\Z)'
    verses = re.findall(verse_pattern, text, re.DOTALL)
    
    for verse_num_str, verse_text in verses:
        verse_num = int(verse_num_str)
        verse_text = verse_text.strip()
        
        # Solo guardar si el texto tiene contenido significativo
        if len(verse_text) > 10:
            # Determinar a qué libro pertenece basándose en la página
            book = None
            for b in mormon_books:
                if b["start"] <= page_num < b["end"]:
                    book = b
                    break
            
            if book:
                cursor.execute('''
                    INSERT INTO verses (book_id, book_name, chapter, verse, text)
                    VALUES (?, ?, ?, ?, ?)
                ''', (book["id"], book["name"], current_chapter, verse_num, verse_text))
                verse_count += 1
                
                if verse_count % 100 == 0:
                    print(f"✓ {verse_count} versículos extraídos...")

conn.commit()
conn.close()
doc.close()

print(f"\n✅ Extracción completada!")
print(f"📊 Total de versículos: {verse_count}")
print(f"💾 Base de datos guardada en: {db_path}")
