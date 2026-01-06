import re
import codecs

# Leer app.js original (recién restaurado)
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ==========================================
# 1. ARREGLAR REFERENCIAS CRUZADAS (Quitar fetch)
# ==========================================
content = content.replace("let crossReferences = {};", "// let crossReferences = {}; // Cargado externamente")
content = re.sub(r"fetch\('cross_references.json'\)[\s\S]*?console\.log\('Referencias cruzadas no disponibles:', err\)\);", 
                 "// Referencias cargadas via script externo", content)

# ==========================================
# 2. INYECTAR DATOS MORMONES
# ==========================================
mormon_data = """
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
# Insertar después de bibleData
content = re.sub(r'(const bibleData\s*=\s*\[[\s\S]*?\];)', r'\1' + mormon_data, content)

# ==========================================
# 3. ACTUALIZAR RENDERBOOKS
# ==========================================
# Reemplazar lógica de filtrado
render_replacement = """
    // Seleccionar datos según modo
    let dataToUse = bibleData;
    if (typeof mormonData !== 'undefined' && currentMode === 'mormon') {
        dataToUse = mormonData;
    }

    const filtered = dataToUse.filter(book => {
        if (currentMode === 'protestant' && book.isDeutero) return false;
"""
pattern_render = r'const filtered = bibleData\.filter\(book => \{[\s\S]*?if \(currentMode === \'protestant\' && book\.isDeutero\) return false;'
if re.search(pattern_render, content):
    content = re.sub(pattern_render, render_replacement.strip(), content)

# Actualizar lógica de portada por defecto en renderBooks
content = content.replace("const defCover = book.testament === 'new' ? `images/covers/default_new.jpg` : `images/covers/moises.png`;",
                          "let defCover = `images/covers/moises.png`; if (book.testament === 'new') defCover = `images/covers/default_new.jpg`; if (book.testament === 'mormon') defCover = `images/covers/mormon_default.jpg`;")

# ==========================================
# 4. PORTADAS ESPECIALES
# ==========================================
mormon_covers = """
        "1nefi": "1 nefi.jpg", "2nefi": "2 nefi.jpg", "jacob": "libro jacob.jpg", "enos": "libro enos.jpg",
        "jarom": "libro de jarom.jpg", "omni": "libro de omni.jpg", "palabras": "palabras de mormon.jpg",
        "mosiah": "libro de mosia.jpg", "alma": "libro de alma.jpg", "helaman": "libro de helaman.jpg",
        "3nefi": "tercer (3) nefi.jpg", "4nefi": "cuarto (4) nefi.jpg", "mormon": "libro mormon.jpg",
        "eter": "libro de eter.jpg", "moroni": "libro moroni.jpg",
"""
content = content.replace('"exodo": "exodo.jpg",', mormon_covers + '        "exodo": "exodo.jpg",')

# ==========================================
# 5. REPARAR OPENBOOKMAP (Wrapper global + setAttribute)
# ==========================================
# Primero agregamos el wrapper al final
wrapper_func = """
// Wrapper global para abrir capítulos
window.openChapterWrapper = function(bookId, chapter) {
    let book = bibleData.find(b => b.id === bookId);
    if (!book && typeof mormonData !== 'undefined') {
        book = mormonData.find(b => b.id === bookId);
    }
    if (book) loadChapterText(book, chapter);
};
"""
content += "\n" + wrapper_func

# Modificar openBookMap para usar setAttribute
# Buscamos la función openBookMap y reemplazamos la línea del onclick interno
pattern_open_map = r'(function openBookMap\(book\) \{[\s\S]*?)btn\.onclick = \(\) => loadChapterText\(book, i\);'
replacement_open_map = r'\1btn.setAttribute("onclick", `window.openChapterWrapper("${book.id}", ${i})`);'
content = re.sub(pattern_open_map, replacement_open_map, content)

# ==========================================
# 6. INYECTAR goToReference (Para cross refs)
# ==========================================
goto_func = """
window.goToReference = function(ref) {
    const parts = ref.split(".");
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
content += "\n" + goto_func

# Guardar
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Parche maestro aplicado correctamente.")
