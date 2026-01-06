import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar opción Mormón
if 'value="mormon"' not in content:
    content = content.replace(
        '<option value="protestant">Reina Valera (66 Libros)</option>',
        '<option value="protestant">Reina Valera (66 Libros)</option>\n                    <option value="mormon">Libro de Mormón (15 Libros)</option>'
    )

# 2. Agregar script referencias cruzadas (antes de app.js)
if 'src="js/cross_references_data.js"' not in content:
    content = content.replace(
        '<script src="js/app.js"></script>',
        '<script src="js/cross_references_data.js"></script>\n    <script src="js/app.js"></script>'
    )
    # Y quitar la carga json vieja si existe
    content = content.replace('<script src="js/data.js"></script>', '') # Limpieza extra

# 3. Borrar botones Mapas y Lex Divina
content = re.sub(r'<button class="nav-btn" data-target="lexDivina"[\s\S]*?</button>', '', content)
content = re.sub(r'<button class="nav-btn" data-target="historicalMaps"[\s\S]*?</button>', '', content)

# 4. Borrar secciones Mapas y Lex Divina
content = re.sub(r'<!-- VISTA: MAPAS HISTÓRICOS -->[\s\S]*?</section>', '', content)
content = re.sub(r'<!-- VISTA: LEX DIVINA \(IA\) -->[\s\S]*?</section>', '', content)

# Guardar
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ HTML reparado: Mormón ON, Refs ON, Mapas OFF, IA OFF.")
