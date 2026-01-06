import re

# Leer el archivo
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar la variable de referencias cruzadas después de freeNotes
insert_after = "let freeNotes = JSON.parse(localStorage.getItem('bibleFreeNotes')) || [];"
cross_ref_code = """
let crossReferences = {}; // Referencias cruzadas

// Cargar referencias cruzadas
fetch('cross_references.json')
    .then(res => res.json())
    .then(data => { crossReferences = data; })
    .catch(err => console.log('Referencias cruzadas no disponibles:', err));
"""

if insert_after in content:
    content = content.replace(insert_after, insert_after + cross_ref_code)
    print("✓ Variable de referencias cruzadas agregada")
else:
    print("✗ No se encontró el punto de inserción para referencias")

# 2. Modificar la función que renderiza versículos para incluir referencias
# Buscar el patrón donde se construye el HTML de versículos
old_pattern = r'html \+= `<p[^>]*><sup[^>]*>\$\{v\.verse\}</sup>\$\{v\.text\}</p>`;'
new_pattern = '''// Buscar referencias cruzadas para este versículo
                        const verseKey = `${book.name}.${chapter}.${v.verse}`;
                        const refs = crossReferences[verseKey] || [];
                        
                        let refsHtml = "";
                        if (refs.length > 0) {
                            refsHtml = ` <span style="font-size:0.7rem; color:#888; margin-left:8px;">(${refs.map(ref => {
                                return `<a href="#" onclick="window.goToReference('${ref}'); return false;" style="color:#2563eb; text-decoration:none; margin:0 2px;">${ref}</a>`;
                            }).join(', ')})</span>`;
                        }
                        
                        html += `<p style="margin-bottom:12px;"><sup style="color:${book.themeColor}; font-weight:bold; margin-right:5px;">${v.verse}</sup>${v.text}${refsHtml}</p>`;'''

# Buscar y reemplazar el patrón de renderizado de versículos
if re.search(r'html \+= `<p', content):
    # Encontrar la línea específica que renderiza versículos
    content = re.sub(
        r'(data\.forEach\(v => \{[\s\S]*?)html \+= `<p[^>]*><sup[^>]*>\$\{v\.verse\}</sup>\$\{v\.text\}</p>`;',
        r'\1' + new_pattern,
        content,
        count=1
    )
    print("✓ Renderizado de versículos actualizado con referencias")
else:
    print("⚠ No se encontró el patrón de renderizado de versículos")

# Guardar el archivo modificado
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Referencias cruzadas integradas en app.js")
