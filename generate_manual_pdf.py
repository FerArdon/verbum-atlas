"""
Generador de Manual PDF Ilustrado para Verbum Atlas 2026
"""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
import os

# Configuración
OUTPUT_FILE = "MANUAL_VERBUM_ATLAS_2026.pdf"
IMG_DIR = "manual_images"

# Colores del manual
PRIMARY_BLUE = HexColor("#2563EB")
PRIMARY_GOLD = HexColor("#D97706")
DARK_TEXT = HexColor("#1F2937")
LIGHT_BG = HexColor("#F3F4F6")

def get_image(name_contains):
    """Busca una imagen por nombre parcial"""
    for f in os.listdir(IMG_DIR):
        if name_contains in f and f.endswith('.png'):
            return os.path.join(IMG_DIR, f)
    return None

def create_manual():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=LETTER,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=PRIMARY_BLUE,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=PRIMARY_BLUE,
        spaceBefore=25,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=PRIMARY_GOLD,
        spaceBefore=18,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_TEXT,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=16
    )
    
    center_style = ParagraphStyle(
        'CenterText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_TEXT,
        alignment=TA_CENTER,
        spaceAfter=8
    )
    
    tip_style = ParagraphStyle(
        'TipStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor("#059669"),
        leftIndent=20,
        spaceBefore=10,
        spaceAfter=10,
        backColor=HexColor("#ECFDF5"),
        borderPadding=8
    )
    
    # Contenido
    story = []
    
    # ========== PORTADA ==========
    story.append(Spacer(1, 1.5*inch))
    
    # Logo/Imagen principal
    intro_img = get_image("intro")
    if intro_img:
        story.append(Image(intro_img, width=4*inch, height=4*inch))
    
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("📖 Manual de Usuario", title_style))
    story.append(Paragraph("<b>Verbum Atlas 2026</b>", center_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Tu compañero digital para el estudio profundo de las Escrituras", center_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<i>Versión 2026 • Enero 2026</i>", center_style))
    story.append(Paragraph("<i>Desarrollado por Fernando Ardón & Antigravity AI</i>", center_style))
    
    story.append(PageBreak())
    
    # ========== TABLA DE CONTENIDOS ==========
    story.append(Paragraph("📋 Tabla de Contenidos", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "1. Introducción",
        "2. Instalación",
        "3. Pantalla Principal",
        "4. Selector de Versión Bíblica",
        "5. Plan Diario",
        "6. Biblioteca",
        "7. Panorama",
        "8. Lex Divina (Inteligencia Artificial)",
        "9. Mi Diario",
        "10. Mis Apuntes",
        "11. Mi Progreso",
        "12. Lectura de Texto con Voz",
        "13. Preguntas Frecuentes",
        "14. Soporte y Créditos"
    ]
    
    for item in toc_items:
        story.append(Paragraph(f"• {item}", body_style))
    
    story.append(PageBreak())
    
    # ========== INTRODUCCIÓN ==========
    story.append(Paragraph("1. Introducción", heading1_style))
    
    story.append(Paragraph(
        "<b>Verbum Atlas 2026</b> es una aplicación de escritorio diseñada para facilitar "
        "el estudio bíblico de manera integral, moderna y espiritualmente enriquecedora. "
        "Combina el acceso a múltiples traducciones de las Escrituras con herramientas de "
        "reflexión personal, inteligencia artificial y seguimiento de progreso.",
        body_style
    ))
    
    story.append(Paragraph("¿Qué incluye?", heading2_style))
    
    features = [
        "<b>3 Versiones de texto bíblico:</b> Biblia Católica (73 libros), Biblia Protestante (66 libros), Libro de Mormón (15 libros)",
        "<b>Lectura guiada diaria</b> basada en el calendario anual",
        "<b>Asistente de IA</b> (Lex Divina) para consultar dudas teológicas",
        "<b>Diario Espiritual</b> estructurado para reflexión y aplicación",
        "<b>Sistema de notas</b> libres tipo 'post-it' digital",
        "<b>Estadísticas de progreso</b> para motivarte a completar tu lectura anual"
    ]
    
    for feat in features:
        story.append(Paragraph(f"• {feat}", body_style))
    
    story.append(PageBreak())
    
    # ========== INSTALACIÓN ==========
    story.append(Paragraph("2. Instalación", heading1_style))
    
    install_img = get_image("instalacion")
    if install_img:
        story.append(Image(install_img, width=3.5*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Sigue estos pasos para instalar Verbum Atlas:", body_style))
    
    install_steps = [
        "Ejecuta el instalador <b>VerbumAtlas_2026_Final_v4.exe</b>",
        "Sigue las instrucciones del asistente de instalación",
        "Selecciona si deseas crear un <b>acceso directo en el escritorio</b>",
        "Haz clic en <b>'Instalar'</b> y espera a que finalice",
        "Al terminar, marca <b>'Ejecutar Verbum Atlas 2026'</b> para iniciar"
    ]
    
    for i, step in enumerate(install_steps, 1):
        story.append(Paragraph(f"{i}. {step}", body_style))
    
    story.append(Paragraph("Requisitos del Sistema", heading2_style))
    
    req_data = [
        ["Componente", "Requisito Mínimo"],
        ["Sistema Operativo", "Windows 10 o superior"],
        ["RAM", "4 GB (8 GB recomendado)"],
        ["Espacio en Disco", "~400 MB"],
        ["Internet", "Solo para Lex Divina (IA)"]
    ]
    
    req_table = Table(req_data, colWidths=[2.5*inch, 3*inch])
    req_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 1, colors.white)
    ]))
    story.append(req_table)
    
    story.append(PageBreak())
    
    # ========== PLAN DIARIO ==========
    story.append(Paragraph("5. 📅 Plan Diario", heading1_style))
    
    plan_img = get_image("plan_diario")
    if plan_img:
        story.append(Image(plan_img, width=3.5*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "Este módulo te ofrece <b>lecturas matutinas guiadas</b> basadas en un calendario anual. "
        "Cada día del año tiene asignado un contenido devocional específico.",
        body_style
    ))
    
    story.append(Paragraph("¿Cómo usarlo?", heading2_style))
    
    plan_steps = [
        "Haz clic en <b>'Plan Diario'</b> en el menú lateral",
        "Verás la fecha actual y el contenido asignado para ese día",
        "Lee la meditación y reflexiona sobre el mensaje"
    ]
    
    for i, step in enumerate(plan_steps, 1):
        story.append(Paragraph(f"{i}. {step}", body_style))
    
    story.append(Paragraph("Funcionalidad 'Cerrar Día'", heading2_style))
    story.append(Paragraph(
        "Cuando hayas completado tu lectura diaria, puedes presionar el botón <b>'Cerrar Día'</b> para: "
        "registrar tu progreso, activar el 'Estado Zen' (pantalla de descanso espiritual), "
        "y guardar las lecturas completadas en tu historial.",
        body_style
    ))
    
    story.append(Paragraph(
        "💡 <b>Tip:</b> Una vez cerrado el día, la interfaz cambia a modo contemplativo hasta el día siguiente.",
        tip_style
    ))
    
    story.append(PageBreak())
    
    # ========== BIBLIOTECA ==========
    story.append(Paragraph("6. 📚 Biblioteca", heading1_style))
    
    biblio_img = get_image("biblioteca")
    if biblio_img:
        story.append(Image(biblio_img, width=4*inch, height=4*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "La <b>Biblioteca Sagrada</b> es el corazón de Verbum Atlas. Aquí encontrarás todos los libros "
        "de la versión bíblica seleccionada, organizados visualmente como tarjetas.",
        body_style
    ))
    
    story.append(Paragraph("Navegación", heading2_style))
    
    story.append(Paragraph(
        "• <b>Vista de Tarjetas:</b> Cada libro muestra nombre, capítulos y color según categoría<br/>"
        "• <b>Filtros Rápidos:</b> Todos, A.T. (Antiguo Testamento), N.T. (Nuevo Testamento), L.M. (Libro de Mormón)<br/>"
        "• <b>Buscador:</b> Escribe parte del nombre de un libro para encontrarlo",
        body_style
    ))
    
    story.append(Paragraph("Leer un Capítulo", heading2_style))
    story.append(Paragraph(
        "1. Haz clic en la tarjeta del libro deseado<br/>"
        "2. Se mostrará una cuadrícula con todos los capítulos<br/>"
        "3. Haz clic en el número de capítulo que deseas leer<br/>"
        "4. Se abrirá el Lector con el texto completo",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== PANORAMA ==========
    story.append(Paragraph("7. 🌍 Panorama", heading1_style))
    
    pano_img = get_image("panorama")
    if pano_img:
        story.append(Image(pano_img, width=4*inch, height=4*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "El módulo <b>Panorama</b> te ayuda a comprender la estructura y el flujo histórico de la Biblia.",
        body_style
    ))
    
    story.append(Paragraph("Sub-secciones", heading2_style))
    
    pano_data = [
        ["Tab", "Contenido"],
        ["Tabla Periódica", "Visualización de géneros literarios (Ley, Historia, Poesía, Profecía, Evangelios, Cartas)"],
        ["Cronología", "Línea de tiempo desde la Creación hasta la consumación"]
    ]
    
    pano_table = Table(pano_data, colWidths=[1.5*inch, 4*inch])
    pano_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_GOLD),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(pano_table)
    
    story.append(PageBreak())
    
    # ========== LEX DIVINA ==========
    story.append(Paragraph("8. ✨ Lex Divina (Inteligencia Artificial)", heading1_style))
    
    lex_img = get_image("lex_divina")
    if lex_img:
        story.append(Image(lex_img, width=4*inch, height=4*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "<b>Lex Divina</b> es tu asistente teológico impulsado por <b>Google Gemini AI</b>. "
        "Puedes hacerle preguntas sobre las Escrituras y recibirás respuestas reflexivas basadas en principios cristianos.",
        body_style
    ))
    
    story.append(Paragraph("Configuración Inicial (Requerida)", heading2_style))
    
    api_steps = [
        "Visita <b>https://aistudio.google.com/app/apikey</b>",
        "Inicia sesión con tu cuenta de Google",
        "Haz clic en <b>'Create API Key'</b>",
        "Copia la clave generada",
        "En Verbum Atlas, haz clic en <b>'⚙️ Configurar API Key Gemini'</b>",
        "Pega tu clave y presiona <b>'💾 Guardar API Key'</b>"
    ]
    
    for i, step in enumerate(api_steps, 1):
        story.append(Paragraph(f"{i}. {step}", body_style))
    
    story.append(Paragraph(
        "🔐 <b>Seguridad:</b> Tu API Key se guarda localmente en tu computadora y no se comparte con terceros.",
        tip_style
    ))
    
    story.append(Paragraph("Ejemplos de preguntas:", heading2_style))
    story.append(Paragraph(
        "• ¿Qué enseña Pablo sobre la gracia en Romanos?<br/>"
        "• ¿Cuál es el significado del Salmo 23?<br/>"
        "• ¿Qué dice Alma sobre la fe?",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== MI DIARIO ==========
    story.append(Paragraph("9. 🧘 Mi Diario", heading1_style))
    
    diario_img = get_image("mi_diario")
    if diario_img:
        story.append(Image(diario_img, width=3.5*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "El <b>Diario Espiritual</b> te permite registrar tus reflexiones personales mientras lees las Escrituras.",
        body_style
    ))
    
    story.append(Paragraph("Estructura de una Entrada", heading2_style))
    
    diario_data = [
        ["Campo", "Propósito"],
        ["💡 Reflexión", "¿Qué ideas o pensamientos surgen de este texto?"],
        ["🚶 Aplicación", "¿Cómo lo voy a aplicar en mi vida hoy?"],
        ["❤️ Mensaje de Dios", "¿Qué siento que Dios me habla al corazón?"]
    ]
    
    diario_table = Table(diario_data, colWidths=[1.8*inch, 3.7*inch])
    diario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 1, colors.white)
    ]))
    story.append(diario_table)
    
    story.append(PageBreak())
    
    # ========== MIS APUNTES ==========
    story.append(Paragraph("10. 📝 Mis Apuntes", heading1_style))
    
    apuntes_img = get_image("mis_apuntes")
    if apuntes_img:
        story.append(Image(apuntes_img, width=3.5*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "<b>Mis Apuntes</b> es un espacio libre tipo 'tablero de notas' para guardar versículos favoritos, "
        "recordatorios o pensamientos rápidos.",
        body_style
    ))
    
    story.append(Paragraph("Características:", heading2_style))
    story.append(Paragraph(
        "• <b>Colores aleatorios:</b> Cada nota tiene un color de acento único<br/>"
        "• <b>Edición en vivo:</b> Los cambios se guardan automáticamente<br/>"
        "• <b>Eliminar:</b> Cada nota tiene un botón para borrarla",
        body_style
    ))
    
    story.append(Paragraph(
        "💡 <b>Idea:</b> Usa este espacio para anotar versículos que quieras memorizar o temas que deseas estudiar más adelante.",
        tip_style
    ))
    
    # ========== MI PROGRESO ==========
    story.append(Paragraph("11. 📈 Mi Progreso", heading1_style))
    
    progreso_img = get_image("mi_progreso")
    if progreso_img:
        story.append(Image(progreso_img, width=4*inch, height=4*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "El módulo de <b>Mi Progreso</b> te muestra estadísticas sobre tu lectura bíblica.",
        body_style
    ))
    
    prog_data = [
        ["Métrica", "Descripción"],
        ["Total", "Porcentaje global de capítulos leídos"],
        ["A.T.", "Progreso en el Antiguo Testamento"],
        ["N.T.", "Progreso en el Nuevo Testamento"],
        ["Meta Diaria", "Sugerencia de próximo capítulo a leer"]
    ]
    
    prog_table = Table(prog_data, colWidths=[1.5*inch, 4*inch])
    prog_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#059669")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 1, colors.white)
    ]))
    story.append(prog_table)
    
    story.append(PageBreak())
    
    # ========== AUDIO ==========
    story.append(Paragraph("12. 🔊 Lectura de Texto con Voz", heading1_style))
    
    audio_img = get_image("audio")
    if audio_img:
        story.append(Image(audio_img, width=3.5*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "Verbum Atlas incluye un motor de <b>Text-to-Speech (TTS)</b> para leer en voz alta los capítulos.",
        body_style
    ))
    
    story.append(Paragraph("Cómo Usarlo:", heading2_style))
    story.append(Paragraph(
        "1. Abre cualquier capítulo en el lector<br/>"
        "2. Busca el botón <b>'🔊 Escuchar'</b> en los controles superiores<br/>"
        "3. La aplicación comenzará a leer el texto en español<br/>"
        "4. Para detener, presiona <b>'⏹️ Detener'</b>",
        body_style
    ))
    
    story.append(Paragraph(
        "🎧 <b>Nota:</b> El motor de voz utiliza las voces instaladas en tu sistema Windows. "
        "Las voces en español (como Sabina o Helena) proporcionan mejor experiencia.",
        tip_style
    ))
    
    story.append(PageBreak())
    
    # ========== FAQ ==========
    story.append(Paragraph("13. ❓ Preguntas Frecuentes", heading1_style))
    
    faqs = [
        ("¿Necesito internet para usar Verbum Atlas?", 
         "No, excepto para el módulo Lex Divina (IA), que requiere conexión para comunicarse con los servidores de Google Gemini."),
        ("¿Puedo usar la aplicación en Mac o Linux?",
         "Actualmente, Verbum Atlas está diseñado exclusivamente para Windows. Futuras versiones podrían incluir soporte multiplataforma."),
        ("¿Mis datos están seguros?",
         "Sí. Todos tus datos se almacenan localmente en tu computadora. No se envía información personal a ningún servidor."),
        ("¿Por qué no veo el Libro de Mormón?",
         "Asegúrate de seleccionar 'Libro de Mormón (15 Libros)' en el selector de versión de la barra lateral."),
        ("¿Cómo reseteo mi progreso?",
         "Puedes eliminar manualmente la base de datos en: C:\\Users\\[Usuario]\\AppData\\Roaming\\VerbumAtlas2026\\user_history.db")
    ]
    
    for q, a in faqs:
        story.append(Paragraph(f"<b>P: {q}</b>", body_style))
        story.append(Paragraph(f"R: {a}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # ========== CRÉDITOS ==========
    story.append(Paragraph("14. Soporte y Créditos", heading1_style))
    
    story.append(Paragraph("Desarrollado por", heading2_style))
    story.append(Paragraph("<b>Fernando Ardón</b> en colaboración con <b>Antigravity AI</b>", center_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Recursos Utilizados", heading2_style))
    story.append(Paragraph(
        "• <b>Textos Bíblicos:</b> Dominio público (Torres Amat, Reina Valera 1909)<br/>"
        "• <b>Libro de Mormón:</b> Texto oficial en español<br/>"
        "• <b>Motor de IA:</b> Google Gemini<br/>"
        "• <b>Iconos:</b> Font Awesome<br/>"
        "• <b>Tipografías:</b> Outfit, Playfair Display (Google Fonts)",
        body_style
    ))
    
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("🙏 Que este recurso sea de bendición para tu vida espiritual 🙏", center_style))
    story.append(Paragraph("<b>Verbum Atlas 2026 - Enero 2026</b>", center_style))
    
    # Construir PDF
    doc.build(story)
    print(f"[OK] PDF generado exitosamente: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_manual()
