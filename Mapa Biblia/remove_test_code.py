import re

# Leer run_app.py
with open('run_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Bloque de prueba a eliminar
test_block = """            # PRUEBA DIAGNÓSTICA: Devolver texto directo para 1 Nefi 1
            if "1 nefi" in book_name_ui.lower() and chapter == 1:
                return json.dumps([
                    {"verse": 1, "text": "TEST EXITOSO: Yo, Nefi, nací de buenos padres... (Si ves esto, la conexión funciona)"},
                    {"verse": 2, "text": "Este texto viene directo del backend, saltándose la base de datos para probar."}
                ])"""

# Buscar y reemplazar por nada
if test_block in content:
    content = content.replace(test_block, "")
    print("✓ Mensaje de prueba eliminado.")
else:
    # Intentar búsqueda con regex por si los espacios cambian
    pattern = r'# PRUEBA DIAGNÓSTICA[\s\S]*?\]\)'
    content = re.sub(pattern, "", content)
    print("✓ Mensaje de prueba eliminado (via regex).")

# Guardar
with open('run_app.py', 'w', encoding='utf-8') as f:
    f.write(content)
