import cv2
import os
import time
from datetime import datetime
import numpy as np

# ==========================================================
# GHOST-PROTOCOL - NÚCLEO DE RECONOCIMIENTO (MASTER)
# ==========================================================

# 1. RUTAS Y RECURSOS
data_path = 'C:/Proyectos FMS digitalprogramacion/Ghost_Protocol/data'
alert_path = 'C:/Proyectos FMS digitalprogramacion/Ghost_Protocol/alertas'
image_paths = os.listdir(data_path)

# 2. CARGA DE MODELOS BIOMÉTRICOS
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modelo_rostro_felipe.xml') 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 3. CONFIGURACIÓN DE SENSIBILIDAD
cap = cv2.VideoCapture(0)
historial_confianza = []
# UMBRAL DE SEGURIDAD (60 = Estricto / 80 = Permisivo)
umbral_tolerancia = 60 

print(">>> GHOST-PROTOCOL MASTER: SISTEMA DE VIGILANCIA ONLINE")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        
        id_predicho, confianza = face_recognizer.predict(rostro)
        
        # Filtro de Media Móvil (Estabilización de imagen)
        historial_confianza.append(confianza)
        if len(historial_confianza) > 20: historial_confianza.pop(0)
        promedio_confianza = sum(historial_confianza) / len(historial_confianza)

        # Lógica de Validación
        if promedio_confianza < umbral_tolerancia:
            nombre = image_paths[id_predicho]
            color = (0, 255, 0) # Verde
            mensaje = f"AUTORIZADO: {nombre}"
        else:
            color = (0, 0, 255) # Rojo
            mensaje = "ACCESO DENEGADO"

        # Dibujado en pantalla
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, mensaje, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow('GHOST-PROTOCOL - MASTER CORE', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()