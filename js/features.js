
// ==========================================
// VERBUM ATLAS 2026 - FUNCIONALIDADES EXTRA
// ==========================================

// 5. PANORAMA
// 5. PANORAMA
function initPanorama() {
    console.log('Iniciando carga de Panorama...');

    // Inicializar listeners de tabs si no existen
    if (!window.showPanoramaTab) {
        window.showPanoramaTab = (tabName) => {
            document.querySelectorAll('.panorama-content').forEach(el => el.style.display = 'none');
            document.getElementById('tab-' + tabName).style.display = 'block';

            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            // Buscar el botón correspondiente
            const buttons = Array.from(document.querySelectorAll('.tab-btn'));
            const btn = buttons.find(b => b.textContent.toLowerCase().includes(tabName === 'structure' ? 'tabla' : 'cronología'));
            if (btn) btn.classList.add('active');
        };
    }

    renderPeriodicTable();

    // Cronología (Timeline) - Solo generar si está vacío para evitar duplicados si se llama initPanorama varias veces
    const timelineContainer = document.querySelector('.timeline-visual');
    // Verificamos si tiene elementos "generados" (no los estáticos del HTML si los hubiera)
    // En el HTML original ya había eventos estáticos, pero la función anterior los sobreescribía.
    // Vamos a respetar lo que haya en HTML si ya está bien, o regenerar si es necesario.
    // En este caso, el HTML que vimos en index.html TIENE eventos estáticos.
    // Así que NO necesitamos inyectarlos vía JS salvo que queramos dinamismo.
    // Dejaremos la lógica de inyección condicional por si se borraron.
    if (timelineContainer && timelineContainer.children.length <= 1) { // <=1 asumiendo que pueda haber algún div vacío o comentario
        const events = [
            { year: "4000 AC", title: "La Creación", desc: "Dios crea el cielo y la tierra." },
            { year: "2000 AC", title: "Llamado de Abraham", desc: "Dios hace un pacto con Abraham." },
            { year: "1446 AC", title: "El Éxodo", desc: "Moisés saca al pueblo de Egipto." },
            { year: "1000 AC", title: "Reinado de David", desc: "Israel se convierte en una potencia." },
            { year: "586 AC", title: "El Exilio", desc: "Jerusalén es destruida por Babilonia." },
            { year: "0", title: "Nacimiento de Jesús", desc: "El Verbo se hace carne." },
            { year: "33 DC", title: "La Cruz y Resurrección", desc: "La victoria sobre la muerte." },
            { year: "90 DC", title: "Apocalipsis", desc: "La revelación final a Juan." }
        ];

        timelineContainer.innerHTML = events.map(e => `
            <div class="timeline-event">
                <div class="t-dot" style="background:var(--primary)"></div>
                <div style="font-weight:bold; color:var(--primary); margin-bottom:4px;">${e.year}</div>
                <h4>${e.title}</h4>
                <p>${e.desc}</p>
            </div>
        `).join('');
    }
}

window.renderPeriodicTable = () => {
    const tableContainer = document.getElementById('periodicTable');
    if (!tableContainer) return;

    // Verificar si bibleData existe
    if (typeof bibleData === 'undefined') {
        tableContainer.innerHTML = '<p>Cargando datos...</p>';
        return;
    }

    // Definir orden de categorías
    const categoryOrder = [
        "Pentateuco", "Históricos", "Sapienciales", "Profetas Mayores", "Profetas Menores", // AT
        "Evangelios", "Históricos", // Hechos está como Históricos en data.js, ojo con duplicados de nombre de cat
        "Cartas de Pablo", "Cartas Generales", "Profecía", // NT
        // Libro de Mormón
        "Libro de Nefi", "Libro de Jacob", "Libro de Enós", "Libro de Jarom", "Libro de Omni", "Palabras de Mormón",
        "Libro de Mosíah", "Libro de Alma", "Libro de Helamán", "Libro de Mormón", "Libro de Éter", "Libro de Moroni"
    ];

    // Filtrar libros según modo actual
    let mode = 'catholic';
    if (typeof currentMode !== 'undefined') mode = currentMode;

    const visibleBooks = bibleData.filter(book => {
        if (mode === 'mormon') return book.testament === 'mormon';
        if (mode === 'protestant') return (book.testament === 'old' || book.testament === 'new') && !book.isDeutero;
        // Catholic (default)
        return (book.testament === 'old' || book.testament === 'new');
    });

    if (visibleBooks.length === 0) {
        tableContainer.innerHTML = '<p>No hay libros para mostrar en esta versión.</p>';
        return;
    }

    // Agrupar libros
    // Nota: "Históricos" aparece en AT y NT. Para separarlos visualmente en la tabla periódica podríamos necesitar lógica extra,
    // o aceptar que salgan separados si el orden de categorías agrupa por nombre. 
    // Como visibleBooks mantiene el orden canónico (generalmente), agrupar por categoría preservando el orden de aparición es mejor.

    // Algoritmo de agrupación preservando orden de aparición (para separar Históricos AT de Históricos NT)
    const groups = [];
    let currentGroup = null;

    visibleBooks.forEach(book => {
        // Un pequeño hack para distinguir Históricos AT de NT si tienen el mismo nombre de categoría
        let catName = book.category;

        // Si no hay grupo actual o la categoría cambia (o cambia de testamento para la misma categoría, aunque raro)
        if (!currentGroup || currentGroup.name !== catName || (catName === 'Históricos' && currentGroup.testament !== book.testament)) {
            currentGroup = {
                name: catName,
                testament: book.testament,
                color: book.themeColor || '#666',
                books: []
            };
            groups.push(currentGroup);
        }
        currentGroup.books.push(book);
    });

    // Generar HTML
    // Usamos display grid o flex para las columnas
    let tableHtml = `<div style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 20px; align-items: flex-start;">`;

    groups.forEach(group => {
        tableHtml += `
            <div style="display: flex; flex-direction: column; gap: 6px; min-width: 70px;">
                <div style="font-size: 0.75rem; font-weight: bold; color: #4B5563; text-align: center; border-bottom: 3px solid ${group.color}; padding-bottom: 4px; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${group.name}">
                    ${group.name.replace('Cartas de ', '').replace('Profetas ', '')}
                </div>
                ${group.books.map(book => {
            // Abreviatura
            let abbr = book.id.substring(0, 3).toUpperCase();
            // Ajustes manuales
            const manualAbbr = {
                '1samuel': '1SA', '2samuel': '2SA', '1reyes': '1RE', '2reyes': '2RE',
                '1cronicas': '1CR', '2cronicas': '2CR', 'cantardeloscantares': 'CNT',
                '1corintios': '1CO', '2corintios': '2CO', '1tesalonicenses': '1TE',
                '2tesalonicenses': '2TE', '1timoteo': '1TI', '2timoteo': '2TI',
                '1pedro': '1PE', '2pedro': '2PE', '1juan': '1JN', '2juan': '2JN',
                '3juan': '3JN', 'filemon': 'FLM', 'nahum': 'NAH', 'sofonias': 'SOF',
                'judit': 'JUD', 'tobias': 'TOB'
            };
            if (manualAbbr[book.id]) abbr = manualAbbr[book.id];

            return `
                    <div onclick="showBookDetailById('${book.id}')" 
                         style="background-color: ${group.color}; color: white; width: 100%; aspect-ratio: 1; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
                         onmouseover="this.style.transform='scale(1.1)'; this.style.zIndex='10';" 
                         onmouseout="this.style.transform='scale(1)'; this.style.zIndex='1';"
                         title="${book.name}">
                        ${abbr}
                    </div>
                `;
        }).join('')}
            </div>
        `;
    });

    tableHtml += `</div>`;
    tableContainer.innerHTML = tableHtml;
};

// Helper necesario para onclicks generados dinámicamente
window.showBookDetailById = (bookId) => {
    const dashboard = document.getElementById('dashboard');
    const bookDetail = document.getElementById('bookDetail');
    const panorama = document.getElementById('panorama');

    // Asumimos que showBookDetail existe (en app.js)
    const book = bibleData.find(b => b.id === bookId);
    if (book && typeof showBookDetail === 'function') {
        if (panorama) panorama.style.display = 'none';
        if (bookDetail) bookDetail.style.display = 'block';
        showBookDetail(book);
    }
};

// 6. PLAN DIARIO
function initDailyPlan() {
    const dateEl = document.getElementById('dailyPlanDate');
    const container = document.getElementById('dailyPlanContainer');
    if (!dateEl || !container) return;

    const today = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateEl.textContent = today.toLocaleDateString('es-ES', options);

    // ISO Date local para backend
    const isoDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

    // 1. VERIFICAR ESTADO (Zen Mode)
    if (window.backend) {
        window.backend.checkDailyStatus(isoDate, (response) => {
            try {
                const res = JSON.parse(response);
                if (res.status === 'CLOSED') {
                    renderDailyGrid(container, today);
                    // Pequeño timeout para asegurar que el DOM se pintó antes de buscar elementos
                    setTimeout(() => applyCompletedState(), 50);
                } else {
                    renderDailyGrid(container, today);
                }
            } catch (e) {
                console.error("Error checking status", e);
                renderDailyGrid(container, today);
            }
        });
    } else {
        renderDailyGrid(container, today);
    }
}


function applyCompletedState() {
    // Buscar inputs y deshabilitarlos
    const inputs = document.querySelectorAll('#devoGratitude, #devoPrayer, #devoCommitment');
    inputs.forEach(input => {
        input.disabled = true;
        input.style.backgroundColor = '#f3f4f6';
        input.style.color = '#9ca3af';
    });

    // Buscar botón y cambiar estado
    const btn = document.getElementById('finishDayBtn');
    if (btn) {
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Día Completado';
        btn.disabled = true;
        btn.style.background = '#10B981';
        btn.style.cursor = 'default';
        btn.style.transform = 'none';
        btn.onclick = null;
    }
}


function renderDailyGrid(container, today) {
    // 1. CONFIGURACIÓN DEL LAYOUT (Flexbox vertical: Fila superior + Fila inferior)
    container.style.display = 'flex';
    container.style.flexDirection = 'column';
    container.style.gap = '30px';
    container.innerHTML = '';

    const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 86400000);
    const todayKey = `devotional_${today.getFullYear()}_${today.getMonth()}_${today.getDate()}`;

    // === FILA SUPERIOR: LECTURAS + DEVOCIONAL (Lado a Lado) ===
    const topRow = document.createElement('div');
    topRow.className = 'top-row-actions';
    topRow.style.cssText = `
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 50px;
        width: 100%;
        box-sizing: border-box;
        align-items: start;
    `;

    // BLOQUE 1: LECTURAS DE HOY (Izquierda)
    const colReadings = document.createElement('div');
    colReadings.style.cssText = 'width: 100%;'; // Grid item fills cell
    colReadings.innerHTML = '<h3 style="color:#1F2937; margin:0 0 15px 0; font-family:\'Outfit\';"><i class="fa-solid fa-book-open"></i> Lecturas de Hoy</h3>';

    // Lógica simple de lectura
    const rOld = calculateReading(dayOfYear, 'old', 3);
    const rNew = calculateReading(dayOfYear, 'new', 1);

    colReadings.innerHTML += createReadingCard("Antiguo Testamento", rOld, "#8B5CF6");
    colReadings.innerHTML += createReadingCard("Nuevo Testamento", rNew, "#EF4444");

    if (typeof currentMode !== 'undefined' && currentMode === 'mormon') {
        const rMormon = calculateReading(dayOfYear, 'mormon', 1);
        colReadings.innerHTML += createReadingCard("Libro de Mormón", rMormon, "#F59E0B");
    }

    // BLOQUE 2: MI DEVOCIONAL (Derecha)
    const colMyDevo = document.createElement('div');
    colMyDevo.style.cssText = 'width: 100%;'; // Grid item fills cell
    colMyDevo.innerHTML = '<h3 style="color:#1F2937; margin:0 0 15px 0; font-family:\'Outfit\';"><i class="fa-solid fa-heart" style="color:#EC4899;"></i> Mi Devocional</h3>';

    const inputsCard = document.createElement('div');
    inputsCard.style.cssText = `
        background: white; 
        border-radius: 16px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        padding: 25px; 
        border-top: 5px solid #10B981;
    `;

    const inputStyle = "width:100%; padding:12px; border:1px solid #E5E7EB; border-radius:8px; margin-bottom:20px; font-family:'Outfit'; font-size:0.95rem; background:#F9FAFB; display:block; box-sizing:border-box;";
    const labelStyle = "display:block; font-weight:600; font-size:0.9rem; color:#374151; margin-bottom:8px;";

    inputsCard.innerHTML = `
        <label style="${labelStyle}">Doy gracias por...</label>
        <textarea id="devoGratitude" style="${inputStyle} height:80px; resize:none;" placeholder="Escribe aquí..."></textarea>

        <label style="${labelStyle}">Petición de Oración</label>
        <textarea id="devoPrayer" style="${inputStyle} height:80px; resize:none;" placeholder="Escribe aquí..."></textarea>

        <label style="${labelStyle}">Compromiso del Día</label>
        <input type="text" id="devoCommitment" style="${inputStyle}" placeholder="Hoy me comprometo a...">

        <div style="text-align:right; font-size:0.75rem; color:#10B981; margin-top:-10px; margin-bottom:20px;">
            <i class="fa-solid fa-check-circle"></i> Guardado automático
        </div>
    `;
    colMyDevo.appendChild(inputsCard);

    topRow.appendChild(colReadings);
    topRow.appendChild(colMyDevo);
    container.appendChild(topRow);


    // === FILA INFERIOR: LECTURA MATUTINA (Centrada) ===
    const bottomRow = document.createElement('div');
    bottomRow.className = 'bottom-row-reading';
    bottomRow.style.cssText = `
        display: flex; 
        justify-content: center; 
        margin-top: 20px;
    `;

    const colDevotional = document.createElement('div');
    colDevotional.style.cssText = 'width: 100%; max-width: 900px;';
    colDevotional.innerHTML = '<h3 style="color:#1F2937; margin:0 0 15px 0; font-family:\'Outfit\';"><i class="fa-regular fa-sun" style="color:#F59E0B;"></i> Lectura Matutina</h3>';

    const devBox = document.createElement('div');
    devBox.id = 'dailyDevotionalContent';
    devBox.style.cssText = `
        background: white; 
        border-radius: 16px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        padding: 40px; 
        min-height: 300px; 
        border-top: 5px solid #F59E0B;
        font-family: 'Charter', 'Georgia', serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #374151;
    `;
    devBox.innerHTML = '<div style="text-align:center; padding-top:60px; color:#aaa;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i><br>Cargando reflexión...</div>';

    colDevotional.appendChild(devBox);
    bottomRow.appendChild(colDevotional);
    container.appendChild(bottomRow);


    // Fetch y manejo de datos de lectura matutina
    const months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
    const monthName = months[today.getMonth()];
    const day = today.getDate();

    if (window.backend) {
        window.backend.getDailyReading(monthName, day, (response) => {
            try {
                const data = JSON.parse(response);
                const targetDiv = document.getElementById('dailyDevotionalContent');

                if (data.error) {
                    targetDiv.innerHTML = `<div style="padding:40px; text-align:center; color:#EF4444;">${data.error}</div>`;
                } else if (data.content) {
                    const content = data.content;
                    const parts = content.split('\n');
                    let title = parts[0];
                    if (title.length > 80) title = "Reflexión del Día";

                    const body = parts.slice(title === "Reflexión del Día" || title === parts[0] ? 1 : 0).join('<br>');

                    targetDiv.innerHTML = `
                        <h2 style="font-family:'Outfit'; font-size:1.6rem; color:#111; margin-top:0; line-height:1.3; text-align:center; margin-bottom:20px;">${title}</h2>
                        <div style="text-align:justify;">${body}</div>
                    `;
                } else {
                    targetDiv.innerHTML = `<div style="padding:40px; text-align:center;">No hay lectura disponible para hoy.</div>`;
                }
            } catch (e) {
                console.error("Error parseando lectura backend", e);
                document.getElementById('dailyDevotionalContent').innerHTML = '<div style="color:red; text-align:center; padding:40px;">Error procesando lectura matutina.</div>';
            }
        });
    } else {
        // Fallback local
        fetch('daily_readings.json')
            .then(r => r.json())
            .then(data => {
                const key = `${monthName}_${day}`;
                const content = data[key];
                const targetDiv = document.getElementById('dailyDevotionalContent');
                if (content) {
                    const parts = content.split('\n');
                    let title = parts[0];
                    if (title.length > 80) title = "Reflexión del Día";
                    const body = parts.slice(title === "Reflexión del Día" || title === parts[0] ? 1 : 0).join('<br>');
                    targetDiv.innerHTML = `<h2 style="font-family:'Outfit'; font-size:1.6rem; color:#111; margin-top:0; line-height:1.3; text-align:center; margin-bottom:20px;">${title}</h2><div style="text-align:justify;">${body}</div>`;
                }
            })
            .catch(err => {
                document.getElementById('dailyDevotionalContent').innerHTML = '<div style="color:red; text-align:center; padding:40px;">No se pudo cargar la lectura matutina.</div>';
            });
    }

    // === FOOTER DE ACCIÓN (Botón Terminar) ===
    const footerAction = document.createElement('div');
    footerAction.className = 'session-footer';
    footerAction.style.cssText = `
        margin-top: 40px; 
        text-align: center; 
        padding-bottom: 20px;
        display: flex;
        justify-content: center;
    `;

    footerAction.innerHTML = `
        <button id="finishDayBtn" onclick="finishDailySession()" 
            style="padding:16px 40px; background:#1F2937; color:white; border:none; border-radius:50px; font-weight:bold; cursor:pointer; font-size:1.1rem; display:inline-flex; align-items:center; gap:12px; transition:all 0.2s; box-shadow:0 10px 25px rgba(0,0,0,0.15);"
            onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 15px 30px rgba(0,0,0,0.2)'" 
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 25px rgba(0,0,0,0.15)'">
            <i class="fa-solid fa-check-double"></i> Terminar Día
        </button>
    `;

    container.appendChild(footerAction);

    // Cargar datos guardados y configurar auto-save
    loadDevotionalInputs(todayKey);
    setupDevotionalAutoSave(todayKey);
}


// === HELPERS PLAN DIARIO ===

function calculateReading(dayOfYear, testament, chaptersPerDay) {
    if (typeof bibleData === 'undefined') return { bookName: 'Génesis', chapter: 1, id: 'genesis' };

    // Filtrar libros del testamento seleccionado
    // Ojo: Para 'mormon', asegurarse de que existen en bibleData (ya que se cargan dinámicamente)
    let books = bibleData.filter(b => b.testament === testament);
    if (testament === 'protestant') books = bibleData.filter(b => (b.testament === 'old' || b.testament === 'new') && !b.isDeutero); // Ejemplo simple

    if (books.length === 0) return { bookName: 'N/A', chapter: 1, id: '' };

    // Calcular capítulo absoluto target
    let totalTarget = (dayOfYear * chaptersPerDay);

    // Buscar libro y capítulo correspondiente
    let currentTotal = 0;
    for (let book of books) {
        if (totalTarget <= (currentTotal + book.totalChapters)) {
            let chapter = totalTarget - currentTotal; // Capítulo dentro del libro
            if (chapter < 1) chapter = 1;
            return { bookName: book.name, chapter: chapter, id: book.id, total: book.totalChapters };
        }
        currentTotal += book.totalChapters;
    }

    // Si se pasa (fin de año o lectura terminada), reiniciar o mostrar el último
    return { bookName: books[0].name, chapter: 1, id: books[0].id };
}

function createReadingCard(title, reading, color) {
    // Si no hay lectura válida
    if (!reading.id) return '';

    return `
    <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 4px rgba(0,0,0,0.05); border-left:4px solid ${color}; margin-bottom:20px;">
        <div style="font-size:0.7rem; font-weight:bold; letter-spacing:1px; text-transform:uppercase; color:#9CA3AF; margin-bottom:5px;">
            ${title}
        </div>
        <h2 style="margin:0 0 15px 0; color:#1F2937; font-size:1.5rem;">${reading.bookName} ${reading.chapter}</h2>
        <button onclick="window.location.hash='reader'; openReading('${reading.id}', ${reading.chapter})" 
            style="width:100%; padding:10px; background:${color}; color:white; border:none; border-radius:8px; font-weight:600; cursor:pointer; transition:opacity 0.2s;"
            onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">
            Empezar Lectura
        </button>
    </div>
    `;
}

function loadDevotionalInputs(key) {
    const data = JSON.parse(localStorage.getItem(key) || '{}');
    if (data.gratitude) document.getElementById('devoGratitude').value = data.gratitude;
    if (data.prayer) document.getElementById('devoPrayer').value = data.prayer;
    if (data.commitment) document.getElementById('devoCommitment').value = data.commitment;
}

function setupDevotionalAutoSave(key) {
    const inputs = ['devoGratitude', 'devoPrayer', 'devoCommitment'];
    inputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => {
                const data = JSON.parse(localStorage.getItem(key) || '{}');
                // Mapear ID a propiedad
                if (id === 'devoGratitude') data.gratitude = el.value;
                if (id === 'devoPrayer') data.prayer = el.value;
                if (id === 'devoCommitment') data.commitment = el.value;

                localStorage.setItem(key, JSON.stringify(data));
            });
        }
    });
}

// 7. MI PROGRESO
function initProgress() {
    const container = document.getElementById('studyPlan');
    if (!container) return;

    // Valores por defecto
    let totalRead = 0;
    let booksStarted = 0;
    let progressPercent = 0;
    let totalRef = 1189;

    // Inyectar estructura inicial con IDs
    const contentArea = container.querySelector('div[style*="grid"]') || container;
    if (contentArea) {
        contentArea.innerHTML = `
            <div style="background:white; padding:30px; border-radius:16px; box-shadow:0 4px 6px rgba(0,0,0,0.05); grid-column: 1 / -1;">
                <h3 style="margin:0 0 25px; color:#2563EB;"><i class="fa-solid fa-chart-line"></i> Tu Progreso de Lectura</h3>
                
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin-bottom:30px;">
                    <div style="text-align:center; padding:20px; background:#EFF6FF; border-radius:12px;">
                        <div id="stat-chapters" style="font-size:2.5rem; font-weight:800; color:#2563EB;">0</div>
                        <div style="font-size:0.9rem; color:#6B7280;">Capítulos Leídos</div>
                    </div>
                    <div style="text-align:center; padding:20px; background:#F0FDF4; border-radius:12px;">
                        <div id="stat-books" style="font-size:2.5rem; font-weight:800; color:#059669;">0</div>
                        <div style="font-size:0.9rem; color:#6B7280;">Libros Iniciados</div>
                    </div>
                    <div style="text-align:center; padding:20px; background:#FEF3C7; border-radius:12px;">
                        <div id="stat-percent" style="font-size:2.5rem; font-weight:800; color:#D97706;">0%</div>
                        <div style="font-size:0.9rem; color:#6B7280;">Progreso Total</div>
                    </div>
                </div>
                
                <div style="background:#F3F4F6; height:20px; border-radius:10px; overflow:hidden; margin-bottom:15px;">
                    <div id="stat-progress-bar" style="width:0%; background:linear-gradient(90deg, #2563EB, #8B5CF6); height:100%; transition:width 0.5s;"></div>
                </div>
                <p id="stat-text" style="text-align:center; color:#6B7280; margin:0;">Cargando estadísticas...</p>

                <h3 style="margin-top:30px; color:#2563EB;">Continúa tu lectura</h3>
                <div id="suggestedReadingsArea" style="background:#F9FAFB; padding:20px; border-radius:12px; border:1px dashed #D1D5DB; text-align:center;">
                    <p style="color:#9CA3AF; margin:0;">Completa un día en el Plan Diario para ver sugerencias aquí.</p>
                </div>
            </div>
        `;
    }

    // Llamar al backend
    if (window.backend && window.backend.getUserStatistics) {
        window.backend.getUserStatistics((response) => {
            try {
                const stats = JSON.parse(response);
                if (stats && !stats.error) {
                    const ch = document.getElementById('stat-chapters');
                    const bk = document.getElementById('stat-books');
                    const pct = document.getElementById('stat-percent');
                    const bar = document.getElementById('stat-progress-bar');
                    const txt = document.getElementById('stat-text');

                    if (ch) ch.innerText = stats.chapters_read;
                    if (bk) bk.innerText = stats.books_started;
                    if (pct) pct.innerText = stats.progress_percent + '%';
                    if (bar) bar.style.width = stats.progress_percent + '%';
                    if (txt) txt.innerText = `${stats.chapters_read} de ${stats.total_chapters_reference} capítulos completados`;

                    // Handle suggestion
                    if (stats.suggestion) {
                        const suggArea = document.getElementById('suggestedReadingsArea');
                        if (suggArea) {
                            suggArea.style.border = 'none';
                            suggArea.style.background = 'white';
                            suggArea.style.padding = '0';
                            suggArea.style.textAlign = 'left';

                            suggArea.innerHTML = `
                                <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 4px rgba(0,0,0,0.05); border-left:4px solid #10B981; display:flex; justify-content:space-between; align-items:center;">
                                    <div>
                                        <div style="font-size:0.75rem; font-weight:bold; letter-spacing:1px; text-transform:uppercase; color:#10B981; margin-bottom:5px;">
                                            Siguiente Capítulo
                                        </div>
                                        <h2 style="margin:0; color:#1F2937; font-size:1.5rem;">${stats.suggestion.bookName} ${stats.suggestion.chapter}</h2>
                                    </div>
                                    <button onclick="window.location.hash='reader'; openReading('${stats.suggestion.bookName}', ${stats.suggestion.chapter})" 
                                        style="padding:10px 20px; background:#10B981; color:white; border:none; border-radius:8px; font-weight:600; cursor:pointer; transition:opacity 0.2s; box-shadow:0 2px 4px rgba(16, 185, 129, 0.3);">
                                        <i class="fa-solid fa-book-open"></i> Leer Ahora
                                    </button>
                                </div>
                            `;
                        }
                    }
                }
            } catch (e) {
                console.error("Error parseando stats", e);
            }
        });
    } else {
        // Fallback LocalStorage (Solo si backend falla o no existe)
        const readData = JSON.parse(localStorage.getItem('readData') || '{}');
        Object.keys(readData).forEach(bookId => {
            if (readData[bookId].length > 0) {
                totalRead += readData[bookId].length;
                booksStarted++;
            }
        });
        progressPercent = Math.round((totalRead / 1189) * 100);

        document.getElementById('stat-chapters').innerText = totalRead;
        document.getElementById('stat-books').innerText = booksStarted;
        document.getElementById('stat-percent').innerText = progressPercent + '%';
        document.getElementById('stat-progress-bar').style.width = progressPercent + '%';
        document.getElementById('stat-text').innerText = `${totalRead} de 1189 capítulos completados`;
    }
}

// 8. MIS APUNTES
function initFreeNotes() {
    const notes = JSON.parse(localStorage.getItem('freeNotes') || '[]');
    const container = document.getElementById('notesBoard');

    if (!container) return;

    if (notes.length === 0) {
        container.innerHTML = `
            <div style="text-align:center; padding:60px; color:#9CA3AF;">
                <i class="fa-solid fa-sticky-note" style="font-size:3rem; margin-bottom:15px; opacity:0.4;"></i>
                <p>No tienes notas aún. Haz clic en "Nueva Nota" para empezar.</p>
            </div>
        `;
    } else {
        container.innerHTML = notes.map((note, idx) => `
            <div style="background:white; padding:20px; border-radius:12px; box-shadow:0 2px 4px rgba(0,0,0,0.05); border-left:4px solid #D97706;">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="font-size:0.8rem; color:#9CA3AF;">${note.date}</span>
                    <button onclick="deleteNote(${idx})" style="background:none; border:none; color:#EF4444; cursor:pointer;">🗑️</button>
                </div>
                <p style="margin:0; color:#374151;">${note.content}</p>
            </div>
        `).join('');
    }
}

window.createNewNote = () => {
    const content = prompt('Escribe tu nota:');
    if (!content || !content.trim()) return;

    const notes = JSON.parse(localStorage.getItem('freeNotes') || '[]');
    notes.unshift({
        content: content.trim(),
        date: new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
    });
    localStorage.setItem('freeNotes', JSON.stringify(notes));
    initFreeNotes();
};

window.deleteNote = (idx) => {
    if (!confirm('¿Eliminar esta nota?')) return;
    const notes = JSON.parse(localStorage.getItem('freeNotes') || '[]');
    notes.splice(idx, 1);
    localStorage.setItem('freeNotes', JSON.stringify(notes));
    initFreeNotes();
};

// 9. MI DIARIO
function initJournal() {
    const container = document.getElementById('journalEntriesList');
    if (!container) return;

    const journal = JSON.parse(localStorage.getItem('spiritualJournal') || '[]');

    if (journal.length === 0) {
        container.innerHTML = `
            <div style="text-align:center; grid-column: 1/-1; padding: 40px; color:#999;">
                <i class="fa-solid fa-pen-fancy" style="font-size:3rem; margin-bottom:1rem; opacity:0.3"></i>
                <p>Aún no tienes entradas. Empieza a leer y escribe tus reflexiones.</p>
            </div>
        `;
    } else {
        container.innerHTML = journal.map((entry, idx) => `
            <div style="background:white; padding:20px; border-radius:16px; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between; margin-bottom:15px;">
                    <h4 style="margin:0; color:#2563EB;">${entry.book} ${entry.chapter}</h4>
                    <span style="font-size:0.8rem; color:#9CA3AF;">${entry.date}</span>
                </div>
                <p style="margin:0 0 10px; color:#374151; font-style:italic;">"${entry.reflection}"</p>
                <button onclick="deleteJournalEntry(${idx})" style="background:none; border:none; color:#EF4444; cursor:pointer; font-size:0.85rem;">🗑️ Eliminar</button>
            </div>
        `).join('');
    }
}

window.deleteJournalEntry = (idx) => {
    if (!confirm('¿Eliminar esta entrada del diario?')) return;
    const journal = JSON.parse(localStorage.getItem('spiritualJournal') || '[]');
    journal.splice(idx, 1);
    localStorage.setItem('spiritualJournal', JSON.stringify(journal));
    initJournal();
};

window.createNewJournalEntry = () => {
    const reflection = prompt('Escribe tu reflexión espiritual:');
    if (!reflection || !reflection.trim()) return;

    const journal = JSON.parse(localStorage.getItem('spiritualJournal') || '[]');
    journal.unshift({
        book: "Nota",
        chapter: "Personal",
        reflection: reflection.trim(),
        date: new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    });
    localStorage.setItem('spiritualJournal', JSON.stringify(journal));
    initJournal();
};

// Función auxiliar para abrir lectura
window.openReading = (bookName, chapter) => {
    // Buscar el libro en la data
    const book = bibleData.find(b => b.name === bookName || b.id === bookName.toLowerCase());
    if (book) {
        openReader(book, chapter);
    } else {
        alert('Libro no encontrado: ' + bookName);
    }
};

// Función auxiliar para mostrar feedback visual
function showSuccessToast(message) {
    // Crear elemento toast si no existe
    let toast = document.getElementById('success-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'success-toast';
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #10B981;
            color: white;
            padding: 12px 24px;
            border-radius: 50px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        document.body.appendChild(toast);
    }

    toast.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${message}`;
    toast.style.opacity = '1';

    setTimeout(() => {
        toast.style.opacity = '0';
    }, 3000);
}

window.finishDailySession = () => {
    const btn = document.getElementById('finishDayBtn');

    if (!confirm("¿Has terminado tus lecturas y devocional de hoy?\nSe guardará tu progreso y se cerrará la sesión de este día.")) return;

    // UX: Feedback inmediato en el botón
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Guardando...';
        btn.disabled = true;
    }

    const today = new Date();
    // ISO Date local
    const isoDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 86400000);

    // Calcular lecturas del día para estadísticas
    const chaptersCovered = [];
    const rOld = calculateReading(dayOfYear, 'old', 3);
    const rNew = calculateReading(dayOfYear, 'new', 1);

    if (rOld && rOld.id) chaptersCovered.push({ bookName: rOld.bookName, chapter: rOld.chapter });
    if (rNew && rNew.id) chaptersCovered.push({ bookName: rNew.bookName, chapter: rNew.chapter });

    if (typeof currentMode !== 'undefined' && currentMode === 'mormon') {
        const rMormon = calculateReading(dayOfYear, 'mormon', 1);
        if (rMormon && rMormon.id) chaptersCovered.push({ bookName: rMormon.bookName, chapter: rMormon.chapter });
    }

    // Recopilar datos
    const payload = {
        date: isoDate,
        readings: {
            gratitude: document.getElementById('devoGratitude')?.value || "",
            prayer: document.getElementById('devoPrayer')?.value || "",
            commitment: document.getElementById('devoCommitment')?.value || "",
            chapters_covered: chaptersCovered
        }
    };

    if (window.backend) {
        window.backend.closeDailySession(JSON.stringify(payload), (response) => {
            try {
                const res = JSON.parse(response);
                if (res.status === 'success') {
                    // Feedback visual de éxito
                    showSuccessToast("¡Excelente! Progreso registrado.");

                    // Actualizar UI
                    setTimeout(() => {
                        initDailyPlan();
                    }, 1000);
                } else {
                    alert("Error guardando sesión: " + res.message);
                    if (btn) {
                        btn.innerHTML = '<i class="fa-solid fa-check-double"></i> Terminar Día';
                        btn.disabled = false;
                    }
                }
            } catch (e) {
                console.error(e);
                alert("Error de comunicación con el backend.");
                if (btn) {
                    btn.innerHTML = '<i class="fa-solid fa-check-double"></i> Terminar Día';
                    btn.disabled = false;
                }
            }
        });
    } else {
        console.warn("Backend no disponible. Simulando cierre...");
        showSuccessToast("¡Excelente! Progreso simulado.");
        applyCompletedState();
    }
};

// Exponer funciones unificadas
window.initAllFeatures = () => {
    initPanorama();
    initDailyPlan();
    initProgress();
    initFreeNotes();
    initJournal();
    console.log('✅ Funcionalidades extra inicializadas');
};

// No auto-inicializar en DOMContentLoaded para esperar al backend
// document.addEventListener('DOMContentLoaded', ...);
