import sqlite3
import re
import os
from pypdf import PdfReader

# Configuración de archivos
PDF_PATH = "book_of_mormon_2013_ed_guide_to_the_scriptures_footnotes_softcover_mod_a5.pdf"
DB_PATH = "libro_mormon.db"

# Orden canónico estricto
ORDEN_LIBROS = [
    "EL PRIMER LIBRO DE NEFI",
    "EL SEGUNDO LIBRO DE NEFI",
    "EL LIBRO DE JACOB",
    "EL LIBRO DE ENÓS",
    "EL LIBRO DE JAROM",
    "EL LIBRO DE OMNI",
    "LAS PALABRAS DE MORMÓN",
    "EL LIBRO DE MOSÍAH",
    "EL LIBRO DE ALMA",
    "EL LIBRO DE HELAMÁN",
    "TERCER NEFI",
    "CUARTO NEFI",
    "EL LIBRO DE MORMÓN",
    "EL LIBRO DE ÉTER",
    "EL LIBRO DE MORONI"
]

# Mapeo de nombres cortos
NOMBRES_CORTOS = {
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
    "TERCER NEFI": "3 Nefi",
    "CUARTO NEFI": "4 Nefi",
    "EL LIBRO DE MORMÓN": "Mormón",
    "EL LIBRO DE ÉTER": "Éter",
    "EL LIBRO DE MORONI": "Moroni"
}

def inicializar_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS versiculos')
    c.execute('DROP TABLE IF EXISTS capitulos')
    c.execute('DROP TABLE IF EXISTS libros')
    
    c.execute('''CREATE TABLE libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT UNIQUE)''')
    
    c.execute('''CREATE TABLE capitulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                libro_id INTEGER, 
                numero INTEGER,
                FOREIGN KEY(libro_id) REFERENCES libros(id))''')
    
    c.execute('''CREATE TABLE versiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                capitulo_id INTEGER, 
                numero INTEGER, 
                texto TEXT,
                FOREIGN KEY(capitulo_id) REFERENCES capitulos(id))''')
    conn.commit()
    return conn

def limpiar_texto(texto):
    texto = texto.replace('\xad', '')
    if texto.startswith("O, "): texto = "YO, " + texto[3:]
    texto = re.sub(r'^Y?\s*O,\s*Nefi', 'YO, Nefi', texto)
    if "que se" in texto and "arrepintiera" in texto:
        texto = re.sub(r'que se.*?arrepintiera', 'que se arrepintiera', texto, flags=re.DOTALL)
    texto = re.sub(r'\s+[a-z]\s+(?=[A-Z])', ' ', texto)
    texto = re.sub(r'\s+[bcdfghjklmnpqrstvwxz]\s+', ' ', texto, flags=re.IGNORECASE)
    noise_patterns = [
        r'\[.*?\]',
        r'GEE\s+.*?\.',
        r'\b(Prov|Enós|Mos|Morm|Éter|DyC|Omni|Cró|Rey|Jer|Sal|Mat|Luc|Hch)\.?\s+\d+[:]\d+.*?\.',
        r'–\d+;',
        r'–\s*\d+'
    ]
    for p in noise_patterns:
        texto = re.sub(p, '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def es_nota_al_pie(texto):
    t = texto.strip()
    t_upper = t.upper()
    if not t or len(t) < 3: return True
    bloqueos = [
        "RELATO DE LEHI", "ESCRIBÍ ESTOS ANALES", "TIERRA PROMETIDA", 
        "LAMÁN", "LEMUEL", "ISMAEL", "ABUNDANCIA", "BARCO", "GRANDES AGUAS",
        "QUITARLE LA VIDA", "CRONOLOGÍA", "APÉNDICE", "ONOLOGÍA",
        "PÁG.", "CAPÍTULO"
    ]
    if any(b in t_upper for b in bloqueos): return True
    if len(re.findall(r'\d+:\d+', t)) >= 2: return True
    if "GEE" in t_upper or "VÉASE" in t_upper: return True
    if re.match(r'^\d*[a-z]\s+GEE', t): return True
    if re.match(r'^\d*[a-z]?\s*[A-Z\s]+\s+\d+[:]\d+', t): return True
    if re.match(r'^[1-4]?\s*[A-Z\s]+\s+\d+[:]\d+', t): return True
    if t.isupper() and len(t) < 80: return True
    return False

def limpiar_db_final(db_path):
    print("Ejecutando limpieza COMPLETA de la base de datos...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    rep_map = {
        "Je rusalén": "Jerusalén", "miste rios": "misterios", "len guaje": "lenguaje",
        "comen zar": "comenzar", "afli cciones": "aflicciones", "ha biendo": "habiendo",
        "du rante": "durante", "ins trucción": "instrucción", "com pone": "compone",
        "nues tro": "nuestro", "mise ricordias": "misericordias", "cin cuenta": "cincuenta",
        "es tas": "estas", "so bre": "sobre", "man dato": "mandato",
        "a rebeliones": "rebeliones", "a padre": "padre",
        "salido Je": "salido de Jerusalén", "biado de": "agobiado de",
        "ins truyó": "instruyó", "re misión": "remisión", "Ja rom": "Jarom",
        "pa labras": "palabras", "pe queñas": "pequeñas", "be nefic": "benefic",
        "a Enós": "Enós", "a lucha": "lucha",
        "E aquí": "HE aquí", "HORA bien": "AHORA bien",
        "tam bién": "también", "es tablecido": "establecido", "arrepen tían": "arrepentían",
        "peca dos": "pecados", "lama nitas": "lamanitas", "conti nuó": "continuó",
        "efec tuaban": "efectuaban", "sana ban": "sanaban", "resucita ban": "resucitaban",
        "obe decían": "obedecían", "edifica ban": "edificaban", "multi plicó": "multiplicó",
        "incen diado": "incendiado", "hundi do": "hundido", "reedifi cadas": "reedificadas",
        "matri monio": "matrimonio", "bendeci dos": "bendecidos", "pros peridad": "prosperidad",
        "orga nizaron": "organizaron", "conten ciones": "contenciones", "disci pulos": "discípulos",
        "mila gros": "milagros", "perma necer": "permanecer", "gene ración": "generación",
        "sacerdo tes": "sacerdotes", "profe tas": "profetas", "iglesia": "iglesia",
        "evan gelio": "evangelio", "ini quidad": "iniquidad", "abo minación": "abominación",
        "perse guían": "perseguían", "pri siones": "prisiones", "hor nos": "hornos",
        "ani males": "animales", "fieras": "fieras", "incre dulidad": "incredulidad",
        "cre yentes": "creyentes", "adora dores": "adoradores", "lemue litas": "lemuelitas",
        "amaleki tas": "amalekitas", "ensal zaban": "ensalzaban", "cos tosas": "costosas",
        "obje tos": "objetos", "trans currido": "transcurrido", "cua renta": "cuarenta",
        "cin cuenta": "cincuenta", "se tenta": "setenta", "ochen ta": "ochenta",
        "no venta": "noventa", "dos cientos": "doscientos", "tres cientos": "trescientos",
        "el a lenguaje": "el lenguaje", "es a verdadera": "es verdadera",
        "el a primer": "el primer", "a Nefi": "Nefi", "a Lehi": "Lehi",
        "e Jerusalén": "Jerusalén", "dJerusalén": "Jerusalén",
        "e aflicciones": "aflicciones", "muchas e aflicciones": "muchas aflicciones",
        "a estas": "estas", "a ciudad": "ciudad", "a hundido": "hundido",
        "a hermoso": "hermoso", "a prácticas": "prácticas", "a perseguían": "perseguían",
        "a prisiones": "prisiones", "a herían": "herían", "a combinaciones": "combinaciones",
        "a pecados": "pecados", "a anales": "anales", "a volvie": "volvie",
        "ORQUE": "PORQUE",
        "1. . . de": "", "profeta nefita.": "", "Mor o. . ordenar.": "",
        ". . .": "", "Alma Juan sacerdotales.": ""
    }
    for roto, limpio in rep_map.items():
        cursor.execute("UPDATE versiculos SET texto = REPLACE(texto, ?, ?)", (roto, limpio))
    citas_basura = [
        "Prov .", "Prov.", "Mos.", "DyC", "GEE", "Véase", "Cró.", "Jer.", "Rey.",
        "Rom.", "Deut.", "Gál.", "Hel.", "Apéndice", "Éter", "Omni",
        "Ne.", "Enós 1:", "Jacob 7:", "3 Nefi", "c Gál."
    ]
    for cita in citas_basura:
        cursor.execute("UPDATE versiculos SET texto = REPLACE(texto, ?, '')", (cita,))
    
    cursor.execute("UPDATE versiculos SET texto = 'Alma' WHERE texto = '. Alma'")
    cursor.execute("UPDATE versiculos SET texto = REPLACE(texto, '. Alma', 'Alma')")
    cursor.execute("UPDATE versiculos SET texto = REPLACE(texto, 'salido Je', 'salido de Jerusalén')")
    
    cursor.execute("""
        DELETE FROM versiculos 
        WHERE LENGTH(texto) < 25 
        AND texto NOT LIKE '%respondió%' 
        AND texto NOT LIKE '%dijo%' 
        AND texto NOT LIKE '%contestó%'
        AND texto NOT LIKE '%Sí%'
        AND texto NOT LIKE '%No%'
    """)
    cursor.execute("DELETE FROM versiculos WHERE TRIM(texto) LIKE '.%' AND LENGTH(texto) < 20")
    cursor.execute("DELETE FROM versiculos WHERE texto LIKE '%. Alma%' AND LENGTH(texto) < 15")
    
    cursor.execute("""
        DELETE FROM versiculos WHERE numero = 2 AND capitulo_id IN (
            SELECT c.id FROM capitulos c 
            JOIN libros l ON c.libro_id = l.id 
            WHERE l.nombre = '3 Nefi' AND c.numero = 11
        ) AND LENGTH(texto) < 15
    """)
    
    texto_v4_limpio = "Pues sucedió que al comenzar el primer año del reinado de Sedequías, rey de Judá (mi padre Lehi había morado en Jerusalén toda su vida), llegaron muchos profetas ese mismo año profetizando al pueblo que se arrepintiera, o la gran ciudad de Jerusalén sería destruida."
    cursor.execute("""
        UPDATE versiculos SET texto = ? 
        WHERE numero = 4 AND capitulo_id = (
            SELECT c.id FROM capitulos c 
            JOIN libros l ON c.libro_id = l.id 
            WHERE l.nombre = '1 Nefi' AND c.numero = 1
        )
    """, (texto_v4_limpio,))

    letras_basura = "bcdfghjklmnpqrstvwxz"
    for letra in letras_basura:
        cursor.execute("UPDATE versiculos SET texto = REPLACE(texto, ' " + letra + " ', ' ')")
    
    cursor.execute("SELECT id, texto FROM versiculos")
    for row in cursor.fetchall():
        texto_limpio = re.sub(r'\d+:\d+[.;,]?', '', row[1])
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
        if texto_limpio != row[1]:
            cursor.execute("UPDATE versiculos SET texto = ? WHERE id = ?", (texto_limpio, row[0]))
    
    for _ in range(5):
        cursor.execute("UPDATE versiculos SET texto = REPLACE(texto, '  ', ' ')")
    
    cursor.execute("DELETE FROM versiculos WHERE texto = 'Alma'")
    cursor.execute("DELETE FROM versiculos WHERE texto = '. Alma'")
    
    conn.commit()
    conn.close()
    print("¡Limpieza COMPLETA finalizada!")

def procesar_pdf():
    if not os.path.exists(PDF_PATH):
        print(f"Error: No se encuentra el archivo PDF: {PDF_PATH}")
        return

    print(f"Leyendo: {PDF_PATH}...")
    try:
        reader = PdfReader(PDF_PATH)
    except Exception as e:
        print(f"Error abriendo PDF (posiblemente falta pypdf): {e}")
        return
        
    conn = inicializar_db()
    cursor = conn.cursor()

    libro_idx = -1
    libro_actual_id = None
    capitulo_actual_id = None
    capitulo_num_actual = 0
    ultimo_versiculo = 0
    esperando_fin_resumen = False # Flag para saltar el resumen inicial
    
    re_capitulo = re.compile(r'CAPÍTULO\s+(\d+)')
    re_header = re.compile(r'^\d*\s*[1-4]?\s*[A-Z\s]+\s+\d+[:]\d+([\u2013\u2014-]\d+)?')
    
    LIBROS_UN_CAPITULO = ["Enós", "Jarom", "Omni", "Palabras de Mormón", "4 Nefi"]

    print(f"Total páginas: {len(reader.pages)}")
    
    for i, page in enumerate(reader.pages):
        texto_pag = page.extract_text()
        if not texto_pag: continue
        
        # 1. Detección de cambio de Libro
        if libro_idx < len(ORDEN_LIBROS) - 1:
            siguiente_libro = ORDEN_LIBROS[libro_idx + 1]
            if siguiente_libro in texto_pag:
                # Validación especial para "EL LIBRO DE MORMÓN"
                es_cambio_valido = True
                if siguiente_libro == "EL LIBRO DE MORMÓN":
                    # Solo es válido si ya pasamos 4 Nefi
                    if libro_idx >= 0 and ORDEN_LIBROS[libro_idx] != "CUARTO NEFI":
                         es_cambio_valido = False

                if es_cambio_valido:
                    libro_idx += 1
                    nombre_corto = NOMBRES_CORTOS[siguiente_libro]
                    print(f"--> [Pág {i}] Iniciando Libro: {nombre_corto}")
                    cursor.execute("INSERT INTO libros (nombre) VALUES (?)", (nombre_corto,))
                    libro_actual_id = cursor.lastrowid
                    capitulo_num_actual = 0
                    ultimo_versiculo = 0
                    
                    if nombre_corto in LIBROS_UN_CAPITULO:
                        capitulo_num_actual = 1
                        cursor.execute("INSERT INTO capitulos (libro_id, numero) VALUES (?, ?)", 
                                       (libro_actual_id, 1))
                        capitulo_actual_id = cursor.lastrowid
                        ultimo_versiculo = 0  
                        esperando_fin_resumen = True
                        print(f"    (Capítulo 1 automático creado para {nombre_corto})")

        if libro_idx == -1: continue

        # 2. Procesamiento de líneas
        lines = texto_pag.split('\n')
        
        for linea in lines:
            linea = linea.strip()
            if not linea: continue

            if re_header.match(linea): continue
            if re.match(r'^\d+$', linea): continue 
            
            # Detectar Nuevo Capítulo
            match_cap = re_capitulo.search(linea)
            if match_cap:
                try:
                    nuevo_cap = int(match_cap.group(1))
                    if nuevo_cap == capitulo_num_actual + 1:
                        capitulo_num_actual = nuevo_cap
                        print(f"    Capítulo {nuevo_cap} detectado (Libro: {ORDEN_LIBROS[libro_idx]})")
                        cursor.execute("INSERT INTO capitulos (libro_id, numero) VALUES (?, ?)", 
                                       (libro_actual_id, capitulo_num_actual))
                        capitulo_actual_id = cursor.lastrowid
                        ultimo_versiculo = 0
                        esperando_fin_resumen = True
                        continue
                except ValueError:
                    pass
            
            # Lógica de Resumen con FAILSAFE
            if esperando_fin_resumen:
                if re.search(r'(\d+|Aproximadamente)\s*(a\.C\.|d\.C\.)', linea):
                    esperando_fin_resumen = False
                    continue
                
                # FAILSAFE: Si vemos un "1 " que parece inicio de versículo, salir del resumen
                if re.match(r'^1\s+[A-Za-zÉÁÍÓÚéáíóúÑñ]', linea):
                    print(f"    [INFO] Salida forzada de resumen en {nombre_corto} Cap {capitulo_num_actual} por hallazgo de Verso 1.")
                    esperando_fin_resumen = False
                    # No continue, procesar esta línea
                else:
                    continue

            # Detectar Versículos
            if capitulo_actual_id:
                match_ver = re.match(r'^(\d+)\s+(.*)', linea)
                if match_ver:
                    num_leido = int(match_ver.group(1))
                    contenido_raw = match_ver.group(2)
                    
                    if num_leido == ultimo_versiculo + 1:
                        if es_nota_al_pie(contenido_raw): continue
                        
                        contenido_limpio = limpiar_texto(contenido_raw)
                        cursor.execute("INSERT INTO versiculos (capitulo_id, numero, texto) VALUES (?, ?, ?)",
                                       (capitulo_actual_id, num_leido, contenido_limpio))
                        ultimo_versiculo = num_leido
                    else:
                        continue
                else:
                    # Línea sin número
                    if capitulo_actual_id and ultimo_versiculo == 0:
                        # Verso 1 sin número explicito (Drop cap)
                        if len(linea) >= 1 and not es_nota_al_pie(linea) and "CAPÍTULO" not in linea:
                            if len(linea) < 40 and NOMBRES_CORTOS[ORDEN_LIBROS[libro_idx]].upper() in linea:
                                continue
                            
                            ultimo_versiculo = 1
                            cursor.execute("INSERT INTO versiculos (capitulo_id, numero, texto) VALUES (?, ?, ?)",
                                           (capitulo_actual_id, 1, limpiar_texto(linea)))
                    
                    elif ultimo_versiculo > 0:
                        # Continuación
                        if NOMBRES_CORTOS[ORDEN_LIBROS[libro_idx]].upper() in linea and len(linea) < 50:
                            continue
                        if es_nota_al_pie(linea): continue

                        contenido_limpio = limpiar_texto(linea)
                        cursor.execute("UPDATE versiculos SET texto = texto || ' ' || ? WHERE capitulo_id=? AND numero=?",
                                       (contenido_limpio, capitulo_actual_id, ultimo_versiculo))

    conn.commit()
    conn.close()
    limpiar_db_final(DB_PATH)
    print("Proceso finalizado. Base de datos 'libro_mormon.db' generada.")

if __name__ == "__main__":
    procesar_pdf()
