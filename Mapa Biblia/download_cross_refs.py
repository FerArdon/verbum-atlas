import requests
import json

# Descargar referencias cruzadas de OpenBible.info
url = "https://a.openbible.info/data/cross-references.txt"

print("Descargando referencias cruzadas...")
response = requests.get(url)

if response.status_code == 200:
    lines = response.text.strip().split('\n')
    cross_refs = {}
    
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        
        parts = line.split('\t')
        if len(parts) >= 2:
            from_verse = parts[0].strip()
            to_verse = parts[1].strip()
            
            if from_verse not in cross_refs:
                cross_refs[from_verse] = []
            cross_refs[from_verse].append(to_verse)
    
    # Guardar en JSON
    with open('cross_references.json', 'w', encoding='utf-8') as f:
        json.dump(cross_refs, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Referencias cruzadas descargadas: {len(cross_refs)} versículos con referencias")
    print(f"✓ Archivo guardado: cross_references.json")
else:
    print(f"Error al descargar: {response.status_code}")
