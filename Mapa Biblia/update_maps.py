import re

# Leer el archivo
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Definir el bloque de la galería
gallery_start = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">'
gallery_end = '</div>'

# Nuevas imágenes
new_gallery = """
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
                    <div class="map-card" style="background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.2s;" onclick="window.openMapModal('images/maps/mormon_map_02_page2077.png', 'Mapa Histórico I')">
                        <img src="images/maps/mormon_map_02_page2077.png" alt="Mapa 1" style="width: 100%; height: 200px; object-fit: cover;">
                        <div style="padding: 15px;">
                            <h3 style="margin: 0 0 5px; color: #059669; font-size: 1rem;">Mapa Histórico I</h3>
                            <p style="font-size: 0.85rem; color: #666; margin: 0;">Tierras del Libro de Mormón</p>
                        </div>
                    </div>

                    <div class="map-card" style="background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.2s;" onclick="window.openMapModal('images/maps/mormon_map_04_page2079.png', 'Mapa Histórico II')">
                        <img src="images/maps/mormon_map_04_page2079.png" alt="Mapa 2" style="width: 100%; height: 200px; object-fit: cover;">
                        <div style="padding: 15px;">
                            <h3 style="margin: 0 0 5px; color: #059669; font-size: 1rem;">Mapa Histórico II</h3>
                            <p style="font-size: 0.85rem; color: #666; margin: 0;">Migraciones y Viajes</p>
                        </div>
                    </div>

                    <div class="map-card" style="background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.2s;" onclick="window.openMapModal('images/maps/mormon_map_08_page2082.png', 'Mapa Histórico III')">
                        <img src="images/maps/mormon_map_08_page2082.png" alt="Mapa 3" style="width: 100%; height: 200px; object-fit: cover;">
                        <div style="padding: 15px;">
                            <h3 style="margin: 0 0 5px; color: #059669; font-size: 1rem;">Mapa Histórico III</h3>
                            <p style="font-size: 0.85rem; color: #666; margin: 0;">Contexto Geográfico Ampliado</p>
                        </div>
                    </div>
                </div>
"""

# Reemplazar usando regex para capturar todo el bloque div
pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(300px, 1fr\)\); gap: 1\.5rem;">[\s\S]*?</div>'

if re.search(pattern, content):
    content = re.sub(pattern, new_gallery.strip(), content, count=1) # Solo reemplazar el primer match (que debería ser el de historicalMaps)
    print("✓ Galería de mapas actualizada")
else:
    print("✗ No se encontró el bloque de galería")

# Guardar
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
