# 🌍 GeoFinder

## Descubre DÓNDE fue tomada cualquier foto 📸

**La aplicación más fácil y rápida para saber exactamente dónde está una foto**

Simplemente sube una foto y GeoFinder te dice:
- 📍 Las coordenadas GPS exactas
- 🗺️ El nombre del lugar
- 📊 Qué tan seguro está (%)

---

## ¿Cómo funciona?

1. ⬆️ **Sube una foto** (arrastra o haz click)
2. ⏳ **Espera 5-15 segundos** mientras la IA analiza
3. 🎯 **Obtén la ubicación** exacta en un mapa
4. 🔄 **Repite** cuantas veces quieras

¡Es así de simple!

---

## ✨ Lo que puedes hacer

✅ Fotos de viajes, monumentos, playas  
✅ Fotos de amigos en lugares desconocidos  
✅ Fotos antiguas para recordar dónde fueron tomadas  
✅ Cualquier foto de cualquier parte del mundo  

**Nota:** Funciona mejor con fotos nítidas que tengan elementos característicos (edificios, montañas, calles especiales)

---

## 🚀 EMPEZAR AHORA (3 minutos)

### Requisitos
Solo necesitas una computadora con:
- **Windows, macOS o Linux**
- **Conexión a internet** (primera vez solamente)
- **Espacio libre**: ~2GB

Eso es todo.

### Instalación Rápida

**1. Descargar Python (si no lo tienes)**
- Ve a [python.org](https://www.python.org/) 
- Descarga Python 3.8 o superior
- Instala (marca "Add Python to PATH")

**2. Descargar GeoFinder**
```bash
git clone https://github.com/tu-usuario/geofinder.git
cd geofinder
```

O descarga como ZIP desde GitHub y extrae la carpeta.

**3. Instalar (copia y pega en terminal/cmd)**

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

💡 Esto puede tardar 5-10 minutos la primera vez.

**4. ¡Ejecutar!**
```bash
python app.py
```

Se abrirá automáticamente en tu navegador. Si no → ve a `http://localhost:5000`

✅ **¡Listo!** Ya puedes empezar a subir fotos

---

## � Cómo Usar

### Interfaz Web (Lo más fácil)

1. Si GeoFinder sigue corriendo, ya está en `http://localhost:5000`
2. **Arrastra una foto** al área gris o haz click para seleccionar
3. Espera a que termine (muestra progreso)
4. 🎉 **¡Resultado listo!**
   - Ves la ubicación exacta
   - El mapa con un pin rojo
   - Qué tan confiado está el sistema
   - Detalles de la ubicación

### Ese es el flujo completo. ¡Todo listo!

---

## ❓ Preguntas Comunes

**P: ¿Qué tipo de fotos funcionan mejor?**  
R: Fotos claras de lugares específicos (edificios, calles, monumentos). Funciona peor con paisajes genéricos (árboles solos, cielo nublado).

**P: ¿Funciona con cualquier lugar del mundo?**  
R: Sí. El sistema fue entrenado con millones de fotos de todo el planeta.

**P: ¿Se suben mis fotos a internet?**  
R: No. Todo se procesa en tu máquina. Las fotos se guardan temporalmente solo mientras las analizas.

**P: ¿Por qué a veces no funciona bien?**  
R: Si la foto es muy borrosa, de lugar muy genérico, o fue tomada en un sitio que pocas fotos tienen, la precisión baja.

**P: ¿Puedo usar imágenes antiguas de Google, etc?**  
R: Sí, pero si son muy diferentes a fotos actuales del lugar, la precisión puede bajar.

**P: ¿Necesito internet siempre?**  
R: Necesitas internet la primera vez para descargar los modelos. Después, puedes usar sin internet.

---

## �️ Si Algo No Funciona

**Error: "Python no encontrado" o "command not found"**
- Reinstala Python desde [python.org](https://www.python.org/)
- Durante instalación, marca "Add Python to PATH"

**Error: "ModuleNotFoundError: No module named 'geoclip'"**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**La aplicación es muy lenta o se congela**
- Primera ejecución: descarga 1GB de modelos (puede tardar 30 min)
- Necesitas buena conexión a internet

**Error: "Port 5000 already in use"**
Otra aplicación está usando el puerto. Usa otro:
```bash
# Edit: Abre app.py, busca "app.run(port=5000)" y cambia a 5001
```

**¿Otros problemas?**
- Abre un ticket en GitHub [Issues](https://github.com/tu-usuario/geofinder/issues)

---

## 📝 Notas Importantes

🔒 **Privacidad:** Tus fotos NO se envían a internet. Todo se procesa localmente.

💾 **Espacio:** Necesita ~2GB libres para descargar modelos IA.

⚡ **GPU vs CPU:** Si tienes tarjeta gráfica, GeoFinder es más rápido. Si no, usa CPU (más lento pero funciona).

🌐 **Internet:** Solo necesitas en la primera ejecución para descargar modelos.

---

## 🎓 ¿Eres Desarrollador?

Para contribuir al código, ver [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 Licencia

Este proyecto es **gratis y de código abierto** (Licencia MIT). Ver [LICENSE](LICENSE)

