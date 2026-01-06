"""
Script de verificación completa del Libro de Mormón
Revisa múltiples libros, capítulos y versículos para detectar ruido
"""
import sqlite3

DB_PATH = "libro_mormon.db"

# Patrones de ruido que no deberían aparecer en el texto limpio
PATRONES_RUIDO = [
    "GEE", "Véase", "Prov.", "Mos.", "Jer.", "DyC", "Cró.", "Rey.",
    "dJerusalén", "1 2 Rey", "Enós 1:", "Omni",
    " a ", " b ", " c ", " d ", " e ", " f ", " g ", " h ",  # Letras de notas
    ":[0-9]",  # Citas bíblicas
    "Relato de Lehi", "escribí estos anales", "hijas de Ismael",
    "grandes aguas", "barco", "Abundancia"
]

def verificar_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Contar registros
    print("=" * 60)
    print("VERIFICACIÓN COMPLETA DEL LIBRO DE MORMÓN")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM libros")
    total_libros = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM capitulos")
    total_capitulos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM versiculos")
    total_versiculos = cursor.fetchone()[0]
    
    print(f"\n📚 Total Libros: {total_libros}")
    print(f"📖 Total Capítulos: {total_capitulos}")
    print(f"📝 Total Versículos: {total_versiculos}")
    
    # 2. Listar todos los libros
    print("\n" + "-" * 40)
    print("LIBROS ENCONTRADOS:")
    print("-" * 40)
    cursor.execute("SELECT id, nombre FROM libros ORDER BY id")
    libros = cursor.fetchall()
    for libro in libros:
        cursor.execute("SELECT COUNT(*) FROM capitulos WHERE libro_id = ?", (libro[0],))
        num_caps = cursor.fetchone()[0]
        print(f"  {libro[0]}. {libro[1]} ({num_caps} capítulos)")
    
    # 3. Muestreo de versículos de diferentes libros
    print("\n" + "-" * 40)
    print("MUESTREO DE VERSÍCULOS (primeros 3 de cada libro):")
    print("-" * 40)
    
    versiculos_con_ruido = []
    
    for libro in libros[:5]:  # Primeros 5 libros
        cursor.execute("""
            SELECT l.nombre, c.numero, v.numero, v.texto
            FROM versiculos v
            JOIN capitulos c ON v.capitulo_id = c.id
            JOIN libros l ON c.libro_id = l.id
            WHERE l.id = ? AND c.numero = 1
            ORDER BY v.numero
            LIMIT 3
        """, (libro[0],))
        
        versiculos = cursor.fetchall()
        print(f"\n📖 {libro[1]} - Capítulo 1:")
        for v in versiculos:
            texto_preview = v[3][:100] + "..." if len(v[3]) > 100 else v[3]
            print(f"   v{v[2]}: {texto_preview}")
            
            # Verificar ruido
            for patron in PATRONES_RUIDO:
                if patron in v[3]:
                    versiculos_con_ruido.append((v[0], v[1], v[2], patron))
    
    # 4. Buscar ruido en TODA la base de datos
    print("\n" + "-" * 40)
    print("BÚSQUEDA DE RUIDO EN TODA LA DB:")
    print("-" * 40)
    
    cursor.execute("""
        SELECT l.nombre, c.numero, v.numero, v.texto
        FROM versiculos v
        JOIN capitulos c ON v.capitulo_id = c.id
        JOIN libros l ON c.libro_id = l.id
    """)
    
    todos_versiculos = cursor.fetchall()
    ruido_encontrado = []
    
    patrones_simples = ["GEE", "Véase", "Prov.", "dJerusalén", "1 2 Rey", "Cró.", "DyC"]
    
    for v in todos_versiculos:
        for patron in patrones_simples:
            if patron in v[3]:
                ruido_encontrado.append((v[0], v[1], v[2], patron))
    
    if ruido_encontrado:
        print(f"⚠️  Se encontró ruido en {len(ruido_encontrado)} versículos:")
        for r in ruido_encontrado[:10]:  # Mostrar máximo 10
            print(f"   - {r[0]} {r[1]}:{r[2]} contiene '{r[3]}'")
    else:
        print("✅ No se encontró ruido conocido en la base de datos!")
    
    # 5. Verificar versículos vacíos o muy cortos
    print("\n" + "-" * 40)
    print("VERSÍCULOS VACÍOS O MUY CORTOS:")
    print("-" * 40)
    
    cursor.execute("""
        SELECT l.nombre, c.numero, v.numero, v.texto
        FROM versiculos v
        JOIN capitulos c ON v.capitulo_id = c.id
        JOIN libros l ON c.libro_id = l.id
        WHERE LENGTH(v.texto) < 20
    """)
    
    cortos = cursor.fetchall()
    if cortos:
        print(f"⚠️  Se encontraron {len(cortos)} versículos muy cortos:")
        for c in cortos[:10]:
            print(f"   - {c[0]} {c[1]}:{c[2]}: '{c[3]}'")
    else:
        print("✅ Todos los versículos tienen longitud adecuada!")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("VERIFICACIÓN COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    verificar_db()
