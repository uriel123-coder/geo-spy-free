# 📜 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/) y este proyecto sigue [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planeado
- Soporte para análisis en batch (múltiples imágenes)
- Dashboard de estadísticas
- Integración con Google Maps
- Modelo fino personalizado
- Aplicación móvil
- Caché distribuido

---

## [1.1.0] - 2026-04-22 (Mejoras de Inteligencia)

### Added - 🆕 Características de IA Mejorada
- ✨ **Sistema de Inteligencia Aumentada** - Puntuación de confianza multi-factor
- 🗺️ **Detección de Street View** - Prioriza lugares con cobertura de Google Street View
- 📍 **Base de datos geo-inteligente** - 50+ lugares turísticos de alta confiabilidad
- 🎯 **Validación de tierra vs océano** - Evita predicciones al azar en océanos
- 🏢 **Clasificación de lugares** - Urbano, turístico, comercial, playas
- 🔍 **Scoring contextual** - Multa por confianza si no es tierra sólida

### Improved
- 🚀 Mejor rendimiento de predicciones en lugares conocidos
- 📊 Puntuación de confianza más realista (basada en múltiples factores)
- 🎨 Puerto consistente (5000) en toda la aplicación
- 🔧 Métodos de cálculo de distancia Haversine (más precisión)

### Technical
- Nuevos métodos: `_load_street_view_places()`, `_has_street_view_coverage()`, `_score_location_intelligence()`
- Integración de análisis multi-factor de confianza
- Mejor manejo de ubicaciones inválidas

### Added
- ✨ Sistema completo de geolocalización con GeoCLIP
- 🌐 Interfaz web interactiva con Leaflet Maps
- 📍 Geocodificación inversa en tiempo real
- 🔌 API REST para integración
- 📊 Soporte GPU/CPU automático
- 🧠 Caché inteligente de predicciones
- 🛡️ Validación de GIS
- 🎨 Interfaz HTML5 responsiva

### Features Principais
- Análisis de imágenes Zero-Shot
- Precisión comparable a sistemas profesionales
- Funcionamiento offline después de descargar modelos
- Múltiples formatos de imagen soportados
- Mapa interactivo con zoom

### Technical
- Flask backend
- PyTorch + Transformers
- GeoCLIP pre-entrenado
- OpenStreetMap (Nominatim)
- FAISS para búsqueda vectorial

---

## Planeado para Futuras Versiones

### v1.1.0
- [ ] Batch processing
- [ ] Historial de predicciones
- [ ] Exportar resultados a CSV/JSON
- [ ] Interfaz oscura

### v1.2.0
- [ ] Integración Google Maps API
- [ ] Visualización avanzada de confianza
- [ ] WebSockets para real-time
- [ ] Multi-idioma

### v2.0.0
- [ ] Modelo personalizado fine-tuning
- [ ] Base de datos persistente
- [ ] Aplicación mobile
- [ ] Autenticación y manejo de usuarios

---

## Notas de Migración

### Ninguna

Este es el lanzamiento inicial del proyecto. No hay versiones anteriores.

---

## Créditos

**Desarrollado por:** Tu Nombre  
**Basado en:** GeoCLIP (FAIR), OpenStreetMap  
**Año:** 2026

---

## Reportar Cambios

Para reportar cambios o sugerencias, abre un [GitHub Issue](https://github.com/tu-usuario/geofinder/issues)
