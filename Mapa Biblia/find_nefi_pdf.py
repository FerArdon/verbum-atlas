import fitz

pdf_path = "83806_spa.pdf"

try:
    doc = fitz.open(pdf_path)
    print(f"Buscando 'PRIMER LIBRO DE NEFI' en {pdf_path}...")
    
    start_page = -1
    
    # Buscar en las primeras 100 páginas (la triple tiene introducción, testimonios, etc.)
    for i in range(100):
        text = doc[i].get_text().upper()
        if "EL PRIMER LIBRO DE NEFI" in text or "1 NEFI" in text:
            # Verificar si parece un inicio de libro (capítulo 1)
            if "CAPÍTULO 1" in text or "CAPITULO 1" in text:
                print(f"¡CANDIDATO ENCONTRADO! Página {i+1}")
                print(text[:300])
                start_page = i
                break
    
    if start_page != -1:
        # Extraer texto de prueba de esa página
        print(f"\n--- Texto extraído de pág {start_page+1} ---")
        print(doc[start_page].get_text())
    else:
        print("No se encontró el inicio de 1 Nefi en las primeras 100 páginas.")

except Exception as e:
    print(f"Error: {e}")
