import os
import subprocess
import sys
import ssl
import urllib.request

# Fix SSL
ssl._create_default_https_context = ssl._create_unverified_context

def install_deps():
    print("[SETUP] Instalando librerías profesionales (PyTorch, Transformers, FAISS)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_images():
    print("[SETUP] Descargando dataset de prueba...")
    os.makedirs("demo_images", exist_ok=True)
    
    data = [
        ("paris.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/800px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg", "París, Torre Eiffel"),
        ("liberty.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Statue_of_Liberty_7.jpg/800px-Statue_of_Liberty_7.jpg", "Nueva York, Estatua de la Libertad"),
        ("colosseum.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Colosseo_2020.jpg/800px-Colosseo_2020.jpg", "Roma, Coliseo"),
        ("taj.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Taj_Mahal_%28Edited%29.jpeg/800px-Taj_Mahal_%28Edited%29.jpeg", "India, Taj Mahal")
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for fn, url, loc in data:
        path = os.path.join("demo_images", fn)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as r, open(path, 'wb') as f:
                f.write(r.read())
            print(f"   -> Descargado: {loc}")
        except Exception as e:
            print(f"   [ERROR] {loc}: {e}")
    return data

def build_index(data):
    print("[SETUP] Inicializando Motor IA (CLIP + FAISS)...")
    # Importar aquí para asegurar que deps están instaladas
    import geo_engine
    engine = geo_engine.get_engine()
    
    print("[SETUP] Entrenando con imágenes descargadas...")
    for fn, _, loc in data:
        path = os.path.join("demo_images", fn)
        if os.path.exists(path):
            engine.add_to_index(path, loc)
            print(f"   -> Indexado: {loc}")
            
    print("[SETUP] ¡Sistema Listo!")

if __name__ == "__main__":
    print("="*50)
    print("   INSTALADOR SISTEMA GEO-PRO")
    print("="*50)
    
    # 1. Instalar
    try:
        import torch
        import faiss
        print("[SETUP] Dependencias ya instaladas.")
    except ImportError:
        install_deps()
        
    # 2. Descargar
    data = download_images()
    
    # 3. Indexar
    build_index(data)
