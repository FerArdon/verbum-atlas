import re

# Leer el archivo
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar donde están los event listeners de navegación
# Vamos a agregar la función goToReference después de switchView

go_to_ref_function = """

    // Función global para navegar a referencias cruzadas
    window.goToReference = function(ref) {
        // Parsear referencia (ej: "Juan.3.16")
        const parts = ref.split('.');
        if (parts.length < 2) return;
        
        const bookName = parts[0];
        const chapter = parseInt(parts[1]);
        
        const book = bibleData.find(b => b.name === bookName);
        
        if (book) {
            openBookMap(book);
            setTimeout(() => loadChapterText(book, chapter), 300);
        }
    };
"""

# Buscar un buen punto de inserción (después de definir switchView o similar)
if 'function switchView' in content or 'switchView(' in content:
    # Buscar el final de la función switchView
    pattern = r'(function switchView\([^)]*\)\s*\{[^}]*\})'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + go_to_ref_function + content[insert_pos:]
        print("✓ Función goToReference agregada después de switchView")
    else:
        # Si no encontramos switchView, buscar otro punto
        # Agregar antes de document.addEventListener
        if 'document.addEventListener' in content:
            content = content.replace('document.addEventListener', go_to_ref_function + '\n    document.addEventListener', 1)
            print("✓ Función goToReference agregada antes de addEventListener")
        else:
            print("⚠ No se pudo encontrar un punto de inserción ideal")
else:
    print("⚠ No se encontró la función switchView")

# Guardar
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Función de navegación agregada")
