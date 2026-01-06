import sys
import os
import sqlite3
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon # Importante
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from PyQt5.QtWebChannel import QWebChannel
import google.generativeai as genai

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

import pyttsx3
import threading
import pythoncom
import time

import queue # Importar Queue

class BackendHandler(QObject):
    def __init__(self):
        super().__init__()
        
        # Cola de mensajes para el TTS
        self.speech_queue = queue.Queue()
        try:
            # genai.configure(api_key='...') # Eliminada clave hardcodeada
            self.api_key = None
            print('Backend: Inicializado. Configura tu API Key en la interfaz.')
        except Exception as e:
            print(f'Error config inical: {e}')
        self.engine = None
        self.is_running = True
        
        # Iniciar Hilo de Voz Persistente
        t = threading.Thread(target=self._tts_worker)
        t.daemon = True
        t.start()

        # Rutas de las bases de datos (Usando resource_path)
        self.db_catholic = resource_path("biblia_catolica.db")
        self.db_protestant = resource_path("biblia.db")
        self.db_mormon = resource_path("libro_mormon.db")
        
        # Fix Persistencia: Mover DB de usuario a AppData
        app_data = os.path.join(os.getenv('APPDATA'), 'VerbumAtlas2026')
        if not os.path.exists(app_data):
            os.makedirs(app_data, exist_ok=True)
        self.db_user_path = os.path.join(app_data, "user_history.db")
        
        # Inicializar DB de usuario
        self._init_user_db()
        
        # Estado actual (por defecto Católica)
        self.current_db = self.db_catholic
        self.is_catholic_mode = True
        self.current_mode = "catholic"  # catholic, protestant, mormon
        self.gemini_key = None
        
        # ... (Mappings se mantienen igual) ...
        # MAPEO CATÓLICO
        self.map_catholic = {
            "Génesis": 10, "Éxodo": 20, "Levítico": 30, "Números": 40, "Deuteronomio": 50,
            "Josué": 60, "Jueces": 70, "Rut": 80, "1 Samuel": 90, "2 Samuel": 100,
            "1 Reyes": 110, "2 Reyes": 120, "1 Crónicas": 130, "2 Crónicas": 140,
            "Esdras": 150, "Nehemías": 160, "Tobías": 170, "Judit": 180, "Ester": 190,
            "Job": 220, "Salmos": 230, "Proverbios": 240, "Eclesiastés": 250, "Cantar": 260,
            "Sabiduría": 270, "Eclesiástico": 280, "Isaías": 290, "Jeremías": 300,
            "Lamentaciones": 310, "Baruc": 320, "Ezequiel": 330, "Daniel": 340,
            "Oseas": 350, "Joel": 360, "Amós": 370, "Abdías": 380, "Jonás": 390,
            "Miqueas": 400, "Nahúm": 410, "Habacuc": 420, "Sofonías": 430, "Hageo": 440,
            "Zacarías": 450, "Malaquías": 460, "1 Macabeos": 462, "2 Macabeos": 464,
            "Mateo": 470, "Marcos": 480, "Lucas": 490, "Juan": 500, "Hechos": 510,
            "Romanos": 520, "1 Corintios": 530, "2 Corintios": 540, "Gálatas": 550,
            "Efesios": 560, "Filipenses": 570, "Colosenses": 580, "1 Tesalonicenses": 590,
            "2 Tesalonicenses": 600, "1 Timoteo": 610, "2 Timoteo": 620, "Tito": 630,
            "Filemón": 640, "Hebreos": 650, "Santiago": 660, "1 Pedro": 670,
            "2 Pedro": 680, "1 Juan": 690, "2 Juan": 700, "3 Juan": 710, "Judas": 720,
            "Apocalipsis": 730
        }

        # MAPEO PROTESTANTE
        self.map_protestant = {
            "Génesis": 1, "Éxodo": 2, "Levítico": 3, "Números": 4, "Deuteronomio": 5, "Josué": 6, "Jueces": 7, "Rut": 8, "1 Samuel": 9, "2 Samuel": 10, "1 Reyes": 11, "2 Reyes": 12, "1 Crónicas": 13, "2 Crónicas": 14, "Esdras": 15, "Nehemías": 16, "Ester": 17, "Job": 18, "Salmos": 19, "Proverbios": 20, "Eclesiastés": 21, "Cantar": 22, "Isaías": 23, "Jeremías": 24, "Lamentaciones": 25, "Ezequiel": 26, "Daniel": 27, "Oseas": 28, "Joel": 29, "Amós": 30, "Abdías": 31, "Jonás": 32, "Miqueas": 33, "Nahúm": 34, "Habacuc": 35, "Sofonías": 36, "Hageo": 37, "Zacarías": 38, "Malaquías": 39,
            "Mateo": 40, "Marcos": 41, "Lucas": 42, "Juan": 43, "Hechos": 44, "Romanos": 45, "1 Corintios": 46, "2 Corintios": 47, "Gálatas": 48, "Efesios": 49, "Filipenses": 50, "Colosenses": 51, "1 Tesalonicenses": 52, "2 Tesalonicenses": 53, "1 Timoteo": 54, "2 Timoteo": 55, "Tito": 56, "Filemón": 57, "Hebreos": 58, "Santiago": 59, "1 Pedro": 60, "2 Pedro": 61, "1 Juan": 62, "2 Juan": 63, "3 Juan": 64, "Judas": 65, "Apocalipsis": 66
        }

    def _configure_voice_for_engine(self, engine):
        try:
            voices = engine.getProperty('voices')
            target_voice = None
            for voice in voices:
                name = voice.name.lower()
                if 'sabina' in name or 'helena' in name or 'elena' in name:
                    target_voice = voice.id
                    break
                if not target_voice and ('spanish' in name or 'mexico' in name or 'spain' in name):
                    target_voice = voice.id
            if target_voice:
                engine.setProperty('voice', target_voice)
            engine.setProperty('rate', 150)
        except:
            pass

    def _tts_worker(self):
        """Worker ETERNO que procesa la cola"""
        pythoncom.CoInitialize()
        try:
            self.engine = pyttsx3.init()
            self._configure_voice_for_engine(self.engine)
            
            while True:
                text = self.speech_queue.get() # Bloquea hasta que haya algo
                if text is None: break # Pill de veneno para cerrar si fuera necesario
                
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as inner:
                    print(f"Error reproduciendo: {inner}")
                    self.engine = pyttsx3.init() # Intento de resurrección
        except Exception as e:
            print("Error fatal TTS worker:", e)
        finally:
            pythoncom.CoUninitialize()

    @pyqtSlot(str)
    def speak(self, text):
        """Encola el texto para hablar"""
        # 1. Detener lo actual
        self.stop_speaker()
        
        # 2. Limpiar cola pendiente (vaciar buffer)
        with self.speech_queue.mutex:
            self.speech_queue.queue.clear()
            
        # 3. Encolar nuevo
        self.speech_queue.put(text)

    @pyqtSlot()
    def stop_speaker(self):
        """Ordena al motor detenerse"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

    @pyqtSlot(str, result=str)
    def setVersion(self, version):
        """Cambia la base de datos activa"""
        print(f"Backend: Cambiando versión a {version}")
        self.current_mode = version
        
        if version == "catholic":
            self.current_db = self.db_catholic
            self.is_catholic_mode = True
            return "Versión Católica Activada (Torres Amat)"
        elif version == "protestant":
            self.current_db = self.db_protestant
            self.is_catholic_mode = False
            return "Versión Protestante Activada (RVR 1909)"
        elif version == "mormon":
            self.current_db = self.db_mormon
            self.is_catholic_mode = False
            return "Libro de Mormón Activado"
        else:
            return "Versión no reconocida"

    @pyqtSlot(str, int, result=str)
    def getDailyReading(self, month_name, day):
        """Devuelve la lectura matutina del JSON extraído del PDF"""
        try:
            # 1. (Verificación de estado eliminada para permitir lectura persistente)
            # El frontend gestionará el bloqueo de inputs independientemente.
            
            # 2. Obtener lectura
             # Normalizar mes a minúsculas
            mes_key = month_name.lower().replace('é', 'e').replace('á', 'a').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            # Meses en el JSON están como 'enero', 'febrero'...
            key = f"{mes_key}_{day}"
            
            path = resource_path("daily_readings.json")
            if not os.path.exists(path):
                return json.dumps({"error": "Archivo de lecturas no encontrado."})
            
            with open(path, "r", encoding="utf-8") as f:
                readings = json.load(f)
            
            content = readings.get(key, "No hay lectura para este día.")
            return json.dumps({"content": content})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @pyqtSlot(str)
    def setApiKey(self, key):
        self.gemini_key = key
        genai.configure(api_key=key)
        print("Backend: API Key de Gemini configurada.")

    @pyqtSlot(str, str, result=str)
    def askAgent(self, context, question):
        if not self.gemini_key:
            return json.dumps({"error": "No has configurado tu API Key de Gemini."}, ensure_ascii=False)
        
        try:
            model = genai.GenerativeModel("models/gemini-flash-latest")
            
            system_instruction = "Eres 'Lex Divina', un agente experto en teología bíblica y guía espiritual. Tu propósito es ayudar al usuario a interpretar la Biblia de forma profunda, respetuosa y reflexiva. Siempre mantén un tono humilde, sabio y alentador. Si se te pasa un texto bíblico de contexto, úsalo para dar una interpretación detallada basada en la sana doctrina, la historia y la aplicación práctica. No generes contenido que contradiga los valores cristianos."
            
            prompt = f"{system_instruction}\n\nContexto lectura: {context}\n\nPregunta: {question}"
            response = model.generate_content(prompt)
            return json.dumps({"answer": response.text}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)


    @pyqtSlot(str, int, result=str)
    def getChapterText(self, book_name_ui, chapter):
        # 0. Si es modo Mormón
        if self.current_mode == "mormon":


            try:
                conn = sqlite3.connect(self.db_mormon)
                cursor = conn.cursor()
                
                # Query with JOINs for the normalized schema
                # Intento 1: Búsqueda exacta
                query = """
                    SELECT v.numero, v.texto 
                    FROM versiculos v
                    JOIN capitulos c ON v.capitulo_id = c.id
                    JOIN libros l ON c.libro_id = l.id
                    WHERE l.nombre = ? AND c.numero = ?
                    ORDER BY v.numero ASC
                """
                cursor.execute(query, (book_name_ui, chapter))
                rows = cursor.fetchall()
                
                # Intento 2: Si falla, búsqueda flexible (LIKE)
                if not rows:
                    print(f"Backend: Exact match failed for '{book_name_ui}', trying LIKE...")
                    query_like = """
                        SELECT v.numero, v.texto 
                        FROM versiculos v
                        JOIN capitulos c ON v.capitulo_id = c.id
                        JOIN libros l ON c.libro_id = l.id
                        WHERE l.nombre LIKE ? AND c.numero = ?
                        ORDER BY v.numero ASC
                    """
                    cursor.execute(query_like, (f"%{book_name_ui}%", chapter))
                    rows = cursor.fetchall()

                conn.close()
                
                # Map results (numero -> verse, texto -> text)
                result = [{"verse": r[0], "text": r[1]} for r in rows]
                
                if not result:
                    print(f"Backend: Failed to find text for {book_name_ui} {chapter}")
                    return json.dumps({"error": f"Capítulo {chapter} de {book_name_ui} sin texto disponible."}, ensure_ascii=False)
                return json.dumps(result, ensure_ascii=False)
            except Exception as e:
                print(f"Backend Error: {str(e)}")
                return json.dumps({"error": f"Error SQL Mormón: {str(e)}"}, ensure_ascii=False)

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
            return json.dumps({"error": f"Libro '{book_name_ui}' no encontrado en versión actual."}, ensure_ascii=False)

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
                return json.dumps({"error": "Capítulo sin texto disponible."}, ensure_ascii=False)
                
            return json.dumps(result, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"error": f"Error SQL: {str(e)}"}, ensure_ascii=False)

    # --- NUEVA FUNCIONALIDAD: PERSISTENCIA DIARIA Y CIERRE DE SESIÓN ---

    def _init_user_db(self):
        """Inicializa la base de datos de usuario si no existe"""
        try:
            conn = sqlite3.connect(self.db_user_path)
            cursor = conn.cursor()
            # Tabla simple para guardar el estado del día
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_history (
                    date_iso TEXT PRIMARY KEY,
                    readings_json TEXT,
                    status TEXT
                )
            ''')
            conn.commit()
            conn.close()
            print("Backend: DB Usuario inicializada.")
        except Exception as e:
            print(f"Backend: Error iniciando DB usuario: {e}")

    def _get_iso_date(self, month_name, day):
        """Convierte mes y día a formato YYYY-MM-DD asumiendo año actual"""
        import datetime
        meses = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
            "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }
        # Limpiar string
        m_key = month_name.lower().strip()
        # Eliminar tildes por si acaso
        m_key = m_key.replace('é', 'e').replace('á', 'a').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        
        month_num = meses.get(m_key, 1)
        year = datetime.datetime.now().year
        return f"{year}-{month_num:02d}-{day:02d}"

    @pyqtSlot(str, result=str)
    def closeDailySession(self, data_json):
        """
        Recibe JSON con { 'date': 'YYYY-MM-DD' (opcional), 'readings': {...} }
        Si no viene fecha, usa la de hoy.
        Guarda en SQLite y marca status='CLOSED'.
        """
        import datetime
        try:
            data = json.loads(data_json)
            
            # Determinar fecha
            date_iso = data.get('date')
            if not date_iso:
                # Fallback a hoy si el frontend no la envía
                date_iso = datetime.datetime.now().strftime("%Y-%m-%d")
            
            readings = json.dumps(data.get('readings', {}))
            status = "CLOSED"

            conn = sqlite3.connect(self.db_user_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO daily_history (date_iso, readings_json, status)
                VALUES (?, ?, ?)
            ''', (date_iso, readings, status))
            
            conn.commit()
            conn.close()
            
            return json.dumps({"status": "success", "message": "Día cerrado correctamente."})
            
        except Exception as e:
            print(f"Error closing session: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    @pyqtSlot(str, result=str)
    def checkDailyStatus(self, date_iso):
        """Permite al frontend verificar explícitamente el estado de una fecha"""
        try:
            conn = sqlite3.connect(self.db_user_path)
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM daily_history WHERE date_iso=?", (date_iso,))
            row = cursor.fetchone()
            conn.close()
            
            st = row[0] if row else "OPEN"
            return json.dumps({"date": date_iso, "status": st})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @pyqtSlot(result=str)
    def getUserStatistics(self):
        """Calcula estadísticas de lectura y sugiere siguiente lectura"""
        try:
            conn = sqlite3.connect(self.db_user_path)
            cursor = conn.cursor()
            
            # 1. Obtener todos los registros para estadísticas
            cursor.execute("SELECT readings_json, date_iso FROM daily_history WHERE status='CLOSED' ORDER BY date_iso DESC")
            rows = cursor.fetchall() # Ordenados del más reciente al más antiguo
            conn.close()

            unique_chapters = set()
            unique_books = set()
            
            # Para sugerencia (usamos el registro más reciente)
            suggestion = None
            if rows:
                try:
                    last_data = json.loads(rows[0][0]) # El más reciente
                    last_chapters = last_data.get('chapters_covered', [])
                    if last_chapters and isinstance(last_chapters, list):
                        # Tomar el último de la lista de ese día
                        last_read = last_chapters[-1] 
                        if 'bookName' in last_read and 'chapter' in last_read:
                            # Sugerir el siguiente
                            suggestion = {
                                "bookName": last_read['bookName'],
                                "chapter": int(last_read['chapter']) + 1,
                                "type": "continue"
                            }
                except:
                    pass

            for row in rows:
                try:
                    data = json.loads(row[0])
                    chapters = data.get('chapters_covered', [])
                    
                    if isinstance(chapters, list):
                        for cap in chapters:
                            if isinstance(cap, dict) and 'bookName' in cap and 'chapter' in cap:
                                key = f"{cap['bookName']}_{cap['chapter']}"
                                unique_chapters.add(key)
                                unique_books.add(cap['bookName'])
                except Exception as json_err:
                    print(f"Error parsing history row: {json_err}")
                    continue

            chapters_read = len(unique_chapters)
            books_started = len(unique_books)

            # Denominador según modo
            total_reference = 1334 # Catholic default
            if self.current_mode == 'protestant':
                total_reference = 1189
            elif self.current_mode == 'mormon':
                total_reference = 239
            
            progress_percent = 0.0
            if total_reference > 0:
                progress_percent = round((chapters_read / total_reference) * 100, 1)

            return json.dumps({
                "chapters_read": chapters_read,
                "books_started": books_started,
                "progress_percent": progress_percent,
                "total_chapters_reference": total_reference,
                "suggestion": suggestion
            })

        except Exception as e:
            print(f"Error calculating stats: {e}")
            return json.dumps({
                "chapters_read": 0,
                "books_started": 0,
                "progress_percent": 0.0,
                "total_chapters_reference": 1334,
                "error": str(e)
            })


class BibleMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verbum Atlas 2026")
        self.setWindowIcon(QIcon(resource_path("app_icon.png")))
        self.resize(1280, 850)
        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self.backend = BackendHandler() # Init
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)
        
        # Configurar perfil persistente para que localStorage funcione correctamente
        profile = QWebEngineProfile.defaultProfile()
        storage_path = os.path.join(os.getenv('APPDATA'), 'VerbumAtlas2026')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path, exist_ok=True)
        
        profile.setPersistentStoragePath(storage_path)
        profile.setCachePath(storage_path)
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache) # Usar disco para persistencia
        
        # self.browser.page().profile().setHttpCacheType(0) # Old no-cache
        
        file_path = resource_path("index.html")
        self.browser.load(QUrl.fromLocalFile(file_path))
        self.setCentralWidget(self.browser)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BibleMapApp()
    window.showMaximized()
    sys.exit(app.exec_())
