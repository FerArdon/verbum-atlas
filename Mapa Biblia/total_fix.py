import os

# 1. ARREGLAR INDEX.HTML (Limpieza total de botones y filtros)
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Asegurar que Lex Divina esté en el menú lateral y NO haya duplicados
# Buscamos la lista de botones y la reconstruimos si es necesario
nav_pattern = r'<nav[^>]*>([\s\S]*?)</nav>'
def fix_nav(match):
    nav_content = match.group(1)
    # Lista limpia de botones que queremos
    buttons = [
        ('<button class="nav-btn" data-target="dailyPlan"><span class="icon">📅</span> Plan Diario</button>', 'dailyPlan'),
        ('<button class="nav-btn" data-target="dashboard"><span class="icon">📚</span> Biblioteca</button>', 'dashboard'),
        ('<button class="nav-btn" data-target="panorama"><span class="icon">🌍</span> Panorama</button>', 'panorama'),
        ('<button class="nav-btn" data-target="lexDivina"><span class="icon">✨</span> Lex Divina</button>', 'lexDivina'),
        ('<button class="nav-btn" data-target="myJournal"><span class="icon">🧘</span> Mi Diario</button>', 'myJournal'),
        ('<button class="nav-btn" data-target="freeNotes"><span class="icon">📝</span> Mis Apuntes</button>', 'freeNotes'),
        ('<button class="nav-btn" data-target="studyPlan"><span class="icon">📈</span> Mi Progreso</button>', 'studyPlan')
    ]
    new_nav = "\n"
    for btn_html, target in buttons:
        new_nav += f"                {btn_html}\n"
    return f"<nav class=\"nav-menu\">{new_nav}            </nav>"

html = re.sub(nav_pattern, fix_nav, html)

# Asegurar Filtro L.M. en la cabecera de biblioteca
filter_pattern = r'<div class="filter-chips">([\s\S]*?)</div>'
def fix_filters(match):
    return """<div class="filter-chips">
                    <button class="filter-chip active" data-filter="all">Todos</button>
                    <button class="filter-chip" data-filter="old">A.T.</button>
                    <button class="filter-chip" data-filter="new">N.T.</button>
                    <button class="filter-chip" data-filter="mormon">L.M.</button>
                </div>"""
import re
html = re.sub(filter_pattern, fix_filters, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. ARREGLAR APP.JS (Reemplazo total de la lógica de filtrado)
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Reemplazamos la función renderBooks completa para evitar errores de llaves
# Buscamos el inicio de renderBooks y el final del bloque de filtrado
render_pattern = r'function renderBooks\(filter, searchTerm\) \{([\s\S]*?)const filteredBooks = bibleData\.filter\(book => \{([\s\S]*?)\}\);'

new_render_body = """
function renderBooks(f, searchTerm) {
    if (!booksGrid) return;
    currentFilter = f;
    
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
"""

# Implementación más simple: Reemplazar el bloque de filtro por uno limpio
js = re.sub(r'const filteredBooks = bibleData\.filter\(book => \{[\s\S]*?\}\);', 
            payload := """const filteredBooks = bibleData.filter(book => {
        const nameMatch = book.name.toLowerCase().includes(searchTerm.toLowerCase());
        const catMatch = book.category.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesS = nameMatch || catMatch;
        
        let matchesF = false;
        if (filter === 'all') {
            if (currentMode === 'mormon') matchesF = (book.testament === 'mormon');
            else matchesF = (book.testament === 'old' || book.testament === 'new');
        } else {
            matchesF = (book.testament === filter);
        }
        return matchesS && matchesF;
    });""", js)

with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✓ Sistema restaurado y limpio.")
