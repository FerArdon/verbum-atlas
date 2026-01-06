import fitz
import os

pdf_path = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\83806_spa.pdf"
maps_dir = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\images\maps"
images_dir = r"C:\Users\frard\OneDrive - stp9\Escritorio\Mapa Biblia\images\mormon"

os.makedirs(maps_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"📖 Analizando Libro de Mormón: {len(doc)} páginas...")

map_count = 0
image_count = 0

for page_num in range(len(doc)):
    page = doc[page_num]
    images = page.get_images()
    
    if images:
        for img_index, img in enumerate(images):
            try:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Clasificar por tamaño
                size_kb = len(image_bytes) / 1024
                
                if size_kb > 100:  # Mapas grandes
                    map_count += 1
                    filename = f"mormon_map_{map_count:02d}_page{page_num+1}.{image_ext}"
                    filepath = os.path.join(maps_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                    
                    print(f"🗺️  Mapa extraído: {filename} ({size_kb:.1f} KB)")
                    
                elif size_kb > 10:  # Imágenes medianas
                    image_count += 1
                    filename = f"mormon_img_{image_count:02d}_page{page_num+1}.{image_ext}"
                    filepath = os.path.join(images_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                    
                    print(f"🖼️  Imagen extraída: {filename} ({size_kb:.1f} KB)")
            except Exception as e:
                print(f"⚠️  Error en página {page_num+1}: {e}")

print(f"\n✅ Extracción completada:")
print(f"   🗺️  Mapas: {map_count}")
print(f"   🖼️  Imágenes: {image_count}")

doc.close()
