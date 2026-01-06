import re

api_key = "AIzaSyAcTLrFJND4zfFNeINcbSr-yfWh-jwtyQg"

# Leer run_app.py
with open('run_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Configurar Key en __init__
# Buscamos __init__(self) y agregamos la configuración
if 'self.speech_queue = queue.Queue()' in content:
    # Insertar configuración de genai justo después
    code_to_insert = f'\n            try:\n                genai.configure(api_key="{api_key}")\n                self.api_key = "{api_key}"\n                print("Backend: API Key integrada exitosamente.")\n            except Exception as e:\n                print(f"Error config API Key: {{e}}")'
    
    content = content.replace('self.speech_queue = queue.Queue()', 'self.speech_queue = queue.Queue()' + code_to_insert)

# 2. Asegurar que askAgent use self.api_key si existe
# Opcional, ya que genai.configure es global, pero por seguridad:
# Buscamos si hay chequeos tipo 'if not self.api_key' y los relajamos o aseguramos que self.api_key tenga valor.
# Como ya lo seteamos en __init__, debería bastar.

# Guardar
with open('run_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ API Key integrada en el Backend.")
