import cv2
import os
import numpy as np

# Ruta de las fotos
data_path = 'C:/Proyectos FMS digitalprogramacion/Ghost_Protocol/data'
lista_personas = os.listdir(data_path)
print('Lista de personas: ', lista_personas)

labels = []
faces_data = []
label = 0

for name_dir in lista_personas:
    person_path = data_path + '/' + name_dir
    print('Leyendo las imágenes de: ' + name_dir)

    for file_name in os.listdir(person_path):
        labels.append(label)
        faces_data.append(cv2.imread(person_path + '/' + file_name, 0))
    label += 1

# Creamos el modelo de entrenamiento
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenando...
print("Entrenando... un momento por favor.")
face_recognizer.train(faces_data, np.array(labels))

# Guardamos el modelo para usarlo en el Ghost-Protocol
face_recognizer.write('modelo_rostro_felipe.xml')
print("¡Modelo almacenado con éxito! (modelo_rostro_felipe.xml)")