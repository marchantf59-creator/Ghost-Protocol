import cv2
import os

# Carpeta donde guardaremos tus fotos
nombre_usuario = "Felipe"
carpeta_datos = f'data/{nombre_usuario}'

if not os.path.exists(carpeta_datos):
    os.makedirs(carpeta_datos)
    print(f"Carpeta creada para: {nombre_usuario}")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

count = 0
print("Ponte frente a la cámara. Presiona 's' para capturar una foto (necesitamos 30).")

while count < 30:
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Si presionas 's', guardamos el recorte de la cara
        if cv2.waitKey(1) & 0xFF == ord('s'):
            rostro = gray[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(f'{carpeta_datos}/rostro_{count}.jpg', rostro)
            count += 1
            print(f"Foto {count}/30 capturada.")

    cv2.imshow('Entrenamiento de Identidad', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
print("¡Listo! Ya tenemos tu base de datos facial.")