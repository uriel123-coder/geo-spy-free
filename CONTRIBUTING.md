# 🤝 Guía de Contribución

¡Gracias por considerar contribuir a GeoFinder! Tu ayuda es invaluable para mejorar este proyecto.

## 📋 Formas de Contribuir

### 1. 🐛 Reportar Bugs
- Abre un [GitHub Issue](https://github.com/tu-usuario/geofinder/issues)
- Describe el problema con claridad
- Incluye pasos para reproducir
- Adjunta screenshots si es posible

**Formato:**
```
Título: [BUG] Descripción breve
Descripción del bug
Pasos a reproducir
Comportamiento esperado vs actual
```

### 2. ✨ Sugerir Mejoras
- Abre un [GitHub Discussion](https://github.com/tu-usuario/geofinder/discussions)
- Explica el caso de uso
- Describe la solución propuesta

### 3. 🔧 Pull Requests (Código)

#### Paso a paso:

**1. Fork el repositorio**
```bash
# En GitHub, click en "Fork"
```

**2. Clonar tu fork**
```bash
git clone https://github.com/tu-usuario/geofinder.git
cd geofinder
```

**3. Crear rama para tu feature**
```bash
git checkout -b feature/tu-feature-name
# o para bugs:
git checkout -b fix/descripcion-bug
```

**4. Hacer cambios**
- Modifica los archivos necesarios
- Mantén el código limpio y documentado
- Sigue PEP 8 para Python

**5. Commit con mensajes descriptivos**
```bash
git add .
git commit -m "feat: descripción clara del cambio"
```

Tipos de commit:
- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Documentación
- `style:` Formato, espacios, etc
- `refactor:` Restructuración sin cambios funcionales
- `test:` Nuevos tests
- `perf:` Mejoras de rendimiento

**6. Push a tu rama**
```bash
git push origin feature/tu-feature-name
```

**7. Abrir Pull Request**
- En GitHub, ve a "Pull Requests"
- Click en "New Pull Request"
- Selecciona tu rama
- Completa el formulario
- Describe los cambios claramente

**8. Responder Reviews**
- Los mantenedores revisarán tu código
- Realiza cambios si se solicitan
- Discute en los comentarios si hay dudas

---

## 📐 Estándares de Código

### Python (PEP 8)

✅ **Bueno:**
```python
def analyze_image(filepath: str, top_k: int = 5) -> dict:
    """Analiza una imagen y retorna predicciones de ubicación.
    
    Args:
        filepath: Ruta a la imagen
        top_k: Número de top predicciones
        
    Returns:
        dict con resultados y confianza
    """
    results = engine.predict(filepath)
    return results[:top_k]
```

❌ **Malo:**
```python
def analyze_image(filepath, top_k):
    results = engine.predict(filepath)
    return results[:top_k]
```

### Reglas:
- 4 espacios de indentación
- Máximo 88 caracteres por línea
- Docstrings en todas las funciones públicas
- Type hints recomendados
- Variables con nombres descriptivos

### JavaScript/HTML:
- 2 espacios de indentación
- Usa const/let, no var
- Comentarios en inglés o español, consistentemente

---

## 🧪 Testing

Antes de abrir un PR, ejecuta tests:

```bash
python test_geoclip.py
python test_gemini.py
```

Para agregar nuevos tests:
```bash
# Crea test_mi_feature.py
python -m pytest test_mi_feature.py
```

---

## 📝 Documentación

Si modificas funcionalidad, actualiza:
- README.md (si aplica)
- Docstrings de funciones
- Comentarios en código complejo
- FAQ (si es uso común)

---

## 🚀 Proceso de Release

(Administradores solamente)

```bash
# 1. Actualizar versión
# 2. Actualizar CHANGELOG
# 3. Crear tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
# 4. GitHub Actions publica automáticamente
```

---

## 💡 Ideas Bienvenidas

- Optimizaciones de rendimiento
- Mejoras en precisión del modelo
- Nuevas características (batch processing, etc)
- Mejor UI/UX
- Documentación en otros idiomas
- Integración con servicios nuevos


---

## 📜 Código de Conducta

Se espera que todos sean respetuosos y profesionales:
- ✅ Sé cortés y constructivo
- ✅ Acepta crítica con madurez
- ✅ Ayuda a otros contributors
- ❌ Sin spam, acoso, o discriminación

---

**¡Gracias por contribuir a GeoFinder!** 🎉
