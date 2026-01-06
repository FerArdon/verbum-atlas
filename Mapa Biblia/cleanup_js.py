import re

# Leer el archivo
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Eliminar función openMapModal
pattern_modal_func = r'window\.openMapModal = function[\s\S]*?};'
content = re.sub(pattern_modal_func, '', content)

# 2. Mantener window.goToReference pero limpiarla si tiene cosas raras
# (Dejaremos goToReference porque es útil para las referencias cruzadas)

# 3. Limpiar referencias en switchView (opcional, pero buena práctica)
# Como usamos un switchView genérico, no hay referencias explícitas que borrar
# excepto si hubiera ifs específicos, pero en mi script anterior los quité.

# Guardar
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ El patio JS está limpio")
