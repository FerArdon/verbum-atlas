import fitz
import sqlite3
import re

pdf_path = "book_of_mormon_2013_ed_guide_to_the_scriptures_footnotes_softcover_mod_a5.pdf"
db_path = "libro_mormon.db"

# Páginas de inicio (según el script anterior)
BOOKS_START = {
    "Enós": 189, # índice (pág 190)
    "Jarom": 192,
    "Omni": 194,
    "Palabras de Mormón": 197,
    "4 Nefi": 589, # Estimado (Mormón era 595. 4 Nefi es justo antes)
    "Mormón": 594 
}

# Límites (aproximados, hasta donde empieza el siguiente libro)
BOOKS_END = {
    "Enós": 192,
    "Jarom": 194,
    "Omni": 197,
    "Palabras de Mormón": 199,
    "4 Nefi": 594,
    "Mormón": 616 # Antes de Éter
}

conn = sqlite3.connect(db_path)
c = conn.cursor()
doc = fitz.open(pdf_path)

def extract_one_chapter_book(book_name, start_idx, end_idx, chapter=1):
    print(f"Rellenando {book_name}...")
    # Borrar si había algo mal
    c.execute("DELETE FROM verses WHERE book_name=? AND chapter=?", (book_name, chapter))
    
    for i in range(start_idx, end_idx + 1):
        text = doc[i].get_text()
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Buscar versículos
            match = re.match(r'^(\d+)\s*(.*)', line)
            if match:
                v_num = int(match.group(1))
                v_text = match.group(2)
                try:
                    c.execute("INSERT INTO verses (book_name, chapter, verse, text) VALUES (?, ?, ?, ?)",
                            (book_name, chapter, v_num, v_text))
                except: pass

# Ejecutar relleno
extract_one_chapter_book("Enós", 189, 192)
extract_one_chapter_book("Jarom", 192, 194)
extract_one_chapter_book("Omni", 194, 197)
extract_one_chapter_book("Palabras de Mormón", 197, 199)
# 4 Nefi y Mormón requieren más cuidado, pero esto ya mejora mucho.

# Para Mormón (caps múltiples), usamos la lógica masiva pero restringida a esas páginas
print("Rellenando libro de Mormón (complejo)...")
start_mor = 594
end_mor = 616
curr_chap = 0
for i in range(start_mor, end_mor + 1):
    text = doc[i].get_text()
    lines = text.split('\n')
    for line in lines:
        line = line.strip().upper()
        if line.startswith("CAPÍTULO") or line.startswith("CAPITULO"):
            try:
                curr_chap = int(line.split()[1])
            except: pass
        
        # Versos
        match = re.match(r'^(\d+)\s*(.*)', line) # Reusar regex simple
        if match and curr_chap > 0:
            try:
                c.execute("INSERT OR IGNORE INTO verses (book_name, chapter, verse, text) VALUES (?, ?, ?, ?)",
                          ("Mormón", curr_chap, int(match.group(1)), match.group(2)))
            except: pass

conn.commit()
conn.close()
print("Relleno completado.")
