import sqlite3
import os

db_file = "biblia.db"
if os.path.exists(db_file): os.remove(db_file)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("CREATE TABLE t_bible (id INTEGER PRIMARY KEY AUTOINCREMENT, b INTEGER, c INTEGER, v INTEGER, t TEXT);")

books_map = {1: "Génesis", 2: "Éxodo", 40: "Mateo", 45: "Romanos"}

# DATOS ESPECÍFICOS PARA LA DEMO
data = []

# --- GÉNESIS ---
# Creación (Cap 1)
data.append((1, 1, 1, 1, "En el principio creó Dios los cielos y la tierra."))
data.append((1, 1, 1, 27, "Y creó Dios al hombre a su imagen, a imagen de Dios lo creó; varón y hembra los creó."))

# Caída (Cap 3)
data.append((1, 1, 3, 1, "Pero la serpiente era astuta, más que todos los animales del campo que Jehová Dios había hecho..."))
data.append((1, 1, 3, 6, "Y vio la mujer que el árbol era bueno para comer, y que era agradable a los ojos, y árbol codiciable para alcanzar la sabiduría; y tomó de su fruto, y comió; y dio también a su marido."))

# Diluvio (Cap 6)
data.append((1, 1, 6, 5, "Y vio Jehová que la maldad de los hombres era mucha en la tierra, y que todo designio de los pensamientos del corazón de ellos era de continuo solamente el mal."))
data.append((1, 1, 6, 14, "Hazte un arca de madera de gofer; harás aposentos en el arca, y la calafatearás con brea por dentro y por fuera."))

# Abraham (Cap 12)
data.append((1, 1, 12, 1, "Pero Jehová había dicho a Abram: Vete de tu tierra y de tu parentela, y de la casa de tu padre, a la tierra que te mostraré."))
data.append((1, 1, 12, 2, "Y haré de ti una nación grande, y te bendeciré, y engrandeceré tu nombre, y serás bendición."))

# José (Cap 37)
data.append((1, 1, 37, 3, "Y amaba Israel a José más que a todos sus hijos, porque lo había tenido en su vejez; y le hizo una túnica de diversos colores."))

# --- ROMANOS ---
# Cap 1, 4, 6, 9, 12
data.append((45, 45, 1, 16, "Porque no me avergüenzo del evangelio, porque es poder de Dios para salvación..."))
data.append((45, 45, 4, 3, "Porque ¿qué dice la Escritura? Creyó Abraham a Dios, y le fue contado por justicia."))
data.append((45, 45, 6, 23, "Porque la paga del pecado es muerte, mas la dádiva de Dios es vida eterna en Cristo Jesús Señor nuestro."))
data.append((45, 45, 9, 16, "Así que no depende del que quiere, ni del que corre, sino de Dios que tiene misericordia."))
data.append((45, 45, 12, 2, "No os conforméis a este siglo, sino transformaos por medio de la renovación de vuestro entendimiento."))

# --- MATEO ---
data.append((40, 40, 1, 1, "Libro de la genealogía de Jesucristo, hijo de David, hijo de Abraham."))
data.append((40, 40, 5, 3, "Bienaventurados los pobres en espíritu, porque de ellos es el reino de los cielos."))
data.append((40, 40, 28, 6, "No está aquí, pues ha resucitado, como dijo. Venid, ved el lugar donde fue puesto el Señor."))

cursor.executemany("INSERT INTO t_bible (b, b, c, v, t) VALUES (?, ?, ?, ?, ?)", data)
conn.commit()
conn.close()
print("Base de datos regenerada con TODOS los capítulos de la demo.")
