import shutil
import os

src_js = r"C:\Users\frard\OneDrive - stp9\Documentos\Mapa Biblia\js\app.js"
dst_js = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\js\app.js"

try:
    shutil.copy2(src_js, dst_js)
    print("✓ app.js restaurado con éxito.")
except Exception as e:
    print(f"Error restaurando app.js: {e}")
