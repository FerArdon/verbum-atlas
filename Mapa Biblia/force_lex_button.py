# Leer index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Botón Lex Divina
lex_btn = """
                <button class="nav-btn" data-target="lexDivina">
                    <span class="icon">✨</span> Lex Divina (IA)
                </button>
"""

# Insertar antes de </nav>
if 'data-target="lexDivina"' not in content:
    content = content.replace('</nav>', lex_btn + '\n            </nav>')
    print("✓ Botón Lex Divina insertado antes de </nav>.")
else:
    print("El botón ya existe (curioso).")

# Guardar
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
