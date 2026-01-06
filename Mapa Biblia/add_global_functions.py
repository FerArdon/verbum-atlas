import codecs

# Código JavaScript a agregar
js_code = """

// Funciones globales para navegación y mapas
window.goToReference = function(ref) {
    // Parsear referencia (ej: "Juan.3.16")
    const parts = ref.split(".");
    if (parts.length < 2) return;
    
    const bookName = parts[0];
    const chapter = parseInt(parts[1]);
    
    // Buscar el libro en la data actual
    const book = bibleData.find(b => b.name === bookName);
    
    if (book) {
        openBookMap(book);
        setTimeout(() => loadChapterText(book, chapter), 300);
    }
};

window.openMapModal = function(imagePath, title) {
    const modal = document.getElementById("mapModal");
    const modalImg = document.getElementById("mapModalImg");
    const modalTitle = document.getElementById("mapModalTitle");
    
    if (modal && modalImg && modalTitle) {
        modalImg.src = imagePath;
        modalTitle.textContent = title;
        modal.style.display = "flex";
    }
};
"""

file_path = r'js\app.js'

try:
    with codecs.open(file_path, 'a', encoding='utf-8') as f:
        f.write(js_code)
    print("✓ Funciones globales agregadas correctamente a js/app.js")
except Exception as e:
    print(f"Error al escribir en el archivo: {e}")
