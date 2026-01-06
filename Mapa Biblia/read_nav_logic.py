with open(r'js\app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = -1
for i, line in enumerate(lines):
    if "document.querySelectorAll('.nav-btn')" in line:
        start = i
        break

if start != -1:
    print("Encontrado bloque de navegación:")
    for j in range(start, min(start+30, len(lines))):
        print(lines[j].strip())
