# Script para generar data.js con 73 libros y CONTEO REAL DE CAPÍTULOS
import json

# Lista maestra: (Nombre, Testamento, Categoría, ¿Deutero?, NumCapitulos)
books_def = [
    # ANTIGUO TESTAMENTO - PENTATEUCO
    ("Génesis", "old", "Pentateuco", False, 50),
    ("Éxodo", "old", "Pentateuco", False, 40),
    ("Levítico", "old", "Pentateuco", False, 27),
    ("Números", "old", "Pentateuco", False, 36),
    ("Deuteronomio", "old", "Pentateuco", False, 34),
    
    # HISTÓRICOS
    ("Josué", "old", "Históricos", False, 24),
    ("Jueces", "old", "Históricos", False, 21),
    ("Rut", "old", "Históricos", False, 4),
    ("1 Samuel", "old", "Históricos", False, 31),
    ("2 Samuel", "old", "Históricos", False, 24),
    ("1 Reyes", "old", "Históricos", False, 22),
    ("2 Reyes", "old", "Históricos", False, 25),
    ("1 Crónicas", "old", "Históricos", False, 29),
    ("2 Crónicas", "old", "Históricos", False, 36),
    ("Esdras", "old", "Históricos", False, 10),
    ("Nehemías", "old", "Históricos", False, 13),
    ("Tobías", "old", "Históricos", True, 14), # Deutero
    ("Judit", "old", "Históricos", True, 16),  # Deutero
    ("Ester", "old", "Históricos", False, 10), # (Católica tiene más, pero base 10 es seguro)
    ("1 Macabeos", "old", "Históricos", True, 16), # Deutero
    ("2 Macabeos", "old", "Históricos", True, 15), # Deutero
    
    # SAPIENCIALES
    ("Job", "old", "Sapienciales", False, 42),
    ("Salmos", "old", "Sapienciales", False, 150),
    ("Proverbios", "old", "Sapienciales", False, 31),
    ("Eclesiastés", "old", "Sapienciales", False, 12),
    ("Cantar de los Cantares", "old", "Sapienciales", False, 8),
    ("Sabiduría", "old", "Sapienciales", True, 19),   # Deutero
    ("Eclesiástico", "old", "Sapienciales", True, 51), # Deutero
    
    # PROFETAS MAYORES
    ("Isaías", "old", "Profetas Mayores", False, 66),
    ("Jeremías", "old", "Profetas Mayores", False, 52),
    ("Lamentaciones", "old", "Profetas Mayores", False, 5),
    ("Baruc", "old", "Profetas Mayores", True, 6),   # Deutero
    ("Ezequiel", "old", "Profetas Mayores", False, 48),
    ("Daniel", "old", "Profetas Mayores", False, 14), # (Católica tiene 14, Protestante 12)
    
    # PROFETAS MENORES
    ("Oseas", "old", "Profetas Menores", False, 14),
    ("Joel", "old", "Profetas Menores", False, 3),
    ("Amós", "old", "Profetas Menores", False, 9),
    ("Abdías", "old", "Profetas Menores", False, 1),
    ("Jonás", "old", "Profetas Menores", False, 4),
    ("Miqueas", "old", "Profetas Menores", False, 7),
    ("Nahúm", "old", "Profetas Menores", False, 3),
    ("Habacuc", "old", "Profetas Menores", False, 3),
    ("Sofonías", "old", "Profetas Menores", False, 3),
    ("Hageo", "old", "Profetas Menores", False, 2),
    ("Zacarías", "old", "Profetas Menores", False, 14),
    ("Malaquías", "old", "Profetas Menores", False, 4),
    
    # NUEVO TESTAMENTO
    ("Mateo", "new", "Evangelios", False, 28),
    ("Marcos", "new", "Evangelios", False, 16),
    ("Lucas", "new", "Evangelios", False, 24),
    ("Juan", "new", "Evangelios", False, 21),
    ("Hechos", "new", "Históricos", False, 28),
    
    ("Romanos", "new", "Cartas de Pablo", False, 16),
    ("1 Corintios", "new", "Cartas de Pablo", False, 16),
    ("2 Corintios", "new", "Cartas de Pablo", False, 13),
    ("Gálatas", "new", "Cartas de Pablo", False, 6),
    ("Efesios", "new", "Cartas de Pablo", False, 6),
    ("Filipenses", "new", "Cartas de Pablo", False, 4),
    ("Colosenses", "new", "Cartas de Pablo", False, 4),
    ("1 Tesalonicenses", "new", "Cartas de Pablo", False, 5),
    ("2 Tesalonicenses", "new", "Cartas de Pablo", False, 3),
    ("1 Timoteo", "new", "Cartas de Pablo", False, 6),
    ("2 Timoteo", "new", "Cartas de Pablo", False, 4),
    ("Tito", "new", "Cartas de Pablo", False, 3),
    ("Filemón", "new", "Cartas de Pablo", False, 1),
    
    ("Hebreos", "new", "Cartas Generales", False, 13),
    ("Santiago", "new", "Cartas Generales", False, 5),
    ("1 Pedro", "new", "Cartas Generales", False, 5),
    ("2 Pedro", "new", "Cartas Generales", False, 3),
    ("1 Juan", "new", "Cartas Generales", False, 5),
    ("2 Juan", "new", "Cartas Generales", False, 1),
    ("3 Juan", "new", "Cartas Generales", False, 1),
    ("Judas", "new", "Cartas Generales", False, 1),
    
    ("Apocalipsis", "new", "Profético", False, 22)
]

js_content = "/** GENERATED DATA FILE with 73 Books & Chapter Counts */\nconst bibleData = [\n"

for book in books_def:
    name, test, cat, deutero, chapters = book
    slug = name.lower().replace(" ", "").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    
    # Colors
    color = "#2563EB"
    if test == "old":
        if cat == "Pentateuco": color = "#10B981"
        elif cat == "Históricos": color = "#F59E0B"
        elif cat == "Sapienciales": color = "#8B5CF6"
        elif "Profetas" in cat: color = "#EF4444"
    else:
        if cat == "Evangelios": color = "#DB2777"
        elif "Pablo" in cat: color = "#3B82F6"
    
    js_content += "    {\n"
    js_content += f'        id: "{slug}",\n'
    js_content += f'        name: "{name}",\n'
    js_content += f'        testament: "{test}",\n'
    js_content += f'        category: "{cat}",\n'
    js_content += f'        isDeutero: {str(deutero).lower()},\n'
    js_content += f'        totalChapters: {chapters},\n'
    js_content += f'        themeColor: "{color}",\n'
    js_content += '        map: {\n'
    js_content += f'            title: "Libro de {name}",\n'
    js_content += '            intro: "Selecciona un capítulo para leer.",\n'
    js_content += '            verses: []\n'
    js_content += '        }\n'
    js_content += "    },\n"

js_content += "];"

with open("js/data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("js/data.js regenerado con conteo de capítulos.")
