import re

# Leer el archivo
with open('run_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Nueva función getChapterText
new_function = """    @pyqtSlot(str, int, result=str)
    def getChapterText(self, book_name_ui, chapter):
        # 0. Si es modo Mormón, la lógica es diferente (Directa por nombre, sin ID map)
        if self.current_mode == "mormon":
            try:
                conn = sqlite3.connect(self.db_mormon)
                cursor = conn.cursor()
                # Usamos book_name directamente
                query = "SELECT verse, text FROM verses WHERE book_name=? AND chapter=? ORDER BY verse ASC"
                cursor.execute(query, (book_name_ui, chapter))
                rows = cursor.fetchall()
                conn.close()
                
                result = [{"verse": r[0], "text": r[1]} for r in rows]
                if not result:
                    return json.dumps({"error": f"Capítulo {chapter} de {book_name_ui} sin texto disponible."})
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"error": f"Error SQL Mormón: {str(e)}"})

        # 1. Rutina normal para Biblia (Católica/Protestante)
        current_map = self.map_catholic if self.is_catholic_mode else self.map_protestant
        
        # 2. Buscar ID del libro (Normalizando nombre)
        book_id = None
        for k, v in current_map.items():
            if k.lower() == book_name_ui.lower():
                book_id = v
                break
        
        # Fallback names
        if not book_id:
            if book_name_ui == "Hageo": book_id = current_map.get("Ageo" if self.is_catholic_mode else "Hageo")
            if book_name_ui == "Cantar de los Cantares": book_id = current_map.get("Cantar")

        if not book_id:
            return json.dumps({"error": f"Libro '{book_name_ui}' no encontrado en versión actual."})

        # 3. Consultar DB
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            
            if self.is_catholic_mode:
                # Esquema Católica
                query = "SELECT verse, text FROM verses WHERE book_number=? AND chapter=? ORDER BY verse ASC"
            else:
                # Esquema Protestante
                query = "SELECT verse, text FROM SpaRV_verses WHERE book_id=? AND chapter=? ORDER BY verse ASC"

            cursor.execute(query, (book_id, chapter))
            rows = cursor.fetchall()
            conn.close()
            
            result = [{"verse": r[0], "text": r[1]} for r in rows]
            
            if not result:
                return json.dumps({"error": "Capítulo sin texto disponible."})
                
            return json.dumps(result)

        except Exception as e:
            return json.dumps({"error": f"Error SQL: {str(e)}"})
"""

# Patrón para encontrar la función existente (usando indentación y decoración)
pattern = r'@pyqtSlot\(str, int, result=str\)\s+def getChapterText\(self, book_name_ui, chapter\):[\s\S]*?return json\.dumps\(\{\"error\": f\"Error SQL: \{str\(e\)\}\"\}\)'

if re.search(pattern, content):
    content = re.sub(pattern, new_function.strip(), content)
    print("✓ Función getChapterText actualizada para soportar Mormón")
else:
    print("✗ No se encontró getChapterText")

# Guardar
with open('run_app.py', 'w', encoding='utf-8') as f:
    f.write(content)
