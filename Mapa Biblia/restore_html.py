import shutil

src_html = r"C:\Users\frard\OneDrive - stp9\Documentos\Mapa Biblia\index.html"
dst_html = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\index.html"

try:
    shutil.copy2(src_html, dst_html)
    print("✓ index.html restaurado con éxito.")
except Exception as e:
    print(f"Error restaurando index.html: {e}")
