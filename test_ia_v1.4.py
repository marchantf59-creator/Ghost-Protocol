import cv2
import os
import time
import ctypes
import numpy as np
from datetime import datetime

alert_path = 'alertas'
if not os.path.exists(alert_path): 
    os.makedirs(alert_path)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modelo_rostro_felipe.xml')  
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
historial_confianza = []

# =========================================================================
# ⚙️ CONFIGURACIÓN CALIBRADA (GHOST-PROTOCOL)
umbral_tolerancia = 98     # Subido a 98 para dar colchón óptimo en baja luz (~81.90)
RSSI_THRESHOLD = -85       # Margen ideal para el llavero ESP32
MODO_CONSOLA = False        # TRUE: Modo pruebas (NO bloquea Windows). FALSE: Bloqueo Real Activo.
# =========================================================================

conteo_intruso = 0 
frames_de_gracia = 30 
bloqueo_ejecutado = False
BLE_STATUS_FILE = "status_ble.txt"

def leer_factor_ble():
    if not os.path.exists(BLE_STATUS_FILE):
        return "AUSENTE", -100
    try:
        with open(BLE_STATUS_FILE, "r") as f:
            datos = f.read().strip().split("|")
            if len(datos) == 2:
                return datos[0], int(datos[1])
    except Exception:
        pass
    return "AUSENTE", -100

print(">>> [GHOST-PROTOCOL] INITIALIZING INTEGRATED AI CORE TEST V1.4...")
if MODO_CONSOLA:
    print("[MODO] *** ENTORNO DE PRUEBAS ACTIVO: El bloqueo real de Windows está DESACTIVADO ***")
else:
    print("[MODO] *** MODO DE SEGURIDAD MÁXIMA: Bloqueo por user32.dll ACTIVADO ***")

print("[KERNEL] Estabilizando sensor óptico (Espere 2 segundos)...")
for i in range(15):
    cap.read()
    time.sleep(0.1)

print("[KERNEL] Sensor óptico LISTO. Monitoreo perimetral activo...")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    # 1. Telemetría del factor físico BLE
    estado_ble, rssi_ble = leer_factor_ble()
    ble_comprometido = (estado_ble == "AUSENTE" or rssi_ble < RSSI_THRESHOLD)
    
    # 2. Procesamiento Óptico (IA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    ia_comprometida = False
    estado_actual = "SEGURO"
    mensaje_ia, color_ia = "ACCESO OK", (0, 255, 0)

    if len(faces) == 0:
        ia_comprometida = True
    else:
        for (x, y, w, h) in faces:
            rostro = gray[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            id_predicho, confianza = face_recognizer.predict(rostro)
            
            historial_confianza.append(confianza)
            if len(historial_confianza) > 15: 
                historial_confianza.pop(0)
            
            promedio_confianza = sum(historial_confianza) / len(historial_confianza)
            
            # Evaluación con el nuevo umbral calibrado de noche
            if promedio_confianza >= umbral_tolerancia:
                ia_comprometida = True
                mensaje_ia = f"INTRUSO ({int(promedio_confianza)})"
                color_ia = (0, 0, 255)
            else:
                mensaje_ia = f"FELIPE OK ({int(promedio_confianza)})"
                color_ia = (0, 255, 0)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color_ia, 2)
            cv2.putText(frame, mensaje_ia, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_ia, 2)

    # 3. Lógica de Fusión Lineal 
    if ia_comprometida or ble_comprometido:
        estado_actual = "ALERTA"
        conteo_intruso += 1
    else:
        conteo_intruso = max(0, conteo_intruso - 2)

    # 4. Gatillo de Mitigación y Registro de Evidencias
    if conteo_intruso > frames_de_gracia and not bloqueo_ejecutado:
        hora_alerta = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_foto = f"{alert_path}/INTRUSO_{hora_alerta}.jpg"
        cv2.imwrite(nombre_foto, frame)
        print(f"[CRÍTICO] COMBINACIÓN DETECTADA (IA/BLE). EVIDENCIA LOCAL: {nombre_foto}")
        
        with open("status.txt", "w") as f: 
            f.write(f"ALERTA|{nombre_foto}")
        
        if not MODO_CONSOLA:
            print("[KERNEL] Invocando Bloqueo Real mediante user32.dll...")
            ctypes.windll.user32.LockWorkStation()
        else:
            print("[SIMULACIÓN] Alerta crítica gatillada. (Bloqueo omitido por MODO_CONSOLA)")
        
        bloqueo_ejecutado = True 
        conteo_intruso = 0 

    if not bloqueo_ejecutado:
        with open("status.txt", "w") as f: 
            f.write(estado_actual)
            
    # 5. HUD Gráfico para la Defensa del Proyecto
    cv2.rectangle(frame, (0,0), (640, 45), (0,0,0), -1) 
    if conteo_intruso > 0: 
        cv2.rectangle(frame, (10, 36), (10 + min(conteo_intruso * 6, 620), 42), (0, 0, 255), -1)
    
    modo_str = "TEST" if MODO_CONSOLA else "PROD"
    info_hud = f"GHOST [{modo_str}]: {estado_actual} | BLE: {estado_ble} ({rssi_ble}dBm) | UMBRAL: {umbral_tolerancia}"
    color_hud = (0, 0, 255) if estado_actual == "ALERTA" else (255, 255, 255)
    cv2.putText(frame, info_hud, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color_hud, 1)

    cv2.imshow('GHOST-PROTOCOL IA', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()