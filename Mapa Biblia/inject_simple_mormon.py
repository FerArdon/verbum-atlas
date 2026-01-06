import re

# Leer app.js
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Definir los libros mormones como objetos JS
mormon_books_js = """
    // LIBRO DE MORMÓN
    { id: "1nefi", name: "1 Nefi", testament: "mormon", category: "Libro de Nefi", themeColor: "#8B5CF6", totalChapters: 22 },
    { id: "2nefi", name: "2 Nefi", testament: "mormon", category: "Libro de Nefi", themeColor: "#8B5CF6", totalChapters: 33 },
    { id: "jacob", name: "Jacob", testament: "mormon", category: "Libro de Jacob", themeColor: "#3B82F6", totalChapters: 7 },
    { id: "enos", name: "Enós", testament: "mormon", category: "Libro de Enós", themeColor: "#3B82F6", totalChapters: 1 },
    { id: "jarom", name: "Jarom", testament: "mormon", category: "Libro de Jarom", themeColor: "#3B82F6", totalChapters: 1 },
    { id: "omni", name: "Omni", testament: "mormon", category: "Libro de Omni", themeColor: "#3B82F6", totalChapters: 1 },
    { id: "palabras", name: "Palabras de Mormón", testament: "mormon", category: "Palabras de Mormón", themeColor: "#10B981", totalChapters: 1 },
    { id: "mosiah", name: "Mosíah", testament: "mormon", category: "Libro de Mosíah", themeColor: "#10B981", totalChapters: 29 },
    { id: "alma", name: "Alma", testament: "mormon", category: "Libro de Alma", themeColor: "#F59E0B", totalChapters: 63 },
    { id: "helaman", name: "Helamán", testament: "mormon", category: "Libro de Helamán", themeColor: "#F59E0B", totalChapters: 16 },
    { id: "3nefi", name: "3 Nefi", testament: "mormon", category: "Libro de Nefi", themeColor: "#EC4899", totalChapters: 30 },
    { id: "4nefi", name: "4 Nefi", testament: "mormon", category: "Libro de Nefi", themeColor: "#EC4899", totalChapters: 1 },
    { id: "mormon", name: "Mormón", testament: "mormon", category: "Libro de Mormón", themeColor: "#EF4444", totalChapters: 9 },
    { id: "eter", name: "Éter", testament: "mormon", category: "Libro de Éter", themeColor: "#6366F1", totalChapters: 15 },
    { id: "moroni", name: "Moroni", testament: "mormon", category: "Libro de Moroni", themeColor: "#06B6D4", totalChapters: 10 }
"""

# Insertar estos libros dentro del array bibleData (justo antes del cierre '];')
content = re.sub(r'(\s*)\}\s*\];', r'\1},\n' + mormon_books_js + r'\n];', content, count=1)

# 2. Modificar renderBooks para filtrar correctamente
# Buscamos la línea del filtro
old_filter = r"const matchesF = f === 'all' \? true : \(f === 'old' \? book\.testament === 'old' : book\.testament === 'new'\);"

# Nueva lógica: 
# Si currentMode es 'mormon', solo mostrar testament === 'mormon'.
# Si currentMode NO es 'mormon', ocultar testament === 'mormon'.
new_filter_logic = """
        let matchesF = false;
        if (currentMode === 'mormon') {
            matchesF = (book.testament === 'mormon');
        } else {
            if (book.testament === 'mormon') matchesF = false;
            else matchesF = (f === 'all' ? true : (f === 'old' ? book.testament === 'old' : book.testament === 'new'));
        }
"""

if re.search(old_filter, content):
    content = re.sub(old_filter, new_filter_logic.strip(), content)
    print("✓ Lógica de filtro actualizada.")
else:
    print("✗ No se encontró la lógica de filtro original (posiblemente diferente formato).")

# 3. Arreglar etiqueta AT/NT en las tarjetas
# Buscamos el ternario del label
old_label = r"\$\{book\.testament === 'old' \? 'A\.T\.' : 'N\.T\.'\}"
new_label = r"${book.testament === 'old' ? 'A.T.' : (book.testament === 'mormon' ? 'L.M.' : 'N.T.')}"
content = re.sub(old_label, new_label, content)

# 4. Agregar portadas especiales (simple diccionario)
# Buscamos "exodo": "exodo.jpg" y agregamos las mormonas antes
mormon_covers = '"1nefi": "1 nefi.jpg", "2nefi": "2 nefi.jpg", "jacob": "libro jacob.jpg", "enos": "libro enos.jpg", "jarom": "libro de jarom.jpg", "omni": "libro de omni.jpg", "palabras": "palabras de mormon.jpg", "mosiah": "libro de mosia.jpg", "alma": "libro de alma.jpg", "helaman": "libro de helaman.jpg", "3nefi": "tercer (3) nefi.jpg", "4nefi": "cuarto (4) nefi.jpg", "mormon": "libro mormon.jpg", "eter": "libro de eter.jpg", "moroni": "libro moroni.jpg",'
content = content.replace('"exodo": "exodo.jpg",', mormon_covers + '\n        "exodo": "exodo.jpg",')


# 5. Fix de loadChapter (el adapter para que el click funcione si usa la versión antigua)
# Como hemos restaurado el JS antiguo, es probable que openBookMap use window.loadChapter o algo así?
# No, el archivo original usaba loadChapterText directamente.
# Voy a asegurarme de que openBookMap usa setAttribute de forma segura por si acaso el JS original tenía el problema de backticks.

# EL JS ORIGINAL tenía: card.onclick = () => openBookMap(book);
# Y dentro de openBookMap? Veamos el archivo original.
# Asumiremos que está bien. Si falla el click, usaremos el fix_clicks.py después.

# Guardar
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Datos inyectados en bibleData.")
