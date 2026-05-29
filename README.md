# Ghost-Protocol (Protocolo Fantasma)

Sistema automatizado de seguridad perimetral hibrida para estaciones de trabajo host basadas en el sistema operativo Windows. La solucion integra algoritmos de vision computacional para el reconocimiento biometrico y el escaneo de proximidad por radiofrecuencia (Bluetooth Low Energy) mediante un factor de autenticacion de hardware portatil basado en ESP32-C3. Si cualquiera de los dos factores criticos es vulnerado o el operador se aleja del perimetro, el sistema destruye las llaves temporales en la memoria RAM y fuerza el aislamiento instantaneo del sistema operativo.

---

## Arquitectura de Archivos del Proyecto

A continuacion se detalla la funcion tecnica de cada componente modular presente en el repositorio:

### Carpetas del Sistema
* /alertas: Repositorio local automatizado donde el hilo de mitigacion guarda de manera asincrona las capturas fotograficas (.jpg) con marcas de tiempo forenses cuando detecta un rostro intruso o una anomalia perimetral.
* /datos: Almacenamiento seguro de estructuras de datos locales, llaves de sesion y firmas criptograficas simetricas.

### Scripts Principales de Ejecucion
* app_ghost.py: El demonio principal del sistema (Main Daemon). Inicializa los hilos de ejecucion concurrentes, gestiona el bucle de control, orquesta la logica de validacion cruzada y procesa las excepciones para mantener el terminal desbloqueado.
* gui_ghost.py: Interfaz Grafica de Usuario (GUI). Provee el entorno visual para la administracion local del sistema, permitiendo visualizar los logs del demonio, configurar los puertos de comunicacion y arrancar el servicio de forma intuitiva.

### Modulos de Vision Artificial (Inteligencia Artificial)
* captura_rostro.py: Script de enrolamiento inicial. Accede al canal optico local mediante OpenCV (cv2.VideoCapture) para capturar las matrices de imagenes del rostro del operador legitimo y guardarlas en crudo para el posterior entrenamiento.
* entrenador.py: Ejecuta el procesamiento matematico. Toma las muestras de rostros locales y compila el algoritmo de Histogramas de Patrones Binarios Locales (LBPH), exportando el mapa de caracteristicas entrenado.
* modelo_rostro_felipe.xml: Archivo serializado resultante del entrenamiento biometrico. Contiene la firma matematica y las ponderaciones de los patrones binarios del operador legitimo para la toma de decisiones en tiempo real.
* test_ia.py / test_ia_v1.4.py: Entornos de prueba unitarios aislados. Se utilizan para calibrar los umbrales de confianza (confidence threshold) del algoritmo LBPH y medir la resiliencia del clasificador Haar Cascade frente a diferentes condiciones de iluminacion.

### Modulos de Radiofrecuencia (Conectividad BLE)
* detector_ble.py: Script encargado del escaneo asincrono del espacio libre utilizando la interfaz Bleak. Filtra las tramas publicitarias (advertising) para interceptar la direccion MAC univoca del llavero fisico y calcula la perdida de trayectoria para evaluar el nivel de la señal (RSSI).

### Archivos de Hardware y Logs
* test_led_esp32.ino: Firmware en C++ para el microcontrolador embebido ESP32-C3. Configura el chip periferico para actuar como un Beacon emisor continuo de tramas BLE de proximidad y manipula los estados de los pines LED fisicos para indicar visualmente el estado del enlace.
* estado.txt / registro_seguridad.txt: Archivos de almacenamiento volatil y persistente de logs. Registran en texto plano el historico de eventos del sistema, caidas de señal, marcas de tiempo de bloqueos y alertas de acceso administrativo.

---

## Requisitos del Entorno

Para levantar el entorno local de desarrollo y ejecucion de la solucion, la estacion de trabajo debe contar con:

* Sistema Operativo: Windows 10 / Windows 11 (Requisito estricto por uso de API nativas de user32.dll).
* Lenguaje de Programacion: Python 3.11 o superior.
* IDE Recomendado: Visual Studio Code.

---

## Flujo Algoritmico de Control

El ciclo de vida operativo del sistema se rige bajo la siguiente jerarquia de decisiones en tiempo real:

1. Arranque Seguro: app_ghost.py invoca los componentes de gui_ghost.py y levanta las variables en la memoria RAM volatil, cargando el archivo modelo_rostro_felipe.xml.
2. Verificacion Optica: Se procesa el stream de video buscando coincidencia del operador legitimo en el clasificador biometrico. Si no se detecta el rostro o la confianza es inferior al umbral, se genera una captura en /alertas y se bloquea el equipo de forma automatica.
3. Verificacion Radial: En paralelo, detector_ble.py evalua de forma asincrona la proximidad del llavero. Si la señal RSSI decae por debajo de los -85 dBm (distancia perimetral excedida), se suspende la inyeccion de llaves y se ejecuta el aislamiento mediante la funcion LockWorkStation().
