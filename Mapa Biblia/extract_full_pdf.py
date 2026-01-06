import fitz
import sqlite3
import re

pdf_path = "book_of_mormon_2013_ed_guide_to_the_scriptures_footnotes_softcover_mod_a5.pdf"
db_path = "libro_mormon.db"

# Mapeo de títulos (texto del PDF -> Nombre DB)
TITLE_MAP = {
    "EL PRIMER LIBRO DE NEFI": "1 Nefi",
    "EL SEGUNDO LIBRO DE NEFI": "2 Nefi",
    "EL LIBRO DE JACOB": "Jacob",
    "EL LIBRO DE ENÓS": "Enós",
    "EL LIBRO DE JAROM": "Jarom",
    "EL LIBRO DE OMNI": "Omni",
    "LAS PALABRAS DE MORMÓN": "Palabras de Mormón",
    "EL LIBRO DE MOSÍAH": "Mosíah",
    "EL LIBRO DE ALMA": "Alma",
    "EL LIBRO DE HELAMÁN": "Helamán",
    "3 NEFI": "3 Nefi", # A veces aparece como TERCER LIBRO
    "EL TERCER LIBRO DE NEFI": "3 Nefi",
    "4 NEFI": "4 Nefi",
    "EL CUARTO LIBRO DE NEFI": "4 Nefi",
    "EL LIBRO DE MORMÓN": "Mormón", # Cuidado confunde con título general
    "EL LIBRO DE ÉTER": "Éter",
    "EL LIBRO DE MORONI": "Moroni"
}

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Limpiar tabla (empezamos de cero)
c.execute("DELETE FROM verses")
print("Base de datos limpia.")

doc = fitz.open(pdf_path)

current_book = "1 Nefi" # Empezamos aquí
current_chapter = 0 # Esperamos encontrar Capítulo 1
buffer_text = ""
start_page = 29 # Índice 29 es página 30

print("Extrayendo texto...")

for i in range(start_page, len(doc)):
    page_text = doc[i].get_text()
    lines = page_text.split('\n')
    
    for line in lines:
        line_clean = line.strip()
        if not line_clean: continue
        
        # Detectar Cambio de Libro
        line_upper = line_clean.upper()
        # Caso especial Mormón vs Título
        if line_upper in TITLE_MAP:
             # Si encontramos "EL LIBRO DE MORMÓN" en medio, asumimos es el libro interno
             if line_upper == "EL LIBRO DE MORMÓN" and current_book == "4 Nefi":
                 current_book = "Mormón"
                 current_chapter = 0
             elif line_upper != "EL LIBRO DE MORMÓN": # Otros libros
                 current_book = TITLE_MAP[line_upper]
                 current_chapter = 0
                 # print(f"--- Cambio de libro: {current_book} ---")

        # Detectar Capítulo
        if line_upper.startswith("CAPÍTULO ") or line_upper.startswith("CAPITULO "):
            try:
                # Extraer número
                parts = line_upper.split()
                if len(parts) > 1 and parts[1].isdigit():
                    current_chapter = int(parts[1])
                    # print(f"   Capítulo {current_chapter}")
            except: pass
            
        # Detectar Versículo (Número al inicio)
        # Regex simple: número al inicio seguido de algo
        # Cuidado con notas al pie (a, b...)
        
        # Mi estrategia sucio-rápida:
        # Si la línea empieza con número, es un versículo nuevo.
        # Si no, es continuación del anterior.
        
        match = re.match(r'^(\d+)\s*(.*)', line_clean)
        
        if match and current_chapter > 0:
            verse_num = int(match.group(1))
            verse_text = match.group(2)
            
            # Limpieza básica de referencias (letras sueltas a,b,c)
            # Esto es difícil sin dañar texto real, pero probemos quitar letras solitarias
            # verse_text = re.sub(r'\s[a-z]\s', ' ', verse_text) 
            
            # Guardar en DB
            try:
                c.execute("INSERT INTO verses (book_name, chapter, verse, text) VALUES (?, ?, ?, ?)",
                          (current_book, current_chapter, verse_num, verse_text))
            except: pass # Ignorar duplicados
            
        elif current_chapter > 0:
            # Texto continuo (quizás añadir al último versículo insertado)
            # Esto mejora la legibilidad
            pass 

conn.commit()
conn.close()
print("¡Extracción terminada! (Revisa si hay datos)")
