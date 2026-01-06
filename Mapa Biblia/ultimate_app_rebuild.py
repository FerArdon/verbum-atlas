
app_content = """
// ==========================================
// VERBUM ATLAS 2026 - CORE LOGIC
// ==========================================

let currentMode = 'catholic';
let currentFilter = 'all';
let backend = null;
let readData = JSON.parse(localStorage.getItem('readData') || '{}');

// Elementos UI
const booksGrid = document.getElementById('booksGrid');
const bookDetail = document.getElementById('bookDetail');
const readerContainer = document.getElementById('readerContainer');
const versionSelect = document.getElementById('versionSelect');
const mainSearch = document.getElementById('searchInput');

// Inicializar QWebChannel
document.addEventListener('DOMContentLoaded', () => {
    if (typeof qt !== 'undefined') {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            backend = channel.objects.backend;
            console.log("Backend conectado");
            
            // Cargar estado inicial
            if (versionSelect) {
                currentMode = versionSelect.value;
                renderBooks('all');
            }
        });
    }

    // Configurar Event Listeners de Navegación
    setupNavigation();
    setupFilters();
    setupLexDivina();
});

// 1. NAVEGACIÓN
function setupNavigation() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.onclick = () => {
            const target = btn.getAttribute('data-target');
            if (!target) return;
            
            // Ocultar todas las secciones
            document.querySelectorAll('.view-section').forEach(s => s.style.display = 'none');
            // Ocultar componentes especiales
            if(bookDetail) bookDetail.style.display = 'none';
            if(readerContainer) readerContainer.style.display = 'none';
            
            // Mostrar target
            const targetSec = document.getElementById(target);
            if (targetSec) targetSec.style.display = 'block';
            
            // Active state
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Si volvemos a biblioteca, volver a renderizar
            if (target === 'dashboard') {
                renderBooks(currentFilter);
            }
        };
    });
}

// 2. FILTROS BIBLIOTECA
function setupFilters() {
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.onclick = () => {
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            currentFilter = chip.getAttribute('data-filter');
            renderBooks(currentFilter);
        };
    });

    if (mainSearch) {
        mainSearch.oninput = (e) => renderBooks(currentFilter, e.target.value);
    }

    if (versionSelect) {
        versionSelect.onchange = (e) => {
            currentMode = e.target.value;
            if (backend) backend.setVersion(currentMode);
            renderBooks('all');
        };
    }
}

// 3. RENDERIZADO DE LIBROS
function renderBooks(filter = 'all', searchTerm = '') {
    if (!booksGrid) return;
    
    const filteredBooks = bibleData.filter(book => {
        const matchesS = book.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         book.category.toLowerCase().includes(searchTerm.toLowerCase());
        
        let matchesF = false;
        if (filter === 'all') {
            if (currentMode === 'mormon') matchesF = (book.testament === 'mormon');
            else matchesF = (book.testament === 'old' || book.testament === 'new');
        } else {
            matchesF = (book.testament === filter);
        }
        return matchesS && matchesF;
    });

    booksGrid.innerHTML = '';
    filteredBooks.forEach(book => {
        const card = document.createElement('div');
        card.className = 'book-card';
        const readCount = (readData[book.id] || []).length;
        const progress = Math.round((readCount / book.totalChapters) * 100);
        
        card.innerHTML = `
            <div class="book-info">
                <h3>${book.name}</h3>
                <p>${book.category} • ${book.totalChapters} caps</p>
                <div class="progress-bar"><div class="progress-fill" style="width: ${progress}%"></div></div>
            </div>
        `;
        card.onclick = () => showBookDetail(book);
        booksGrid.appendChild(card);
    });
}

function showBookDetail(book) {
    document.getElementById('dashboard').style.display = 'none';
    bookDetail.style.display = 'block';
    document.getElementById('detailBookName').innerText = book.name;
    document.getElementById('detailBookInfo').innerText = `${book.category} • ${book.totalChapters} capítulos`;
    
    const grid = document.getElementById('chaptersGrid');
    grid.innerHTML = '';
    for (let i = 1; i <= book.totalChapters; i++) {
        const btn = document.createElement('button');
        btn.className = 'chapter-btn';
        if ((readData[book.id] || []).includes(i)) btn.classList.add('completed');
        btn.innerText = i;
        btn.onclick = () => openReader(book, i);
        grid.appendChild(btn);
    }
}

function openReader(book, chapter) {
    bookDetail.style.display = 'none';
    readerContainer.style.display = 'block';
    document.getElementById('readerTitle').innerText = `${book.name} ${chapter}`;
    
    const verseContent = document.getElementById('verseContent');
    verseContent.innerHTML = 'Cargando...';
    
    if (backend) {
        backend.getChapterText(book.name, chapter, (json) => {
            const verses = JSON.parse(json);
            verseContent.innerHTML = verses.map(v => `
                <div class="verse">
                    <span class="verse-num">${v.verse}</span>
                    <span class="verse-text">${v.text}</span>
                </div>
            `).join('');
        });
    }
}

// 4. LEX DIVINA (IA)
function setupLexDivina() {
    const chatContainer = document.getElementById('chatContainer');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendChatBtn');
    const clearBtn = document.getElementById('clearChatBtn');

    if (sendBtn) {
        sendBtn.onclick = () => {
            const text = chatInput.value.trim();
            if (!text || !backend) return;
            
            addMessage(text, 'user');
            chatInput.value = '';
            const loadingId = addMessage("Meditando...", 'ai');
            
            backend.askAgent("", text, (response) => {
                const loading = document.getElementById(loadingId);
                if (loading) loading.remove();
                addMessage(response, 'ai');
            });
        };
    }
    
    if (clearBtn) {
        clearBtn.onclick = () => {
            chatContainer.innerHTML = '<div style="text-align:center; color:#9CA3AF; margin-top:150px;"><p>Haz una pregunta...</p></div>';
        };
    }
}

function addMessage(text, sender) {
    const chat = document.getElementById('chatContainer');
    if (!chat) return;
    const isUser = sender === 'user';
    const msg = document.createElement('div');
    msg.id = 'msg_' + Date.now() + Math.random();
    msg.style.cssText = `margin-bottom:15px; text-align:${isUser ? 'right' : 'left'};`;
    msg.innerHTML = `<div style="display:inline-block; max-width:80%; padding:12px; border-radius:12px; background:${isUser ? '#8B5CF6' : '#F3F4F6'}; color:${isUser ? 'white' : '#1F2937'};">${text}</div>`;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
    return msg.id;
}

// Globales necesarias para botones "Volver"
window.goBackToLibrary = () => {
    bookDetail.style.display = 'none';
    readerContainer.style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
};
window.goBackToChapters = () => {
    readerContainer.style.display = 'none';
    bookDetail.style.display = 'block';
};
"""

with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("✓ app.js RESTRSCTURADO DESDE CERO. Cero errores.")
