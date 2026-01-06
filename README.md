# 📖 Verbum Atlas 2026

<div align="center">

![Verbum Atlas Logo](app_icon.png)

**Una aplicación integral de estudio bíblico con inteligencia artificial**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-WebEngine-green.svg)](https://pypi.org/project/PyQt6-WebEngine/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ Características

### 📚 **Biblioteca Bíblica Completa**
- **Reina-Valera 1909** - Texto clásico del protestantismo
- **Biblia Católica Latinoamericana** - Incluye libros deuterocanónicos

### 🤖 **Lex Divina - Asistente con IA**
- Chat interactivo con inteligencia artificial (Google Gemini)
- Respuestas contextualizadas a preguntas teológicas
- Formato enriquecido con Markdown

### 📅 **Plan de Lectura Diario**
- Lecturas matutinas organizadas por fecha
- Seguimiento de progreso personal
- Sistema de "Cierre de Día" con estado Zen

### 🗺️ **Panorama Bíblico**
- Tabla periódica de libros de la Biblia
- Cronología de eventos bíblicos
- Referencias cruzadas interactivas

### 📝 **Mi Diario**
- Diario personal de estudio
- Guardado automático de reflexiones
- Historial de entradas

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/verbum-atlas.git
cd verbum-atlas

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install PyQt6 PyQt6-WebEngine google-generativeai
```

### Ejecución

```bash
python run_app.py
```

---

## 📦 Generar Ejecutable

Para crear un archivo `.exe` standalone:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --icon=app_icon.ico --name="Verbum Atlas 2026" run_app.py
```

O simplemente ejecuta:
```bash
BUILD_APP.bat
```

---

## 🔧 Configuración

### API de Gemini
Para usar el asistente **Lex Divina**, necesitas una API key de Google Gemini:

1. Obtén tu API key en [Google AI Studio](https://aistudio.google.com/app/apikey)
2. En la aplicación, ve a **Configuración** → ingresa tu API key

---

## 📁 Estructura del Proyecto

```
Mapa Biblia/
├── run_app.py           # Aplicación principal (PyQt6)
├── index.html           # Interfaz de usuario
├── css/                 # Estilos
│   └── style.css
├── js/                  # JavaScript
│   ├── app.js           # Lógica principal
│   ├── features.js      # Funcionalidades
│   └── data.js          # Datos de la Biblia
├── biblia.db            # Base de datos Reina-Valera
├── biblia_catolica.db   # Base de datos Católica
├── daily_readings.json  # Lecturas diarias
└── cross_references.json # Referencias cruzadas
```

---

## 📖 Manual de Usuario

Consulta el [Manual de Usuario](MANUAL_USUARIO_VERBUM_ATLAS.md) para instrucciones detalladas sobre cómo usar cada función de la aplicación.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| **Python 3.10+** | Backend y lógica de aplicación |
| **PyQt6 WebEngine** | Interfaz gráfica con Chromium embebido |
| **SQLite3** | Almacenamiento de textos bíblicos |
| **Google Gemini** | Inteligencia artificial para Lex Divina |
| **HTML/CSS/JS** | Interfaz de usuario moderna |

---

## 👨‍💻 Autor

**Fer Ardón**  
Ingeniero Forestal & Desarrollador de Software

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**"En el principio era el Verbo..."** - Juan 1:1

⭐ Si te gusta este proyecto, ¡deja una estrella!

</div>
