# Leer index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Quitar/Ocultar el mensaje de nota en Lex Divina
# Buscamos el div específico
msg_start = '<div style="margin-top:20px; padding:15px; background:#EFF6FF;'
if msg_start in content:
    # Reemplazar por versión oculta o texto diferente
    content = content.replace(msg_start, '<div style="display:none;">') # Lo ocultamos

# 2. Ocultar el botón de configuración de API Key del menú lateral si quieres
# Buscamos <div class="api-key-container"
if '<div class="api-key-container"' in content:
    content = content.replace('<div class="api-key-container"', '<div class="api-key-container" style="display:none !important;"')

# Guardar
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ UI limpia de advertencias de API Key.")
