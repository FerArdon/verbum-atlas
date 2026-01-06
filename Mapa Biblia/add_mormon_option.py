import re

# Leer el archivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Patrón para encontrar el select y sus opciones
pattern = r'<select id="bibleVersion"[\s\S]*?</select>'

# Nueva versión con la opción mormona
replacement = """<select id="bibleVersion" style="width: 100%; padding: 8px; border-radius: 8px; border: 1px solid #ccc; font-family: 'Outfit';">
                    <option value="catholic" selected>Católica (73 Libros)</option>
                    <option value="protestant">Reina Valera (66 Libros)</option>
                    <option value="mormon">Libro de Mormón (15 Libros)</option>
                </select>"""

if re.search(pattern, content):
    content = re.sub(pattern, replacement, content)
    print("✓ Opción de Libro de Mormón agregada al selector")
else:
    print("✗ No se encontró el selector bibleVersion")

# Guardar
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
