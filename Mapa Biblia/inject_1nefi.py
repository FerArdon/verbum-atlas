import sqlite3

db_path = 'libro_mormon.db'

# Texto de 1 Nefi 1 (Versículos 1-5 como prueba)
verses_1nefi_1 = [
    (1, "Yo, Nefi, nací de buenos padres, por lo tanto fui instruido en algo de toda la ciencia de mi padre; y habiendo visto muchas aflicciones en el curso de mis días, no obstante, habiendo sido altamente favorecido del Señor en todos mis días; sí, habiendo tenido un gran conocimiento de la bondad y los misterios de Dios, escribo, por tanto, la historia de los hechos de mis días."),
    (2, "Y sí, hago una relación en el lenguaje de mi padre, que consiste en la ciencia de los judíos y el idioma de los egipcios."),
    (3, "Y sé que la relación que hago es verdadera; y la hago de mi propia mano; y la hago según mi saber."),
    (4, "Porque sucedió que al comienzo del primer año del reinado de Sedequías, rey de Judá (mi padre Lehi había morado en Jerusalén toda su vida), llegaron muchos profetas ese mismo año, profetizando al pueblo que se arrepintieran, o la gran ciudad de Jerusalén sería destruida."),
    (5, "Por lo que aconteció que mi padre Lehi, mientras iba por su camino, oró al Señor, sí, aun con todo su corazón, a favor de su pueblo.")
]

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 1. Limpiar datos basura
    print("Limpiando datos corruptos...")
    c.execute("DELETE FROM verses")
    
    # 2. Insertar 1 Nefi 1
    print("Insertando 1 Nefi Capítulo 1...")
    for v_num, text in verses_1nefi_1:
        # Schema: id, book_id, book_name, chapter, verse, text
        c.execute("INSERT INTO verses (book_id, book_name, chapter, verse, text) VALUES (?, ?, ?, ?, ?)",
                  (1, "1 Nefi", 1, v_num, text))

    conn.commit()
    
    # 3. Verificar
    c.execute("SELECT count(*) FROM verses WHERE book_name='1 Nefi' AND chapter=1")
    count = c.fetchone()[0]
    print(f"✓ Éxito: {count} versículos de 1 Nefi insertados correctamente.")
    
    conn.close()

except Exception as e:
    print(f"Error: {e}")
