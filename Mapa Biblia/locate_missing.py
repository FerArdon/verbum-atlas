import fitz
import sqlite3
import re

pdf_path = "book_of_mormon_2013_ed_guide_to_the_scriptures_footnotes_softcover_mod_a5.pdf"
db_path = "libro_mormon.db"

MISSING_BOOKS = {
    "EL LIBRO DE ENÓS": "Enós",
    "EL LIBRO DE JAROM": "Jarom",
    "EL LIBRO DE OMNI": "Omni",
    "LAS PALABRAS DE MORMÓN": "Palabras de Mormón",
    "4 NEFI": "4 Nefi",
    "EL LIBRO DE MORMÓN": "Mormón" # Este es confuso
}

conn = sqlite3.connect(db_path)
c = conn.cursor()

doc = fitz.open(pdf_path)
print("Buscando libros perdidos...")

current_book = None
text_buffer = ""

# Escaneo rápido de todo el documento buscando títulos exactos
for i in range(len(doc)):
    text = doc[i].get_text()
    lines = text.split('\n')
    
    for line in lines:
        line_clean = line.strip().upper()
        
        # Si encontramos un título perdido
        if line_clean in MISSING_BOOKS:
            current_book = MISSING_BOOKS[line_clean]
            print(f"¡ENCONTRADO DE NUEVO! {current_book} en pág {i+1}")
            # Estos libros tienen solo 1 capítulo (excepto Mormón)
            # Vamos a extraer todo el texto hasta el siguiente libro
            
            # (Aquí iría lógica compleja de extracción, pero por ahora solo registro hallazgo)

conn.close()
