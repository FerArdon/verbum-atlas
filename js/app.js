
// ==========================================
// VERBUM ATLAS 2026 - CORE LOGIC
// ==========================================

let currentMode = 'catholic';
let currentFilter = 'all';
let backend = null;
let readData = {};
try {
    readData = JSON.parse(localStorage.getItem('readData') || '{}');
} catch (e) {
    console.warn('LocalStorage error:', e);
    readData = {};
}

// Elementos UI (se asignan después del DOMContentLoaded)
let booksGrid = null;
let bookDetail = null;
let readerContainer = null;
let versionSelect = null;
let mainSearch = null;

// Inicializar cuando todo esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Asignar elementos del DOM
    booksGrid = document.getElementById('booksGrid');
    bookDetail = document.getElementById('bookDetail');
    readerContainer = document.getElementById('readerContainer');
    versionSelect = document.getElementById('bibleVersion'); // ID CORRECTO
    mainSearch = document.getElementById('searchInput');

    console.log('DOM cargado. BibleData:', typeof bibleData !== 'undefined' ? bibleData.length + ' libros' : 'NO DISPONIBLE');

    // Conectar con backend
    if (typeof qt !== 'undefined') {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            backend = channel.objects.backend;
            window.backend = backend; // Expose to features.js
            console.log("Backend conectado");

            // Cargar estado inicial
            if (versionSelect) {
                currentMode = versionSelect.value;
                backend.setVersion(currentMode);
            }
            renderBooks('all');

            // Inicializar características dependientes del backend
            if (window.initAllFeatures) window.initAllFeatures();
        });
    } else {
        console.log('Backend Qt no disponible, modo web');
        renderBooks('all');
        if (window.initAllFeatures) window.initAllFeatures();
    }

    // Configurar Event Listeners
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
            document.querySelectorAll('.view').forEach(s => s.style.display = 'none');
            if (bookDetail) bookDetail.style.display = 'none';
            if (readerContainer) readerContainer.style.display = 'none';

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
    document.querySelectorAll('.filter-btn').forEach(chip => {
        chip.onclick = () => {
            document.querySelectorAll('.filter-btn').forEach(c => c.classList.remove('active'));
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
            // Actualizar tabla periódica si existe
            if (typeof renderPeriodicTable === 'function') renderPeriodicTable();
        };
    }
}

// 3. RENDERIZADO DE LIBROS
function renderBooks(filter = 'all', searchTerm = '') {
    if (!booksGrid) return;

    // Validar que bibleData existe
    if (typeof bibleData === 'undefined' || !Array.isArray(bibleData) || bibleData.length === 0) {
        booksGrid.innerHTML = '<div style="color: #EF4444; padding: 2rem; text-align: center;"><p>Error: Los datos de la Biblia no están disponibles</p></div>';
        console.error('Error: bibleData no está disponible o está vacío');
        return;
    }

    const safeTerm = searchTerm.trim().toLowerCase();

    const filteredBooks = bibleData.filter(book => {
        const matchesS = book.name.toLowerCase().includes(safeTerm) ||
            book.category.toLowerCase().includes(safeTerm);

        let matchesF = false;
        if (filter === 'all') {
            // Mostrar según el modo actual
            if (currentMode === 'mormon') matchesF = (book.testament === 'mormon');
            else matchesF = (book.testament === 'old' || book.testament === 'new');
        } else if (filter === 'mormon') {
            // Si el filtro es mormon, mostrar solo libros de mormón
            matchesF = (book.testament === 'mormon');
        } else {
            // old o new
            matchesF = (book.testament === filter);
        }

        // Filtro protestante (ocultar deuterocanónicos)
        if (currentMode === 'protestant' && book.isDeutero) return false;

        return matchesS && matchesF;
    });

    booksGrid.innerHTML = '';

    if (filteredBooks.length === 0) {
        booksGrid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:3rem; color:#6B7280;"><p>No se encontraron libros con ese criterio.</p></div>';
        return;
    }

    filteredBooks.forEach(book => {
        const card = document.createElement('div');
        card.className = 'book-card';
        const readCount = (readData[book.id] || []).length;
        const progress = Math.round((readCount / book.totalChapters) * 100);

        // Mapear nombre del libro a imagen de portada
        const coverImage = getCoverImage(book.name);

        card.innerHTML = `
            <div style="height:180px; background:url('${coverImage}') center/cover; position:relative; border-radius:12px 12px 0 0; overflow:hidden;">
                <div style="position:absolute; top:10px; right:10px;">
                    <span style="color:white; font-size:0.75rem; background:rgba(0,0,0,0.6); padding:4px 8px; border-radius:6px; font-weight:600;">
                        ${book.testament === 'mormon' ? 'L.M.' : (book.testament === 'old' ? 'A.T.' : 'N.T.')}
                    </span>
                </div>
            </div>
            <div style="padding:15px;">
                <h3 style="margin:0 0 5px; font-size:1.05rem; color:#1F2937; font-weight:700;">${book.name}</h3>
                <p style="margin:0 0 10px; font-size:0.8rem; color:#6B7280;">${book.category} • ${book.totalChapters} caps</p>
                <div style="background:#E5E7EB; height:4px; border-radius:2px; overflow:hidden;">
                    <div style="width:${progress}%; background:${book.themeColor || '#2563EB'}; height:100%; transition:width 0.3s;"></div>
                </div>
            </div>
        `;

        card.onclick = () => showBookDetail(book);
        booksGrid.appendChild(card);
    });
}

// Función para obtener la imagen de portada según el nombre del libro
function getCoverImage(bookName) {
    // Normalizar nombre del libro para buscar la imagen
    const normalized = bookName.toLowerCase()
        .replace('é', 'e')
        .replace('á', 'a')
        .replace('í', 'i')
        .replace('ó', 'o')
        .replace('ú', 'u')
        .replace('ñ', 'n');

    // Mapeo de nombres de libros a archivos de imagen
    const coverMap = {
        'genesis': 'genesis.jpg',
        'exodo': 'exodo.jpg',
        'levitico': 'levitico.jpg',
        'numeros': 'numeros.jpg',
        'deuteronomio': 'deuteronomio.jpg',
        'josue': 'josue.png',
        'jueces': 'jueces.jpg',
        'rut': 'rut.jpg',
        '1 samuel': '1 samuel.jpg',
        '2 samuel': '2 samuel.jpg',
        '1 reyes': '1 reyes.jpg',
        '2 reyes': '2 reyes.jpg',
        '1 cronicas': '1 cronicas.jpg',
        '2 cronicas': '2 cronicas.jpg',
        'esdras': 'Esdras.jpg',
        'nehemias': 'Nehemías.jpg',
        'tobias': 'tobias.jpg',
        'judit': 'judit.jpg',
        'ester': 'ESTER.jpg',
        '1 macabeos': '1 era MACABEOS.jpg',
        '2 macabeos': '2 da MACABEOS.jpg',
        'job': 'job.jpg',
        'salmos': 'salmos.jpg',
        'proverbios': 'proverbios.jpg',
        'eclesiastes': 'eclesiastés.jpg',
        'cantar de los cantares': 'cantar de los cantares.jpg',
        'sabiduria': 'sabiduria.jpg',
        'eclesiastico': 'eclesiastico.jpg',
        'isaias': 'isaias.jpg',
        'jeremias': 'jeremias.jpg',
        'lamentaciones': 'lamentaciones.jpg',
        'baruc': 'baruc.jpg',
        'ezequiel': 'ezequiel.jpg',
        'daniel': 'daniel.jpg',
        'oseas': 'oseas.jpg',
        'joel': 'joel.jpg',
        'amos': 'amós.jpg',
        'abdias': 'abdias.jpg',
        'jonas': 'jonas.jpg',
        'miqueas': 'miqueas.jpg',
        'nahum': 'nahún.jpg',
        'habacuc': 'habacuc.jpg',
        'sofonias': 'sofonías.jpg',
        'hageo': 'Hageo.jpg',
        'zacarias': 'zacarías.jpg',
        'malaquias': 'malaquias.jpg',
        'mateo': 'mateo.jpg',
        'marcos': 'marcos.jpg',
        'lucas': 'lucas.jpg',
        'juan': 'juan.jpg',
        'hechos': 'hechos.jpg',
        'romanos': 'romanos.jpg',
        '1 corintios': '1 corintios.jpg',
        '2 corintios': '2 corintios.jpg',
        'galatas': 'galatas.jpg',
        'efesios': 'efesios.jpg',
        'filipenses': 'filipenses.jpg',
        'colosenses': 'colosenses.jpg',
        '1 tesalonicenses': '1 tesalonicenses.jpg',
        '2 tesalonicenses': '2 tesalonicenses.jpg',
        '1 timoteo': '1 timoteo.jpg',
        '2 timoteo': '2 timoteo.jpg',
        'tito': 'tito.jpg',
        'filemon': 'filemon.jpg',
        'hebreos': 'hebreos.jpg',
        'santiago': 'santiago.jpg',
        '1 pedro': '1 pedro.jpg',
        '2 pedro': '2 pedro.jpg',
        '1 juan': '1 juan.jpg',
        '2 juan': '2n juan.jpg',
        '3 juan': '3 juan.jpg',
        'judas': 'judas.jpg',
        'apocalipsis': 'apocalipsis.jpg',
        // Libro de Mormón
        '1 nefi': '1 nefi.jpg',
        '2 nefi': '2 nefi.jpg',
        'jacob': 'libro jacob.jpg',
        'enos': 'libro enos.jpg',
        'jarom': 'libro de jarom.jpg',
        'omni': 'libro de omni.jpg',
        'palabras de mormon': 'palabras de mormon.jpg',
        'mosiah': 'libro de mosia.jpg',
        'alma': 'libro de alma.jpg',
        'helaman': 'libro de helaman.jpg',
        '3 nefi': 'tercer (3) nefi.jpg',
        '4 nefi': 'cuarto (4) nefi.jpg',
        'mormon': 'libro mormon.jpg',
        'eter': 'libro de eter.jpg',
        'moroni': 'libro moroni.jpg'
    };

    const imageName = coverMap[normalized] || 'default_cover.jpg';
    return `images/covers/${imageName}`;
}

function showBookDetail(book) {
    document.getElementById('dashboard').style.display = 'none';
    bookDetail.style.display = 'block';

    document.getElementById('detailBookName').innerText = book.name;
    document.getElementById('detailBookInfo').innerText = `${book.category} • ${book.totalChapters} Capítulos`;

    const grid = document.getElementById('chaptersGrid');
    grid.innerHTML = '';

    for (let i = 1; i <= book.totalChapters; i++) {
        const btn = document.createElement('button');
        btn.className = 'chapter-btn';
        btn.innerText = i;

        if ((readData[book.id] || []).includes(i)) {
            btn.classList.add('completed');
        }

        btn.onclick = () => openReader(book, i);
        grid.appendChild(btn);
    }
}

function openReader(book, chapter) {
    bookDetail.style.display = 'none';
    readerContainer.style.display = 'block';

    document.getElementById('readerTitle').innerText = `${book.name} ${chapter}`;
    const contentDiv = document.getElementById('verseContent');
    contentDiv.innerHTML = '<div style="text-align:center; padding:20px; color:#6B7280;">Cargando Sagradas Escrituras...</div>';

    if (backend) {
        backend.getChapterText(book.name, chapter, (response) => {
            const data = JSON.parse(response);

            if (data.error) {
                contentDiv.innerHTML = `<div style="color:red;">Error: ${data.error}</div>`;
            } else {
                let html = '';
                data.forEach(v => {
                    // Limpieza profunda de texto
                    let cleanText = v.text
                        // Eliminar referencias GEE y notas al pie comunes
                        .replace(/GEE/g, '')
                        // Eliminar referencias tipo [a], [b], o letras sueltas que indican notas (e.g., "y aconteció^a que")
                        // Esto es agresivo, tener cuidado. En español BoM suele tener letras voladas o superindices, aquí asumimos texto plano.
                        // Eliminar referencias cruzadas "a Mos. 1:2", "Véase..."
                        .replace(/[a-z]\s[A-Z][a-z]+\.\s*\d+:\d+([–-]\d+)?/g, '')
                        .replace(/Véase también.*/gi, '')
                        .replace(/Véase.*/gi, '')
                        // Eliminar números sueltos que no sean el versículo
                        //.replace(/\b\d+\b/g, '') // Arriesgado si hay números legítimos en el texto
                        .trim();

                    // Limpieza adicional de espacios dobles
                    cleanText = cleanText.replace(/\s+/g, ' ');

                    html += `
                        <div style="margin-bottom:15px; display:flex; gap:15px;">
                            <span style="color:#2563EB; font-weight:bold; min-width:30px; font-family:'Outfit';">${v.verse}</span>
                            <span style="color:#374151; font-family:'Charter', 'Georgia', serif; font-size:1.15rem;">${cleanText}</span>
                        </div>
                    `;
                });
                contentDiv.innerHTML = html;
            }
        });
    } else {
        contentDiv.innerHTML = '<div style="text-align:center; padding:40px; color:#6B7280;"><p><i class="fa-solid fa-info-circle" style="font-size:2rem; margin-bottom:10px; color:#2563EB;"></i></p><p>Para leer los versículos, ejecuta la aplicación con:</p><code style="background:#f3f4f6; padding:10px; border-radius:8px; display:inline-block; margin-top:10px;">python run_app.py</code></div>';
    }
}

// 4. LEX DIVINA (CHAT IA)
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

    // Parseo de Markdown Mejorado
    let formattedText = text
        // Primero convertir \n literal (string) a saltos de línea reales
        .replace(/\\n/g, '\n')
        // Encabezados ### (antes que ##)
        .replace(/^### (.*?)$/gm, '<h4 style="margin:10px 0; color:#4B5563;">$1</h4>')
        // Encabezados ##
        .replace(/^## (.*?)$/gm, '<h3 style="margin:12px 0; color:#374151;">$1</h3>')
        // Separadores ---
        .replace(/^---$/gm, '<hr style="border:none; border-top:1px solid #E5E7EB; margin:15px 0;">')
        // Blockquotes >
        .replace(/^> (.*?)$/gm, '<blockquote style="border-left:3px solid #8B5CF6; padding-left:12px; margin:10px 0; color:#6B7280; font-style:italic;">$1</blockquote>')
        // Listas (guiones o asteriscos al inicio de línea)
        .replace(/^[\-\*]\s(.*?)$/gm, '<li>$1</li>')
        // Listas numeradas
        .replace(/^\d+\.\s(.*?)$/gm, '<li>$1</li>')
        // Negrita
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Cursiva
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Convertir saltos de línea en <br>
        .replace(/\n/g, '<br>');

    // Envolver listas si existen
    if (formattedText.includes('<li>')) {
        formattedText = formattedText.replace(/((<li>.*<\/li>)+)/s, '<ul style="margin:10px 0; padding-left:20px;">$1</ul>');
    }


    msg.innerHTML = `<div style="display:inline-block; max-width:85%; padding:14px; border-radius:12px; background:${isUser ? '#8B5CF6' : '#FFFFFF'}; color:${isUser ? 'white' : '#374151'}; line-height:1.6; box-shadow:0 2px 4px rgba(0,0,0,0.05); text-align:left;">${formattedText}</div>`;
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

// 5. CONFIGURACIÓN DE API KEY
function setupApiKeyUI() {
    const toggleBtn = document.getElementById('toggleApiKeyBtn');
    const configPanel = document.getElementById('apiKeyConfig');

    if (toggleBtn && configPanel) {
        toggleBtn.onclick = () => {
            const isHidden = configPanel.style.display === 'none';
            configPanel.style.display = isHidden ? 'block' : 'none';
            toggleBtn.textContent = isHidden ? '🔒 Ocultar' : '⚙️ Configurar API Key Gemini';
        };
    }
}

// Función global para guardar API Key
window.saveApiKey = () => {
    const input = document.getElementById('geminiInput');
    if (!input) return;

    const key = input.value.trim();
    if (!key) {
        alert('Por favor ingresa una API Key válida');
        return;
    }

    if (backend) {
        backend.setApiKey(key);
        alert('✅ API Key configurada correctamente');
        input.value = '';
        document.getElementById('apiKeyConfig').style.display = 'none';
        document.getElementById('toggleApiKeyBtn').textContent = '⚙️ Configurar API Key Gemini';
    } else {
        alert('⚠️ Backend no conectado. Ejecuta: python run_app.py');
    }
};

// Llamar setupApiKeyUI después de que el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupApiKeyUI);
} else {
    setupApiKeyUI();
}
