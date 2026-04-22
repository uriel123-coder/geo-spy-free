from flask import Flask, request, jsonify, send_from_directory
import os
import geo_engine
import webbrowser
import threading

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inicializar motor al arrancar
print("[SERVIDOR] Iniciando Motor Global...")
engine = geo_engine.get_engine()
print("[SERVIDOR] Sistema listo.")

@app.route('/')
def index():
    """Servir la interfaz web."""
    return send_from_directory('.', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint para analizar una imagen."""
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Análisis Zero-Shot (busca en todo el mundo)
    results, visual_context = engine.analyze(filepath, top_k=5)
    
    if results:
        return jsonify({
            'status': 'success',
            'location': results[0]['location'],
            'location_es': results[0].get('location_es', ''),
            'lat': results[0]['lat'],
            'lon': results[0]['lon'],
            'confidence': f"{results[0]['confidence']:.1f}%",
            'reasoning': visual_context
        })
    else:
        return jsonify({
            "status": "error",
            "message": "No se pudo analizar la imagen."
        })

@app.route('/status')
def status():
    """Estado del sistema."""
    return jsonify({
        "status": "online",
        "model": "Contundente IA de Visión (Cero Datos Pregrabados)"
    })

def open_browser():
    """Abre el navegador automáticamente."""
    webbrowser.open('http://localhost:8080')

if __name__ == '__main__':
    # Abrir navegador después de 1 segundo
    threading.Timer(1.5, open_browser).start()
    print("\n" + "="*50)
    print("🌍 SISTEMA GEO-FINDER INICIADO")
    print("="*50)
    print("📍 Abre tu navegador en: http://localhost:8080")
    print("🔍 Arrastra una foto para encontrar su ubicación")
    print("="*50 + "\n")
    app.run(port=8080, debug=False)

