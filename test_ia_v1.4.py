import cv2
import os
import time
import ctypes
import numpy as np
import winsound
from datetime import datetime

# 1. CONFIGURACIÓN DE RUTAS
# Creamos la carpeta de alertas si no existe para guardar las fotos
alert_path = 'alertas'
if not os.path.exists(alert_path): 
    os.makedirs(alert_path)

# 2. CARGA DE MODELOS
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modelo_rostro_felipe.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 3. VARIABLES DE CONTROL
cap = cv2.VideoCapture(0)
historial_confianza = []
umbral_tolerancia = 60  
seguridad_maxima = True

# Variables para el margen de seguridad y captura
conteo_intruso = 0 
frames_de_gracia = 30 # Aprox 3 segundos para que te reconozca
bloqueo_ejecutado = False 

print(">>> GHOST-PROTOCOL IA: MODO FORENSE ACTIVADO")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Estado inicial: si no hay nadie, es alerta preventiva
    estado_actual = "ALERTA" if len(faces) == 0 else "SEGURO"
    if len(faces) == 0:
        conteo_intruso += 1

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        id_predicho, confianza = face_recognizer.predict(rostro)
        
        historial_confianza.append(confianza)
        if len(historial_confianza) > 20: historial_confianza.pop(0)
        promedio_confianza = sum(historial_confianza) / len(historial_confianza)

        if promedio_confianza < umbral_tolerancia:
            estado_actual = "SEGURO"
            mensaje, color = "ACCESO OK", (0, 255, 0)
            conteo_intruso = 0 # Reinicia si eres tú
            bloqueo_ejecutado = False 
        else:
            estado_actual = "ALERTA"
            mensaje, color = "INTRUSO", (0, 0, 255)
            conteo_intruso += 1 # Suma si no te reconoce (con o sin gorro)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, mensaje, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 4. LÓGICA DE ALERTA, CAPTURA Y BLOQUEO
    if seguridad_maxima and conteo_intruso > 0 and not bloqueo_ejecutado:
        # Pitido de advertencia: sube de frecuencia mientras la barra crece
        frecuencia = 400 + (conteo_intruso * 20)
        winsound.Beep(frecuencia, 100) 

        if conteo_intruso > frames_de_gracia:
            # A. CAPTURAR EVIDENCIA ANTES DE BLOQUEAR
            hora_alerta = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_foto = f"{alert_path}/INTRUSO_{hora_alerta}.jpg"
            cv2.imwrite(nombre_foto, frame)
            print(f"!!! EVIDENCIA GUARDADA: {nombre_foto}")

            # B. AVISAR A LA APP (mandamos el estado y la ruta de la foto)
            with open("status.txt", "w") as f: 
                f.write(f"ALERTA|{nombre_foto}")
            
            # C. BLOQUEO FINAL
            winsound.Beep(1000, 500) 
            bloqueo_ejecutado = True 
            conteo_intruso = 0 
            ctypes.windll.user32.LockWorkStation()

    # GUARDAR ESTADO PARA LA APP SI NO HEMOS BLOQUEADO
    if not bloqueo_ejecutado:
        with open("status.txt", "w") as f: f.write(estado_actual)

    # INTERFAZ VISUAL
    cv2.rectangle(frame, (0,0), (640, 40), (0,0,0), -1) 
    if conteo_intruso > 0: # Barra roja de "Carga de Bloqueo"
        cv2.rectangle(frame, (10, 32), (10 + (conteo_intruso * 6), 38), (0, 0, 255), -1)
    
    cv2.putText(frame, f"GHOST-STATUS: {estado_actual}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.imshow('GHOST-PROTOCOL IA', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()