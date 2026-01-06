import fitz

pdf_path = "83806_spa.pdf"
doc = fitz.open(pdf_path)

print("Escaneando 'CAPÍTULO' en las primeras 50 páginas...")
for i in range(50):
    text = doc[i].get_text()
    lines = text.split('\n')
    for line in lines:
        if "CAPÍTULO" in line.upper() or "CAPITULO" in line.upper():
            print(f"Pág {i+1}: {line.strip()}")
            # Imprimir contexto (las siguientes 2 lineas)
            try:
                idx = lines.index(line)
                print(f"   CTX: {lines[idx+1].strip() if idx+1<len(lines) else ''}")
            except: pass
