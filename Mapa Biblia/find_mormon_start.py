import fitz  # PyMuPDF

pdf_path = "83806_spa.pdf"

try:
    doc = fitz.open(pdf_path)
    print(f"Abriendo {pdf_path} ({len(doc)} páginas)...")
    
    found = False
    for i in range(min(100, len(doc))):
        text = doc[i].get_text()
        # Buscamos "Yo, Nefi, nací de buenos padres"
        if "nací de buenos padres" in text or "naci de buenos padres" in text:
            print(f"¡ENCONTRADO! El inicio está en la página {i+1} (índice {i})")
            print(f"Texto muestra: {text[:200]}...")
            found = True
            break
            
    if not found:
        print("No se encontró la frase clave en las primeras 100 páginas.")
        
except Exception as e:
    print(f"Error abriendo PDF: {e}")
