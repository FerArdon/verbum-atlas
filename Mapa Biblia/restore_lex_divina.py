import re

# Leer index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar Botón de Navegación (antes de "Mi Progreso" o "Configurar")
nav_btn = """
            <button class="nav-btn" data-target="lexDivina" style="display:flex; align-items:center; width:100%; padding:12px; border:none; background:transparent; color:#4B5563; font-weight:600; cursor:pointer; text-align:left; border-radius:8px; transition:all 0.2s;">
                <span style="margin-right:10px; font-size:1.2rem;">✨</span> Lex Divina (IA)
            </button>
"""

# Insertar antes de "Mi Progreso"
if 'data-target="lexDivina"' not in content:
    target = 'data-target="progress"'
    if target in content:
        # Buscamos la línea completa del botón progress para insertar antes
        content = re.sub(r'(<button.*?data-target="progress".*?>)', nav_btn + r'\1', content, count=1, flags=re.DOTALL)
    else:
        # Fallback: insertar antes del div de API Key
        content = content.replace('<div class="api-key-container"', nav_btn + '\n            <div class="api-key-container"')


# 2. Agregar Sección Lex Divina (al final, antes de los scripts)
lex_section = """
    <!-- VISTA: LEX DIVINA (IA) -->
    <section id="lexDivina" class="view-section" style="display:none; padding:40px; max-width:800px; margin:0 auto;">
        <div style="background:white; border-radius:24px; padding:40px; box-shadow:0 10px 30px rgba(0,0,0,0.05);">
            <div style="text-align:center; margin-bottom:30px;">
                <h2 style="font-size:2.5rem; color:#1F2937; margin-bottom:10px;">Lex Divina</h2>
                <p style="color:#6B7280;">Inteligencia Artificial aplicada al estudio espiritual</p>
            </div>

            <!-- Chat Container -->
            <div id="chatContainer" style="height:400px; overflow-y:auto; border:1px solid #E5E7EB; border-radius:16px; padding:20px; margin-bottom:20px; background:#F9FAFB;">
                <div style="text-align:center; color:#9CA3AF; margin-top:150px;">
                    <p>Haz una pregunta sobre las escrituras...</p>
                </div>
            </div>

            <!-- Input Area -->
            <div style="position:relative;">
                <textarea id="chatInput" placeholder="Ej: ¿Qué enseña Alma sobre la fe?" 
                    style="width:100%; padding:15px 50px 15px 20px; border:2px solid #E5E7EB; border-radius:12px; font-family:inherit; resize:none; outline:none; transition:border-color 0.2s;"></textarea>
                <button id="sendChatBtn" style="position:absolute; right:10px; top:50%; transform:translateY(-50%); background:#8B5CF6; color:white; border:none; width:40px; height:40px; border-radius:10px; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                    ➤
                </button>
            </div>
            
            <div style="margin-top:20px; text-align:right;">
                 <button id="clearChatBtn" style="background:none; border:none; color:#EF4444; cursor:pointer; font-size:0.9rem;">🗑️ Borrar chat</button>
            </div>

            <div style="margin-top:20px; padding:15px; background:#EFF6FF; border-radius:12px; font-size:0.9rem; color:#1E40AF;">
                <strong>Nota:</strong> Lex Divina utiliza Gemini AI. Asegúrate de configurar tu API Key en el menú lateral.
            </div>
        </div>
    </section>
"""

if 'id="lexDivina"' not in content:
    # Insertar antes del cierre de main o antes de los scripts
    content = content.replace('</main>', lex_section + '\n    </main>')

# Guardar
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Lex Divina restaurada en HTML.")
