import fitz
import os

pdf_path = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\https___mifecatolica.net_wp-content_uploads_biblia-latinoamericana.pdf"
output_dir = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\images\maps"

os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Analizando {len(doc)} páginas...")

# Buscar páginas con imágenes grandes (probablemente mapas)
map_count = 0
for page_num in range(len(doc)):
    page = doc[page_num]
    images = page.get_images()
    
    # Si la página tiene imágenes
    if images:
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Solo guardar imágenes grandes (probablemente mapas)
            if len(image_bytes) > 50000:  # Más de 50KB
                map_count += 1
                filename = f"map_{map_count:02d}_page{page_num+1}.{image_ext}"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(image_bytes)
                
                print(f"✓ Mapa extraído: {filename} ({len(image_bytes)/1024:.1f} KB)")

print(f"\n✓ Total de mapas extraídos: {map_count}")
doc.close()
