import re

with open(r'js\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Definimos la función completa para que no haya errores de pegado
new_function = """
function renderBooks(f, searchTerm = '') {
    if (!booksGrid) return;
    const filteredBooks = bibleData.filter(book => {
        const matchesS = book.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         book.category.toLowerCase().includes(searchTerm.toLowerCase());
        let matchesF = false;
        if (f === 'all') {
            if (currentMode === 'mormon') matchesF = (book.testament === 'mormon');
            else matchesF = (book.testament === 'old' || book.testament === 'new');
        } else {
            matchesF = (book.testament === f);
        }
        return matchesS && matchesF;
    });

    booksGrid.innerHTML = '';
    filteredBooks.forEach(book => {
        const card = document.createElement('div');
        card.className = 'book-card';
        const progress = Math.round(((readData[book.id] || []).length / book.totalChapters) * 100);
        card.innerHTML = `
            <div class="book-info">
                <h3>${book.name}</h3>
                <p>${book.category} • ${book.totalChapters} capítulos</p>
                <div class="progress-bar"><div class="progress-fill" style="width: ${progress}%"></div></div>
            </div>
        `;
        card.onclick = () => showBookDetail(book);
        booksGrid.appendChild(card);
    });
}
"""

# Reemplazamos desde 'function renderBooks' hasta el final de la función (aproximadamente)
# Como la función es larga, usaremos un truco: Reemplazar el bloque de filtrado anterior que era el conflictivo.
# Y asegurarnos que no haya residuos.

# Borrar todo entre 'function renderBooks' y 'booksGrid.innerHTML' (que suele ser el inicio del render)
js = re.sub(r'function renderBooks\(.*?\)\s*\{[\s\S]*?booksGrid\.innerHTML = \'\';', 
            new_function.replace("booksGrid.innerHTML = '';", "booksGrid.innerHTML = '';"), js)

with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✓ renderBooks limpiado y estabilizado.")
