
nav_js = """
// ==========================================
// FIX DE NAVEGACIÓN (Para asegurar que Lex Divina funcione)
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // Reasignar clicks a botones de navegación para garantizar que todo funcione
    const allNavBtns = document.querySelectorAll('.nav-btn');
    const allSections = document.querySelectorAll('.view-section'); // Asegúrate que tus secciones tengan esta clase o usa ids
    
    // Lista explícita de secciones ID
    const sectionIds = ['library', 'panorama', 'reader', 'dailyPlan', 'myJournal', 'myNotes', 'progress', 'lexDivina'];

    allNavBtns.forEach(btn => {
        // Clonar para eliminar listeners viejos rotos (opcional, pero seguro)
        // const newBtn = btn.cloneNode(true);
        // btn.parentNode.replaceChild(newBtn, btn);
        
        btn.addEventListener('click', (e) => {
            // Prevenir default si es necesario
            // e.preventDefault();
            
            const targetId = btn.getAttribute('data-target');
            console.log("Navegando a:", targetId);
            
            if (targetId) {
                // 1. Ocultar todo
                sectionIds.forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.style.display = 'none';
                });
                
                // 2. Mostrar target
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    targetEl.style.display = 'block';
                    window.scrollTo(0,0);
                } else {
                    console.error("No se encontró la sección:", targetId);
                }
                
                // 3. Estilo Active
                allNavBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }
        });
    });
    
    // Mostrar biblioteca por defecto al inicio (o lo que estuviera)
    // if(document.getElementById('library').style.display === '') document.getElementById('library').style.display = 'block';
});
"""

with open(r'js\app.js', 'a', encoding='utf-8') as f:
    f.write("\n" + nav_js)
    
print("✓ Fix de navegación inyectado (reparación de botones).")
