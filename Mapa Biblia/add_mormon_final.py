import re

# Leer el archivo
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Definir datos mormones
mormon_data_code = """
// Datos del Libro de Mormón
const mormonData = [
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
];
"""

# Agregar mormonData si no existe
if 'const mormonData' not in content:
    # Insertar después de bibleData]
    content = re.sub(r'(const bibleData\s*=\s*\[[\s\S]*?\];)', r'\1' + mormon_data_code, content)
    print("✓ Datos del Libro de Mormón agregados")

# 2. Actualizar renderBooks para usar los datos correctos
render_update = """
    let dataToRender = bibleData;
    if (currentMode === 'mormon') {
        dataToRender = mormonData;
    }

    const filtered = searchTerm 
        ? dataToRender.filter(b => b.name.toLowerCase().includes(searchTerm.toLowerCase()))
        : dataToRender;
"""

# Reemplazar la lógica de filtrado inicial en renderBooks
pattern_render = r'const filtered = searchTerm\s*\?\s*bibleData\.filter[\s\S]*?: bibleData;'
if re.search(pattern_render, content):
    content = re.sub(pattern_render, render_update, content)
    print("✓ renderBooks actualizado para soportar modo Mormón")
else:
    print("⚠ No se encontró el patrón de renderBooks")

# Guardar
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)
