"""
Validador GIS Dinámico - Arquitectura "Francotirador"
Usa Overpass API (OpenStreetMap) para encontrar la ubicación exacta dentro del Radio Cero.
"""
import overpy
import math
from functools import lru_cache

class GISValidator:
    def __init__(self):
        self.api = overpy.Overpass()
        print("[GIS] Validator OSINT activado. Conectado a Overpass API.")
        
    def query_smart_location(self, lat, lon, radius_meters, visual_context, ocr_text=None):
        """
        Genera y ejecuta una query dinámica en OSM basada en el contexto.
        Retorna la coordenada exacta si hay una coincidencia fuerte.
        """
        print(f"\n[GIS] 🎯 Iniciando protocolo francotirador en: {lat:.5f}, {lon:.5f} (Radio: {radius_meters}m)")
        
        # 1. Extraer entidades interesantes del contexto
        osm_tags = self._translate_features_to_osm_tags(visual_context)
        
        # 2. Si hay OCR, la prioridad máxima es encontrar ese nombre
        if ocr_text:
            cleaned_text = self._clean_ocr(ocr_text)
            if len(cleaned_text) > 3:
                print(f"[GIS] Buscando nombre específico: '{cleaned_text}'")
                result = self._query_name(lat, lon, radius_meters, cleaned_text)
                if result:
                    return result
                    
        # 3. Si no hay OCR pero hay entidades fuertes (ej. puente, gasolinera)
        if osm_tags:
            print(f"[GIS] Buscando entidades semánticas: {osm_tags}")
            result = self._query_entities(lat, lon, radius_meters, osm_tags)
            if result:
                return result
                
        print("[GIS] ⚠️ Sin intersección exacta en OpenStreetMap. Manteniendo coordenada original.")
        return None

    def _query_name(self, lat, lon, radius, name):
        """Busca un nodo/vía por nombre usando expresión regular (insensible a mayúsculas)."""
        # Escapar comillas para evitar inyecciones en Overpass
        safe_name = name.replace('"', '').replace("'", "")
        
        # Query Overpass (busca name que contenga la palabra)
        query = f"""
        [out:json][timeout:15];
        (
          node["name"~"{safe_name}",i](around:{radius},{lat},{lon});
          way["name"~"{safe_name}",i](around:{radius},{lat},{lon});
        );
        out center;
        """
        try:
            result = self.api.query(query)
            if result.nodes:
                n = result.nodes[0]
                print(f"      📍 ¡BULLSEYE! Encontrado nodo exacto: {n.tags.get('name', '')}")
                return float(n.lat), float(n.lon), n.tags.get('name', '')
            elif result.ways:
                w = result.ways[0]
                print(f"      📍 ¡BULLSEYE! Encontrado edificio/vía exacta: {w.tags.get('name', '')}")
                return float(w.center_lat), float(w.center_lon), w.tags.get('name', '')
        except Exception as e:
            print(f"      [GIS Error] Overpass API: {e}")
        return None
        
    def _query_entities(self, lat, lon, radius, tags):
        """Busca combinaciones de entidades (ej: amenity=pharmacy)."""
        if not tags: return None
        
        for k, v in tags.items():
            query = f"""
            [out:json][timeout:15];
            (
              node["{k}"="{v}"](around:{radius},{lat},{lon});
              way["{k}"="{v}"](around:{radius},{lat},{lon});
            );
            out center;
            """
            try:
                result = self.api.query(query)
                if result.nodes:
                    n = result.nodes[0]
                    name = n.tags.get('name', f"{k}={v}")
                    print(f"      📍 ¡BULLSEYE! Encontrada entidad: {name}")
                    return float(n.lat), float(n.lon), name
                elif result.ways:
                    w = result.ways[0]
                    name = w.tags.get('name', f"{k}={v}")
                    print(f"      📍 ¡BULLSEYE! Encontrado recinto: {name}")
                    return float(w.center_lat), float(w.center_lon), name
            except Exception as e:
                print(f"      [GIS Error] Overpass API en entidad {k}={v}: {e}")
        return None

    def _translate_features_to_osm_tags(self, visual_context):
        """Traduce las deducciones visuales a tags de OpenStreetMap."""
        tags = {}
        features = visual_context.get("features", {})
        sub_type = visual_context.get("sub_type", "")
        
        # Mapeo básico de arquitectura/entorno a OSM (extensible más adelante con clasificadores visuales dedicados)
        if sub_type == "INDUSTRIAL":
            tags["landuse"] = "industrial"
            
        return tags

    def _clean_ocr(self, text):
        """Limpia el texto OCR para hacer una búsqueda más realista."""
        import string
        # Elimina ruido común de OCR
        words = text.split()
        # Filtra palabras muy cortas que suelen ser errores
        valid_words = [w for w in words if len(w) > 3 and any(c.isalpha() for c in w)]
        
        if valid_words:
            # Tomar la palabra más larga o las dos primeras como heurística
            sorted_words = sorted(valid_words, key=len, reverse=True)
            return sorted_words[0]
        return ""
