import re

# Leer el archivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Eliminar sección Mapas Históricos
pattern_maps = r'<!-- VISTA: MAPAS HISTÓRICOS -->[\s\S]*?</section>'
content = re.sub(pattern_maps, '', content)

# 2. Eliminar sección Lex Divina
pattern_lex = r'<!-- VISTA: LEX DIVINA \(IA\) -->[\s\S]*?</section>'
content = re.sub(pattern_lex, '', content)

# 3. Eliminar botones del menú
# Eliminar botón Lex Divina
pattern_btn_lex = r'<button class="nav-btn" data-target="lexDivina"[\s\S]*?</button>'
content = re.sub(pattern_btn_lex, '', content)

# Eliminar botón Mapas Históricos
pattern_btn_maps = r'<button class="nav-btn" data-target="historicalMaps"[\s\S]*?</button>'
content = re.sub(pattern_btn_maps, '', content)

# Limpiar líneas vacías extras que pudieron quedar en el nav
content = re.sub(r'(\n\s*){3,}', '\n\n', content)

# Guardar
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ El patio está limpio: Se eliminaron Mapas y Lex Divina del HTML")
