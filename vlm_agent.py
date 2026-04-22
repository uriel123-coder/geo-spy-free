import os
import json
from google import genai
from google.genai import types
from PIL import Image

class VLMAgent:
    """
    Inteligencia de Visión (VLM) usando Gemini para emular a un experto de GeoGuessr.
    Extrae pistas de muy alto nivel (lenguaje, flora, arquitectura) 
    para potenciar exponencialmente a GeoCLIP.
    """
    
    def __init__(self):
        # API Key proporcionada por el usuario para acceso SOTA
        self.api_key = "AIzaSyCT-Bb0umrU9CZoPSfa5Eiq0Wzf1h4LKyQ"
        if not self.api_key:
            print("\n[!] ========================================================")
            print("[!] ADVERTENCIA VLM: GEMINI_API_KEY no encontrada.")
            print("[!] El sistema funcionará, pero sin el 'Cerebro de Detective'.")
            print("[!] Por favor, ingresa tu API Key en la terminal o código.")
            print("[!] ========================================================\n")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
            print("[IA] ✓ VLM Agent (Gemini Detective) conectado y listo.")

    def analyze_full_context(self, image_path):
        """
        Analiza la imagen usando Gemini (Flash/Pro) y retorna un JSON
        estructurado con deducciones a nivel 'GeoGuessr'.
        """
        if not self.client:
            return self._mock_context()
            
        print("[RAZONAMIENTO] VLM Detective: Analizando imagen con Gemini...")
        
        try:
            image = Image.open(image_path)
            # Reducir imagen para que consuma menos tokens y responda en 2 segundos
            image.thumbnail((1024, 1024))
            
            prompt = '''
            Actúa como un jugador Campeón Mundial de GeoGuessr. Analiza detalladamente esta imagen para localizar dónde fue tomada.
            Revisa a fondo: idioma o alfabeto de los letreros, arquitectura, marcas viales, diseño de postes de luz, sentido del tráfico, flora, y geografía.
            
            Responde ÚNICA Y EXCLUSIVAMENTE con un JSON válido usando EXACTAMENTE esta estructura en español:
            {
                "type": "URBANO o RURAL",
                "sub_type": "CENTRO_CIUDAD, SUBURBIO, INDUSTRIAL, DESIERTO, SELVA, BOSQUE, CAMPO o PLAYA",
                "time_of_day": "DIA o NOCHE",
                "climate": "ARIDO, TROPICAL, TEMPLADO o FRIO",
                "features": {
                    "País/Región Deducida": "Explicación detallada de por qué crees que es este país.",
                    "Idioma y Texto": "¿Ves algún texto, letrero o alfabeto? ¿En qué idioma?",
                    "Arquitectura": "Estilo de los edificios o casas.",
                    "Infraestructura Vial": "Líneas de la calle, postes, placas de autos, tipo de asfalto."
                },
                "osm_tags": ["etiquetas OpenStreetMap probables formato clave=valor", "ej: amenity=restaurant", "historic=ruins", "building=church", "tourism=museum", "natural=beach"],
                "deduced_country": "OBLIGATORIO: Nombre corto del país en ESPAÑOL (ej. India, Francia, Tailandia, Mexico).",
                "deduced_city": "OBLIGATORIO: Nombre de la ciudad exacta o provincia si hay pistas visuales. Si no hay pistas, escribe DESCONOCIDO",
                "exact_location_name": "Si conoces el nombre de este lugar exacto, edificio o monumento al 100%, ponlo aquí. Si no, DESCONOCIDO"
            }
            IMPORTANTE: No uses etiquetas markdown (como ```json). Sólo imprime el JSON de corrido.
            '''
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[image, prompt],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                )
            )
            
            # Limpieza del string JSON
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
                
            context = json.loads(text.strip())
            print(f"[RAZONAMIENTO] DEDUCCIÓN VLM: {context.get('features', {}).get('País/Región Deducida', 'Contexto analizado')}")
            return context
            
        except Exception as e:
            print(f"[VLM ERROR] Falló el análisis avanzado de Gemini: {e}")
            return self._mock_context()
            
    def _mock_context(self):
        """Contexto de emergencia si falla la API o falta la llave."""
        return {
            "type": "URBANO", "sub_type": "GENERICO", 
            "time_of_day": "DIA", "climate": "TEMPLADO", 
            "features": {"Aviso Sistema": "Falta la clave API GEMINI_API_KEY para habilitar deducciones expertas en tiempo real."}
        }
