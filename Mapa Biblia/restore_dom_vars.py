import re

# Leer app.js
with open(r'js\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Variables perdidas
missing_vars = """
    // 1. REFS DOM (Restauradas)
    const booksGrid = document.getElementById('booksGrid');
    const periodicTable = document.getElementById('periodicTable');
    const searchInput = document.getElementById('searchInput');
    const bookDetail = document.getElementById('bookDetail');
    const verseViewer = document.getElementById('verseViewer');
    const verseTitle = document.getElementById('verseTitle');
    const verseContent = document.getElementById('verseContent');
    const viewerControls = document.getElementById('viewerControls');
    const navBtns = document.querySelectorAll('.nav-btn');
    const backBtn = document.getElementById('backBtn');
    const dailyPlanContainer = document.getElementById('dailyPlanContainer');
    const dailyPlanDate = document.getElementById('dailyPlanDate');
"""

# Buscar un buen punto de inserción (al inicio del listener)
if "document.addEventListener('DOMContentLoaded', () => {" in content:
    content = content.replace("document.addEventListener('DOMContentLoaded', () => {", 
                            "document.addEventListener('DOMContentLoaded', () => {" + missing_vars)
    print("✓ Variables DOM restauradas.")
else:
    print("✗ No se encontró el inicio del DOMContentLoaded")

# Guardar
with open(r'js\app.js', 'w', encoding='utf-8') as f:
    f.write(content)
