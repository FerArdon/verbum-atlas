import re

# Leer el archivo
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Patrón original
pattern = r'const filtered = bibleData\.filter\(book => \{[\s\S]*?if \(currentMode === \'protestant\' && book\.isDeutero\) return false;'

# Nuevo código
replacement = """
    // Seleccionar datos según modo
    let dataToUse = bibleData;
    if (typeof mormonData !== 'undefined' && currentMode === 'mormon') {
        dataToUse = mormonData;
    }

    const filtered = dataToUse.filter(book => {
        if (currentMode === 'protestant' && book.isDeutero) return false;
"""

if re.search(pattern, content):
    content = re.sub(pattern, replacement.strip(), content)
    print("✓ renderBooks actualizado para usar mormonData")
else:
    print("✗ No se encontró el patrón en renderBooks")

# Guardar
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)
