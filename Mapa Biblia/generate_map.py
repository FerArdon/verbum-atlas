import sqlite3

conn = sqlite3.connect("biblia_catolica.db")
cursor = conn.cursor()

# Extraer todos los libros y sus IDs
cursor.execute("SELECT book_number, long_name FROM books ORDER BY book_number")
rows = cursor.fetchall()

print("MAPEO_CATOLICO = {")
for r in rows:
    # r[0] es el ID (ej 10), r[1] es el Nombre (ej Génesis)
    print(f'    "{r[1]}": {r[0]},')
print("}")

conn.close()
