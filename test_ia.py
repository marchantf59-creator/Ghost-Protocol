import cv2
import os
import time
from datetime import datetime
import numpy as np

# ==========================================================
# GHOST-PROTOCOL v1.3 - VERSIÓN FINAL DE DEFENSA
# Arquitectura: Multicapa con Filtro de Media Móvil
# ==========================================================

# 1. CONFIGURACIÓN DE RUTAS Y RECURSOS
data_path = 'C:/Proyectos FMS digitalprogramacion/Ghost_Protocol/data'
alert_path = 'C:/Proyectos FMS digitalprogramacion/Ghost_Protocol/alertas'
image_paths = os.listdir(data_path)

# 2. CARGA DE MODELOS BIOMÉTRICOS
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modelo_rostro_felipe.xml') 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 3. VARIABLES DE CONTROL DE ESTABILIDAD
cap = cv2.VideoCapture(0)
ultimo_registro = 0 
historial_confianza = [] # Búfer para promediar lecturas y evitar parpadeo
umbral_tolerancia = 88   # Ajustado para compensar ruido lumínico ambiental

print(">>> GHOST-PROTOCOL: VIGILANCIA REFORZADA ACTIVA...")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    # Pre-procesamiento: Escala de grises para optimizar recursos
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aux_frame = gray.copy()
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # ESTADO: ESCANEO (Sin presencia de sujetos)
    if len(faces) == 0:
        historial_confianza.clear() # Limpiar búfer al perder rastro facial
        cv2.putText(frame, 'SISTEMA DE VIGILANCIA: ESCANEANDO...', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    for (x, y, w, h) in faces:
        # Normalización del recorte facial (150x150 px)
        rostro = aux_frame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        
        # PREDICCIÓN MEDIANTE ALGORITMO LBPH
        id_predicho, confianza = face_recognizer.predict(rostro)
        
        # IMPLEMENTACIÓN DE FILTRO DE MEDIA MÓVIL (Ventana de 20 muestras)
        historial_confianza.append(confianza)
        if len(historial_confianza) > 20: 
            historial_confianza.pop(0)
        
        promedio_confianza = sum(historial_confianza) / len(historial_confianza)

        # LÓGICA DE DECISIÓN SEGÚN UMBRAL CALIBRADO
        if promedio_confianza < umbral_tolerancia:
            nombre = image_paths[id_predicho]
            color = (0, 255, 0) # Verde (Acceso)
            mensaje = f'ACCESO CONCEDIDO: {nombre}'
        else:
            color = (0, 0, 255) # Rojo (Alerta)
            mensaje = 'DESCONOCIDO - BLOQUEO'
            
            # Persistencia de Evidencia (Cada 5 segundos)
            tiempo_actual = time.time()
            if tiempo_actual - ultimo_registro > 5:
                ahora = datetime.now().strftime("%H-%M-%S")
                cv2.imwrite(f"{alert_path}/INTRUSO_{ahora}.jpg", frame)
                ultimo_registro = tiempo_actual
                
                # Registro en Log de Auditoría
                with open("log_seguridad.txt", "a") as archivo_log:
                    fecha_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    archivo_log.write(f"[{fecha_log}] ALERTA: Intruso detectado. Promedio Conf: {promedio_confianza:.2f}\n")
                
                print(f"[!] PROTOCOLO DE BLOQUEO: Registro guardado en INTRUSO_{ahora}.jpg")

        # RENDERIZADO DE INTERFAZ TÉCNICA
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, f"{mensaje} ({int(promedio_confianza)})", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow('GHOST-PROTOCOL v1.3 - CFMC SECURITY', frame)
    
    # Salida segura del sistema
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        print(">>> APAGANDO SISTEMA... BUENAS NOCHES.")
        break

cap.release()
cv2.destroyAllWindows()