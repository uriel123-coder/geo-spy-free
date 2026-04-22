#!/usr/bin/env python3
"""
Script de prueba para GeoCLIP
"""
import sys

print("[TEST] Iniciando pruebas de GeoCLIP...")

# Test 1: Import
try:
    from geoclip import GeoCLIP
    print("[✓] GeoCLIP importado correctamente")
except ImportError as e:
    print(f"[✗] ERROR: No se pudo importar GeoCLIP: {e}")
    sys.exit(1)

# Test 2: Inicialización
try:
    print("[TEST] Inicializando modelo...")
    model = GeoCLIP()
    print("[✓] Modelo inicializado")
except Exception as e:
    print(f"[✗] ERROR al inicializar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Prueba con imagen de ejemplo
try:
    from PIL import Image
    import numpy as np
    
    # Crear imagen de prueba (100x100 aleatoria)
    print("[TEST] Creando imagen de prueba...")
    test_img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    test_img.save("/tmp/test_geoclip.png")
    
    print("[TEST] Ejecutando predicción...")
    top_pred_gps, top_pred_prob = model.predict("/tmp/test_geoclip.png", top_k=3)
    
    print("[✓] Predicción exitosa!")
    print(f"    GPS: {top_pred_gps[0]}")
    print(f"    Probabilidad: {top_pred_prob[0]:.4f}")
    
except Exception as e:
    print(f"[✗] ERROR en predicción: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[✓✓✓] Todas las pruebas pasaron!")
print("GeoCLIP está funcionando correctamente.")
