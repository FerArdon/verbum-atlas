import sys
import os
import sqlite3
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon # Importante
from PyQt5.QtWebEngineWidgets import QWebEngineView
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
            genai.configure(api_key='AIzaSyAcTLrFJND4zfFNeINcbSr-yfWh-jwtyQg')
            self.api_key = 'AIzaSyAcTLrFJND4zfFNeINcbSr-yfWh-jwtyQg'
            print('Backend: API Key integrada exitosamente.')
        except Exception as e:
            print(f'Error config API Key: {e}')
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
            return json.dumps({"error": "No has configurado tu API Key de Gemini."})
        
        try:
            model = genai.GenerativeModel("models/gemini-flash-latest")
            
            system_instruction = "Eres 'Lex Divina', un agente experto en teología bíblica y guía espiritual. Tu propósito es ayudar al usuario a interpretar la Biblia de forma profunda, respetuosa y reflexiva. Siempre mantén un tono humilde, sabio y alentador. Si se te pasa un texto bíblico de contexto, úsalo para dar una interpretación detallada basada en la sana doctrina, la historia y la aplicación práctica. No generes contenido que contradiga los valores cristianos."
            
            prompt = f"{system_instruction}\n\nContexto lectura: {context}\n\nPregunta: {question}"
            response = model.generate_content(prompt)
            return json.dumps({"answer": response.text})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @pyqtSlot(str, int, result=str)
    def getChapterText(self, book_name_ui, chapter):
        # 0. Si es modo Mormón
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
        
        # Deshabilitar caché para evitar problemas de actualización
        self.browser.page().profile().setHttpCacheType(0) # NoCache
        self.browser.page().profile().clearHttpCache()
        
        file_path = resource_path("index.html")
        self.browser.load(QUrl.fromLocalFile(file_path))
        self.setCentralWidget(self.browser)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BibleMapApp()
    window.showMaximized()
    sys.exit(app.exec_())
