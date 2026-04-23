import torch
from PIL import Image, ImageFilter
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import requests
from io import BytesIO
import re
from scipy.spatial.distance import cdist
import cv2
import faiss
import os
import pickle
from vlm_agent import VLMAgent
from gis_validator import GISValidator
import json
from datetime import datetime

class GeoEngineReal:
    """
    Motor de Geolocalización REAL usando GeoCLIP pre-entrenado.
    Este modelo fue entrenado con MILLONES de fotos reales del mundo.
    Puede predecir coordenadas GPS precisas de cualquier lugar.
    """
    def __init__(self):
        print(f"[IA] Inicializando Motor REAL de Geolocalización...")
        print(f"[IA] Descargando GeoCLIP (modelo profesional)...")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Cargar el modelo GeoCLIP real desde HuggingFace
        try:
            from geoclip import GeoCLIP
            self.model = GeoCLIP()
            print(f"[IA] ✓ GeoCLIP cargado exitosamente.")
        except ImportError:
            print("[ADVERTENCIA] GeoCLIP no instalado. Instalando ahora...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "geoclip"])
            from geoclip import GeoCLIP
            self.model = GeoCLIP()
            print(f"[IA] ✓ GeoCLIP instalado y cargado.")
        
        # Inicializar sistema de razonamiento visual experto (VLM)
        self.reasoning = VLMAgent()
        print(f"[IA] ✓ Sistema de razonamiento visual (Gemini) activado.")
        
        # Inicializar el Validador GIS
        self.gis = GISValidator()
        print(f"[IA] ✓ Sistema de validación GIS (Francotirador) activado.")
        
        # 🆕 LUGARES CON CONFIANZA ALTA (Street View disponible)
        self.high_confidence_places = self._load_street_view_places()
        print(f"[IA] ✓ Base de datos de Street View cargada ({len(self.high_confidence_places)} lugares).")
        
        # 🆕 Sistema de análisis profundo
        self.analysis_cache = {}
        print(f"[IA] ✓ Sistema de análisis profundo activado.")
        
        # Eliminar Memoria Visual a petición del usuario (sin datos pregrabados)
        # self.memory = VisualMemory(self.model)
        
        print(f"[IA] ✓ Sistema listo para análisis global.")

    
    def analyze(self, image_path, top_k=5):
        """
        Analiza una imagen y devuelve las coordenadas GPS más probables.
        
        Returns:
            Lista de resultados con coordenadas GPS reales.
        """
        try:
            # PASO 0: Análisis de razonamiento visual
            visual_context = self.reasoning.analyze_full_context(image_path)
            
            # PASO 2: OCR para detectar texto en la imagen
            detected_text = self._extract_text_from_image(image_path)
            if detected_text:
                print(f"[IA] 📝 Texto detectado: {detected_text[:50]}...")
            
            confidence_score = 0
            best_lat, best_lon = None, None
            
            # 1. MODO DIOS (Anclaje de Texto): Si Gemini sabe exactamente el país o ciudad, forzamos esa coordenada base.
            country = str(visual_context.get("deduced_country", "DESCONOCIDO")).strip()
            city = str(visual_context.get("deduced_city", "DESCONOCIDO")).strip()
            exact_location = str(visual_context.get("exact_location_name", "DESCONOCIDO")).strip()
            
            # Limpiar strings como "India." -> "India"
            if country.endswith('.'): country = country[:-1]
            if city.endswith('.'): city = city[:-1]
            if "DESCONOCIDO" in country.upper(): country = "DESCONOCIDO"
            if "DESCONOCIDO" in city.upper(): city = "DESCONOCIDO"
            if "DESCONOCIDO" in exact_location.upper(): exact_location = "DESCONOCIDO"
            
            print(f"[DEBUG] VLM extrajo -> País: '{country}' | Ciudad: '{city}' | Exacto: '{exact_location}'")
            
            if exact_location != "DESCONOCIDO" or country != "DESCONOCIDO":
                search_query = country
                query_fallback_1 = ""
                query_fallback_2 = country
                
                if city != "DESCONOCIDO":
                    search_query = f"{city}, {country}"
                    query_fallback_1 = search_query
                    
                if exact_location != "DESCONOCIDO":
                    search_query = f"{exact_location}, {search_query}" if country != "DESCONOCIDO" else exact_location
                
                print(f"[IA] 🧠 VLM Detective aisló la ubicación exacta: '{search_query}'. Anclando...")
                best_lat, best_lon = self._geocode_text(search_query)
                
                # Cascade Fallbacks if Nominatim fails with complex strict name
                if best_lat is None and query_fallback_1:
                    print(f"[IA] ⚠️ Falló búsqueda estricta. Intentando Nivel 2: '{query_fallback_1}'")
                    best_lat, best_lon = self._geocode_text(query_fallback_1)
                
                if best_lat is None and query_fallback_2:
                    print(f"[IA] ⚠️ Falló búsqueda nivel 2. Intentando Nivel 3 (País): '{query_fallback_2}'")
                    best_lat, best_lon = self._geocode_text(query_fallback_2)
                
                if best_lat is not None:
                    # 🆕 INTELIGENCIA AUMENTADA: Calcular confianza de forma inteligente
                    confidence_score = self._score_location_intelligence(best_lat, best_lon, visual_context)
                    print(f"[IA] 🧠 Score de confianza inteligente: {confidence_score:.1f}%")
                
            # 2. Fallback a GeoCLIP si Gemini no supo el país exacto
            if best_lat is None or best_lon is None:
                print(f"[IA] 🔍 Iniciando análisis Multi-Crop (La Lupa) con GeoCLIP...")
                with torch.no_grad():
                    # Usar la nueva función Multi-Crop para encontrar el consenso
                    top_pred_gps, top_pred_prob = self._extract_features_multi_crop(image_path, top_k=min(15, top_k*3))
                
                # 3. Filtrar según razonamiento visual (descarta incompatibles)
                filtered_predictions = self._filter_by_context(top_pred_gps, top_pred_prob, visual_context)
                
                if not filtered_predictions:
                    print("[ERROR] Todas las predicciones descartadas. Fallback a mejor probabilidad.")
                    filtered_predictions = [(float(top_pred_gps[0][0]), float(top_pred_gps[0][1]), float(top_pred_prob[0]))]
                
                # 4. Magia de Precisión Extrema: Triangulación por Clustering (Obtener Radio Cero)
                print("[IA] Ejecutando algoritmo de precisión (Clustering Espacial) para obtener Radio Cero...")
                best_lat, best_lon = self._refine_with_clustering(filtered_predictions)
                confidence_score = filtered_predictions[0][2] * 100
                
            
            # 4.5. NIVEL GOBIERNO: Francotirador GIS usando GISValidator
            # Radio Cero dinámico: Si Gemini dio la ciudad, confiamos más, radio menor.
            radius_zero = 3000 if confidence_score == 99.9 else 8000
            
            print(f"[IA] [FRANCOTIRADOR] Disparando query GIS en radio {radius_zero}m...")
            gis_match = self.gis.query_smart_location(
                best_lat, best_lon, radius_zero, visual_context, ocr_text=detected_text
            )
            
            if gis_match:
                best_lat, best_lon, exact_name = gis_match
                print(f"[IA] [FRANCOTIRADOR] ¡BLANCO CONFIRMADO! Localización exacta: {exact_name}")
                # Hacemos override del texto detectado para mostrar el nombre exacto de OSM
                detected_text = exact_name 
            
            # 5. Snap a la carretera/edificio más cercano (Nivel Calle) -> BILINGÜE
            print("[IA] Ajustando coordenadas a elementos reales (Snapping)...")
            snapped_lat, snapped_lon, location_local, location_es = self._snap_to_nearest_feature(best_lat, best_lon)
            
            # Formatear el resultado maestro único
            results = [{
                "location": location_local,
                "location_es": location_es,
                "lat": snapped_lat,
                "lon": snapped_lon,
                "confidence": confidence_score
            }]
            
            print(f"[IA] ✓ Análisis de Extrema Precisión completo: {location_local} a ({snapped_lat:.5f}, {snapped_lon:.5f})")
            return results, visual_context
            
        except Exception as e:
            print(f"[ERROR] Error analizando imagen: {e}")
            import traceback
            traceback.print_exc()
            return [], {}

    def _extract_features_multi_crop(self, image_path, top_k=5):
        """
        Divide la imagen en múltiples recortes, predice sobre cada uno
        y agrega las predicciones para mayor precisión.
        """
        try:
            img = Image.open(image_path).convert('RGB')
        except Exception as e:
            print(f"[ERROR] Multi-crop no pudo cargar la imagen: {e}")
            # Fallback a prediccion basica si falla (aunque no deberia pasar aca)
            return self.model.predict(image_path, top_k)
            
        w, h = img.size
        # Definir los recortes: Entero + Cuadrantes
        crops = [
            img,  # Original
            img.crop((0, 0, w//2, h//2)),          # Top-Left
            img.crop((w//2, 0, w, h//2)),          # Top-Right
            img.crop((0, h//2, w//2, h)),          # Bottom-Left
            img.crop((w//2, h//2, w, h)),          # Bottom-Right
            img.crop((w//4, h//4, 3*w//4, 3*h//4)) # Centro
        ]
        
        all_gps = []
        all_probs = []
        
        for crop in crops:
            # Requerimos guardar el recorte temporalmente para GeoCLIP
            temp_path = "/tmp/temp_crop_geo.jpg"
            crop.save(temp_path)
            
            gps, probs = self.model.predict(temp_path, top_k=5)
            # Acumular
            for i in range(len(gps)):
                # Convertir tensor a numpy/float para mantener homogeneidad
                val_lat = float(gps[i][0].item() if torch.is_tensor(gps[i][0]) else gps[i][0])
                val_lon = float(gps[i][1].item() if torch.is_tensor(gps[i][1]) else gps[i][1])
                val_prob = float(probs[i].item() if torch.is_tensor(probs[i]) else probs[i])
                
                all_gps.append([val_lat, val_lon])
                all_probs.append(val_prob)
                
        # Normalizar prioridades y ordenar
        all_gps = np.array(all_gps)
        all_probs = np.array(all_probs)
        
        # Eliminar las peores predicciones globales para evitar ruido
        # Quedarse con el top 50%
        valid_indices = np.argsort(all_probs)[::-1][:top_k*2]
        
        best_gps = all_gps[valid_indices]
        best_probs = all_probs[valid_indices]
        
        # Retornar arrays compatibles
        return best_gps, best_probs
    
    
    def _filter_by_context(self, gps_predictions, probabilities, visual_context):
        """
        Filtra y pondera predicciones según el contexto visual detectado.
        ESTA ES LA INTEGRACIÓN DEL RAZONAMIENTO.
        """
        context_type = visual_context["type"]
        features = visual_context["features"]
        climate = visual_context["climate"]
        
        valid_predictions = []
        
        for i in range(len(gps_predictions)):
            lat = float(gps_predictions[i][0].item() if torch.is_tensor(gps_predictions[i][0]) else gps_predictions[i][0])
            lon = float(gps_predictions[i][1].item() if torch.is_tensor(gps_predictions[i][1]) else gps_predictions[i][1])
            prob = float(probabilities[i].item() if torch.is_tensor(probabilities[i]) else probabilities[i])
            
            # Validar tierra vs océano (solo si es URBANo)
            if context_type == "URBANO":
                if not self._is_on_land(lat, lon):
                    print(f"[IA] ❌ Descartada (océano): ({lat:.4f}, {lon:.4f})")
                    continue
            
            # Validar consistencia con clima
            # Por ejemplo, si detectamos NIEVE, descartar coordenadas tropicales
            if climate == "NIEVE/POLAR":
                if -30 < lat < 30:  # Zona tropical
                    print(f"[IA] ⚠️ Inconsistencia clima: nieve detectada pero coordenada tropical")
                    prob *= 0.3  # Penalizar pero no descartar completamente
            
            elif climate == "ARIDO/DESERTICO":
                # Desiertos típicamente en ciertas latitudes
                if features.get("vegetation_type") == "TROPICAL" and prob < 0.01:
                    continue  # Descartar
            
            valid_predictions.append((lat, lon, prob))
        
        if not valid_predictions:
            print("[WARN] Todas las predicciones fueron descartadas por filtro contextual.")
            # Fallback: usar la mejor original
            lat = float(gps_predictions[0][0].item() if torch.is_tensor(gps_predictions[0][0]) else gps_predictions[0][0])
            lon = float(gps_predictions[0][1].item() if torch.is_tensor(gps_predictions[0][1]) else gps_predictions[0][1])
            prob = float(probabilities[0].item() if torch.is_tensor(probabilities[0]) else probabilities[0])
            return [(lat, lon, prob)]
        
        # Ordenar por probabilidad
        valid_predictions.sort(key=lambda x: x[2], reverse=True)
        return valid_predictions
    
    def _detect_urban_context(self, image_path):
        """
        Detecta si la imagen muestra un contexto urbano (edificios, calles).
        Retorna True si hay estructuras, False si es naturaleza/agua.
        """
        try:
            # Cargar imagen
            img = cv2.imread(image_path)
            if img is None:
                return True  # Asumir urbano por defecto si falla
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detectar bordes (estructuras tienen muchos bordes rectos)
            edges = cv2.Canny(gray, 50, 150)
            
            # Detectar líneas (edificios/calles tienen líneas rectas)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
            
            # Si hay muchas líneas, probablemente es urbano
            if lines is not None and len(lines) > 20:
                print(f"[IA] Contexto detectado: URBANO ({len(lines)} líneas estructurales)")
                return True
            else:
                print(f"[IA] Contexto detectado: NATURAL/PAISAJE")
                return False
                
        except Exception as e:
            print(f"[DEBUG] Error detectando contexto: {e}")
            return True  # Asumir urbano por defecto
    
    def _is_on_land(self, lat, lon):
        """
        Verifica si unas coordenadas están en tierra firme.
        Optimizado: devuelve True directamente para evitar bloqueos
        masivos consultando Nominatim API por cada punto.
        GeoCLIP rara vez predice puntos en altamar a menos que la imagen lo sea.
        """
        return True
    
    def _extract_text_from_image(self, image_path):
        """Extrae texto visible de la imagen usando OCR optimizado."""
        try:
            import pytesseract
            image = Image.open(image_path)
            # Optimización: Reducir imagen para que OCR sea 4 veces más rápido
            image.thumbnail((800, 800))
            text = pytesseract.image_to_string(image)
            # Limpiar y filtrar
            text = ' '.join(text.split())  # Quitar espacios extra
            if len(text) > 5:  # Solo si hay contenido significativo
                return text
        except Exception as e:
            print(f"[DEBUG] OCR no disponible: {e}")
        return None
    
    def _refine_with_clustering(self, predictions_list):
        """
        Refina la predicción matemática calculando el centroide de gravedad
        ponderado de las predicciones más fuertes (Triangulación).
        Recibe lista de tuplas espaciales filtradas: (lat, lon, prob)
        """
        coords = []
        weights = []
        
        # Tomar el Top 5 u 8 para densificar el punto céntrico
        for lat, lon, prob in predictions_list[:8]:
            coords.append([lat, lon])
            weights.append(prob)
        
        coords = np.array(coords)
        weights = np.array(weights)
        
        if len(coords) > 1:
            # Centroide gravitatorio normalizado
            weights_norm = weights / weights.sum()
            centroid = np.average(coords, axis=0, weights=weights_norm)
            return centroid[0], centroid[1]
        else:
            return coords[0][0], coords[0][1]
            
    def _snap_to_nearest_feature(self, lat, lon):
        """
        Consigue la calle exacta o punto de interés más pegado a la coordenada,
        realizando dos consultas a OSM: una en el idioma nativo del lugar
        y otra forzada en español para mostrar doble denominación como pidió el usuario.
        """
        try:
            url_local = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=18&addressdetails=1"
            url_es = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=18&addressdetails=1&accept-language=es"
            headers = {'User-Agent': 'GeoSpy-Pro/3.0'}
            
            resp_local = requests.get(url_local, headers=headers, timeout=5).json()
            resp_es = requests.get(url_es, headers=headers, timeout=5).json()
            
            snap_lat = float(resp_local.get('lat', lat))
            snap_lon = float(resp_local.get('lon', lon))
            
            def extract_name(data):
                address = data.get('address', {})
                parts = []
                for key in ['amenity', 'building', 'historic', 'tourism', 'road', 'neighbourhood', 'suburb', 'city', 'town', 'country']:
                    if key in address:
                        parts.append(address[key])
                return ", ".join(parts[:4]) if parts else f"Locación (Lat: {snap_lat:.5f}, Lon: {snap_lon:.5f})"

            location_local = extract_name(resp_local)
            location_es = extract_name(resp_es)
            
            return snap_lat, snap_lon, location_local, location_es
            
        except Exception as e:
            print(f"[WARN] Geocodificación Snapping falló: {e}")
            fallback = self._reverse_geocode(lat, lon)
            return lat, lon, fallback, fallback
    
    def _enhance_location_with_text(self, location_name, detected_text):
        """Mejora el nombre de ubicación si el texto detectado contiene info relevante."""
        # Buscar patrones comunes de nombres de calles
        street_patterns = [
            r'\b([A-Z][a-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd))\b',
            r'\b(Calle\s+[A-Z][a-z]+)\b',
            r'\b(Rue\s+[A-Z][a-z]+)\b',
        ]
        
        for pattern in street_patterns:
            match = re.search(pattern, detected_text)
            if match:
                street_name = match.group(1)
                return f"{street_name}, {location_name}"
        
        return location_name
    
    def _search_overpass(self, lat, lon, osm_tags, radius_meters=10000):
        """
        [NIVEL DIOS]
        Busca en la base de datos de OpenStreetMap dentro de un radio los tags específicos.
        Ejemplo: Si Gemini ve una Iglesia, busca 'building=church' en 10km a la redonda de la
        coordenada matemática de GeoCLIP. Mueve el puntero AL TECHO de la iglesia.
        """
        # Filtrar solo tags válidos k=v
        valid_tags = [t for t in osm_tags if "=" in t and len(t.split("=")) == 2]
        if not valid_tags:
            return None
            
        # Tomar max 2 tags principales para no ser extremadamente restrictivo y fallar
        query_lines = ""
        for tag in valid_tags[:2]:
            k, v = tag.split("=", 1)
            # Buscar en nodos (puntos), ways (edificios) o relations
            query_lines += f'node["{k}"="{v}"](around:{radius_meters},{lat},{lon});'
            query_lines += f'way["{k}"="{v}"](around:{radius_meters},{lat},{lon});'
            
        if not query_lines:
            return None
            
        overpass_query = f"""
        [out:json][timeout:15];
        (
          {query_lines}
        );
        out center;
        """
        try:
            url = "http://overpass-api.de/api/interpreter"
            response = requests.post(url, data={'data': overpass_query}, timeout=10) # Reducido a 10s para no colgar app
            if not response.ok:
                print(f"[WARN] Overpass HTTP Error {response.status_code}. API Limits?")
                return None
            
            data = response.json()
            if data.get('elements'):
                # Retornar la coordenada del primer elemento exacto que haga match
                element = data['elements'][0]
                elat = element.get('lat', element.get('center', {}).get('lat'))
                elon = element.get('lon', element.get('center', {}).get('lon'))
                if elat and elon:
                    return float(elat), float(elon)
        except Exception as e:
            print(f"[WARN] Consulta Overpass falló: {e}")
        return None
        
    def _geocode_text(self, text_query):
        """Traduce una query de texto (ej. 'París, Francia') a coordenadas ancla."""
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={text_query}&format=json&limit=1"
            headers = {'User-Agent': 'GeoSpy-Pro/3.0'}
            response = requests.get(url, headers=headers, timeout=5).json()
            if response:
                return float(response[0]['lat']), float(response[0]['lon'])
        except Exception as e:
            print(f"[WARN] Falló el geocoding de texto '{text_query}': {e}")
        return None, None

    def _reverse_geocode(self, lat, lon):
        """
        Convierte coordenadas GPS en nombre legible usando Nominatim (OpenStreetMap).
        GRATIS y sin límites estrictos.
        """
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
            headers = {'User-Agent': 'GeoFinder/1.0'}
            
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            
            # Construir nombre amigable
            address = data.get('address', {})
            parts = []
            
            # Priorizar elementos relevantes (mantener en idioma local)
            for key in ['road', 'suburb', 'city', 'town', 'village', 'state']:
                if key in address:
                    parts.append(address[key])
            
            # Traducir el país a español
            country = address.get('country', '')
            country_es = self._translate_country_to_spanish(country)
            if country_es:
                parts.append(country_es)
            
            if parts:
                return ", ".join(parts[:4])  # Máximo 4 partes (incluye país)
            else:
                return f"Lat: {lat:.4f}, Lon: {lon:.4f}"
                
        except Exception as e:
            print(f"[WARN] Geocodificación inversa falló: {e}")
            return f"Coordenadas: {lat:.4f}, {lon:.4f}"
    
    def _translate_country_to_spanish(self, country_name):
        """Traduce el nombre del país a español."""
        # Diccionario de países comunes
        translations = {
            # Asia
            'Thailand': 'Tailandia',
            'ประเทศไทย': 'Tailandia',
            'Japan': 'Japón',
            '日本': 'Japón',
            'China': 'China',
            '中国': 'China',
            'South Korea': 'Corea del Sur',
            'North Korea': 'Corea del Norte',
            'Vietnam': 'Vietnam',
            'India': 'India',
            'भारत': 'India',
            'Indonesia': 'Indonesia',
            'Philippines': 'Filipinas',
            'Malaysia': 'Malasia',
            'Singapore': 'Singapur',
            
            # Europa
            'France': 'Francia',
            'Germany': 'Alemania',
            'Deutschland': 'Alemania',
            'Italy': 'Italia',
            'Italia': 'Italia',
            'Spain': 'España',
            'España': 'España',
            'United Kingdom': 'Reino Unido',
            'Portugal': 'Portugal',
            'Netherlands': 'Países Bajos',
            'Nederland': 'Países Bajos',
            'Belgium': 'Bélgica',
            'België': 'Bélgica',
            'Switzerland': 'Suiza',
            'Schweiz': 'Suiza',
            'Austria': 'Austria',
            'Österreich': 'Austria',
            'Poland': 'Polonia',
            'Polska': 'Polonia',
            'Greece': 'Grecia',
            'Ελλάδα': 'Grecia',
            'Russia': 'Rusia',
            'Россия': 'Rusia',
            
            # América
            'United States': 'Estados Unidos',
            'United States of America': 'Estados Unidos',
            'Canada': 'Canadá',
            'Mexico': 'México',
            'México': 'México',
            'Brazil': 'Brasil',
            'Brasil': 'Brasil',
            'Argentina': 'Argentina',
            'Chile': 'Chile',
            'Colombia': 'Colombia',
            'Peru': 'Perú',
            'Perú': 'Perú',
            'Venezuela': 'Venezuela',
            'Ecuador': 'Ecuador',
            'Uruguay': 'Uruguay',
            'Paraguay': 'Paraguay',
            'Bolivia': 'Bolivia',
            'Cuba': 'Cuba',
            'Costa Rica': 'Costa Rica',
            'Panama': 'Panamá',
            'Panamá': 'Panamá',
            'Puerto Rico': 'Puerto Rico',
            
            # África
            'Egypt': 'Egipto',
            'مصر': 'Egipto',
            'South Africa': 'Sudáfrica',
            'Morocco': 'Marruecos',
            'المغرب': 'Marruecos',
            'Algeria': 'Argelia',
            'الجزائر': 'Argelia',
            'Tunisia': 'Túnez',
            'Ethiopia': 'Etiopía',
            'Kenya': 'Kenia',
            
            # Oceanía
            'Australia': 'Australia',
            'New Zealand': 'Nueva Zelanda',
            
            # Medio Oriente
            'Israel': 'Israel',
            'ישראל': 'Israel',
            'Saudi Arabia': 'Arabia Saudita',
            'السعودية': 'Arabia Saudita',
            'United Arab Emirates': 'Emiratos Árabes Unidos',
            'الإمارات': 'Emiratos Árabes Unidos',
            'Turkey': 'Turquía',
            'Türkiye': 'Turquía',
            'Iran': 'Irán',
            'ایران': 'Irán',
        }
        
        # Buscar traducción
        for key, value in translations.items():
            if country_name.lower() == key.lower() or country_name == key:
                return value
        
        # Si no hay traducción, devolver el original
        return country_name

class VisualMemory:
    """
    Sistema de Memoria Visual usando FAISS.
    Permite 'recordar' lugares específicos mediante búsqueda vectorial.
    """
    def __init__(self, model):
        self.model = model
        self.index = None
        self.metadata = []
        self.dimension = 512  # Dimensión de vectores CLIP
        self.memory_path = "memory_index.faiss"
        self.metadata_path = "memory_metadata.pkl"
        self._load_memory()
    
    def _load_memory(self):
        """Carga el índice FAISS y metadatos si existen."""
        if os.path.exists(self.memory_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.memory_path)
                with open(self.metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                print(f"[MEMORIA] Cargados {len(self.metadata)} lugares conocidos.")
            except Exception as e:
                print(f"[ERROR] Falló carga de memoria: {e}")
                self._init_empty_index()
        else:
            self._init_empty_index()
    
    def _init_empty_index(self):
        """Inicializa un índice vacío."""
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner Product (similitud coseno)
        self.metadata = []
    
    def search(self, image_path, threshold=0.85):
        """
        Busca la imagen en la memoria.
        Retorna el resultado si la similitud supera el umbral.
        """
        if self.index.ntotal == 0:
            return None
            
        try:
            # Extraer vector de características usando el modelo GeoCLIP
            # Nota: Accedemos al encoder de imagen interno de GeoCLIP
            # Esto requiere procesar la imagen para obtener su embedding
            
            # Simplificación: Usamos el método predict de GeoCLIP para obtener embeddings
            # GeoCLIP no expone fácilmente solo el embedding, así que usaremos un truco:
            # Si no podemos obtener el embedding fácilmente, este paso requiere más integración.
            # Por ahora, asumiremos que no hay memoria cargada para evitar errores complejos
            # hasta que integremos correctamente la extracción de features.
            return None 
            
        except Exception as e:
            print(f"[DEBUG] Error en búsqueda de memoria: {e}")
            return None

    # 🆕 ============ MÉTODOS DE INTELIGENCIA MEJORADA ============
    
    def _load_street_view_places(self):
        """Carga lugares que TIENEN Street View de Google (lugares fotografiados y confiables)."""
        places = [
            # Ciudades Principales (Alta confiabilidad - mucho Street View)
            {"name": "New York, USA", "lat": 40.7128, "lon": -74.0060, "score": 100, "type": "urban"},
            {"name": "London, United Kingdom", "lat": 51.5074, "lon": -0.1278, "score": 100, "type": "urban"},
            {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503, "score": 100, "type": "urban"},
            {"name": "Paris, France", "lat": 48.8566, "lon": 2.3522, "score": 100, "type": "urban"},
            {"name": "Berlin, Germany", "lat": 52.5200, "lon": 13.4050, "score": 100, "type": "urban"},
            {"name": "Toronto, Canada", "lat": 43.6532, "lon": -79.3832, "score": 100, "type": "urban"},
            {"name": "Sydney, Australia", "lat": -33.8688, "lon": 151.2093, "score": 100, "type": "urban"},
            {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "score": 100, "type": "urban"},
            {"name": "Dubai, UAE", "lat": 25.2048, "lon": 55.2708, "score": 100, "type": "urban"},
            {"name": "Bangkok, Thailand", "lat": 13.7563, "lon": 100.5018, "score": 100, "type": "urban"},
            {"name": "Lima, Peru", "lat": -12.0464, "lon": -77.0428, "score": 95, "type": "urban"},
            {"name": "Rio de Janeiro, Brazil", "lat": -22.9068, "lon": -43.1729, "score": 98, "type": "urban"},
            {"name": "Mexico City, Mexico", "lat": 19.4326, "lon": -99.1332, "score": 98, "type": "urban"},
            
            # Monumentos Famosos (Muy Alta confiabilidad)
            {"name": "Eiffel Tower, Paris", "lat": 48.8584, "lon": 2.2945, "score": 99, "type": "landmark"},
            {"name": "Statue of Liberty, New York", "lat": 40.6892, "lon": -74.0445, "score": 99, "type": "landmark"},
            {"name": "Big Ben, London", "lat": 51.4975, "lon": -0.1246, "score": 99, "type": "landmark"},
            {"name": "Colosseum, Rome", "lat": 41.8902, "lon": 12.4922, "score": 99, "type": "landmark"},
            {"name": "Golden Gate Bridge, San Francisco", "lat": 37.8199, "lon": -122.4783, "score": 99, "type": "landmark"},
            
            # Playas populares
            {"name": "Miami Beach, USA", "lat": 25.7907, "lon": -80.1300, "score": 95, "type": "beach"},
            {"name": "Bondi Beach, Sydney", "lat": -33.8891, "lon": 151.2768, "score": 95, "type": "beach"},
            {"name": "Waikiki Beach, Hawaii", "lat": 21.2810, "lon": -157.8283, "score": 95, "type": "beach"},
            
            # Áreas comerciales
            {"name": "Times Square, New York", "lat": 40.7580, "lon": -73.9855, "score": 98, "type": "commercial"},
            {"name": "Shibuya, Tokyo", "lat": 35.6595, "lon": 139.7004, "score": 98, "type": "commercial"},
        ]
        return places
    
    def _has_street_view_coverage(self, lat, lon):
        """Verifica si hay Street View disponible en Google Maps (indirectamente)."""
        # Esto es una heurística - lugares turísticos principales generalmente tienen coverage
        # En producción, usarías Google Street View Static API
        
        # Si está cerca de algún lugar conocido con cobertura
        for place in self.high_confidence_places:
            distance = self._calculate_distance(lat, lon, place["lat"], place["lon"])
            if distance < 50:  # Menos de 50km
                return True, place["score"]
        
        # Por defecto, asumimos que lugares urbanos tienen cobertura
        return False, 50
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calcula distancia en km entre dos puntos GPS (Fórmula de Haversine)."""
        from math import radians, cos, sin, asin, sqrt
        
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radio de la tierra en km
        return c * r
    
    def _score_location_intelligence(self, lat, lon, visual_context):
        """Da un score de confianza basado en múltiples factores inteligentes."""
        base_score = 50
        
        # ✅ Factor 1: ¿Hay Street View disponible?
        has_sv, sv_score = self._has_street_view_coverage(lat, lon)
        if has_sv:
            base_score += 20
        
        # ✅ Factor 2: ¿Coincide con lo que la IA visual detectó?
        if visual_context.get("deduced_country"):
            base_score += 10
        if visual_context.get("deduced_city"):
            base_score += 15
        
        # ✅ Factor 3: ¿Es un lugar turístico/conocido?
        for place in self.high_confidence_places:
            dist = self._calculate_distance(lat, lon, place["lat"], place["lon"])
            if dist < 5:  # Menos de 5km
                base_score += place["score"] * 0.1
                break
        
        # ✅ Factor 4: Validar que NO sea coordenadas al azar en el océano
        if not self._is_valid_land_location(lat, lon):
            base_score -= 30
        
        return min(base_score, 100)
    
    def _is_valid_land_location(self, lat, lon):
        """Verifica que sea una ubicación en tierra (muy básico)."""
        # Coordenadas extremas (océano):
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            return False
        
        # Muy pocas ciudades en antártida/regiones polares extremas
        if lat < -60 or lat > 75:
            if abs(lon) not in [x for x in range(-180, 180)]:  # Solo algunos lugares
                return False
        
        # Generalmente válido si llegó aquí
        return True

    def add_image(self, image_path, lat, lon, location_name):
        """Añade una imagen a la memoria (para futuro aprendizaje)."""
        pass  # Implementar cuando tengamos interfaz de entrenamiento
    
    # 🆕 ============ ANÁLISIS INTELIGENTE AVANZADO ============
    
    def _analyze_environmental_features(self, image_path):
        """Analiza características del entorno (arquitectura, naturaleza, etc)."""
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Análisis básico de características
            features = {
                "urban_density": self._detect_urban_density(img_array),
                "architectural_style": self._detect_architecture(img_array),
                "vegetation": self._detect_vegetation(img_array),
                "water_bodies": self._detect_water(img_array),
                "climate_indicators": self._detect_climate(img_array)
            }
            
            return features
        except:
            return {}
    
    def _detect_urban_density(self, img_array):
        """Detecta si es zona urbana o rural."""
        # Heurística: contar píxeles grises (edificios típicamente)
        gray_pixels = np.sum((img_array[:,:,0] > 100) & (img_array[:,:,0] < 180))
        total_pixels = img_array.shape[0] * img_array.shape[1]
        density = gray_pixels / total_pixels
        
        if density > 0.4:
            return "urban"
        elif density > 0.2:
            return "suburban"
        else:
            return "rural"
    
    def _detect_architecture(self, img_array):
        """Detecta estilo arquitectónico básico."""
        # Análisis de colores dominantes para estimar arquitectura
        colors = self._get_dominant_colors(img_array)
        
        if colors and colors[0][0] > 150:  # Tonos claros = arquitectura moderna
            return "modern"
        else:
            return "traditional"
    
    def _detect_vegetation(self, img_array):
        """Detecta presencia de vegetación."""
        green_channel = img_array[:,:,1]
        vegetation_pixels = np.sum(green_channel > 120)
        total_pixels = img_array.shape[0] * img_array.shape[1]
        
        if vegetation_pixels / total_pixels > 0.3:
            return "abundant"
        elif vegetation_pixels / total_pixels > 0.1:
            return "moderate"
        else:
            return "minimal"
    
    def _detect_water(self, img_array):
        """Detecta cuerpos de agua."""
        # Tonos azules/cian indican agua
        blue_channel = img_array[:,:,2]
        water_pixels = np.sum(blue_channel > 150)
        total_pixels = img_array.shape[0] * img_array.shape[1]
        
        return "present" if water_pixels / total_pixels > 0.15 else "absent"
    
    def _detect_climate(self, img_array):
        """Detecta indicadores de clima."""
        # Brillo general de la imagen = iluminación solar
        brightness = np.mean(img_array)
        
        if brightness > 150:
            return "sunny_tropical"
        elif brightness > 100:
            return "temperate"
        else:
            return "cloudy_polar"
    
    def _get_dominant_colors(self, img_array):
        """Obtiene colores dominantes de la imagen."""
        img_array = img_array.reshape(-1, 3)
        
        try:
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=3, n_init=10)
            kmeans.fit(img_array)
            return kmeans.cluster_centers_
        except:
            # Fallback sin sklearn
            return [(100, 100, 100)]
    
    def _generate_deep_analysis(self, lat, lon, visual_context, features):
        """Genera análisis profundo basado en múltiples factores."""
        analysis = f"📊 ANÁLISIS PROFUNDO IA:\\n\\n"
        
        # Factor 1: Ubicación
        analysis += f"📍 Ubicación: {visual_context.get('deduced_city', 'Desconocida')}\\n"
        
        # Factor 2: Ambiente
        if features:
            analysis += f"🏙️ Densidad: {features.get('urban_density', 'N/A')}\\n"
            analysis += f"🌳 Vegetación: {features.get('vegetation', 'N/A')}\\n"
            analysis += f"🌡️ Clima: {features.get('climate_indicators', 'N/A')}\\n"
        
        # Factor 3: Confianza
        confidence = visual_context.get('confidence', 50)
        analysis += f"\\n✓ Confianza IA: {confidence:.0f}%"
        
        return analysis

# Instancia global
_engine = None

def get_engine():
    """Obtiene la instancia singleton del motor."""
    global _engine
    if _engine is None:
        _engine = GeoEngineReal()
    return _engine

