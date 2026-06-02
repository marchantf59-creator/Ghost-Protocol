# Ghost-Protocol (Protocolo Fantasma) v1.4

Sistema automatizado de seguridad perimetral híbrida para estaciones de trabajo host basadas en el sistema operativo Windows. La solución integra algoritmos de visión computacional para el reconocimiento biométrico y el escaneo de proximidad por radiofrecuencia (Bluetooth Low Energy) mediante un factor de autenticación de hardware portátil basado en ESP32-C3. Si cualquiera de los dos factores críticos es vulnerado o el operador se aleja del perímetro, el sistema destruye las llaves temporales en la memoria RAM y fuerza el aislamiento instantáneo del sistema operativo.

---

## 🚀 Características Avanzadas (v1.4)

* **Autenticación Multifactor Continua (2FA):** Fusión lineal de dos canales independientes:
    * **Factor Óptico:** Reconocimiento facial local mediante algoritmos LBPH (Local Binary Patterns Histograms) optimizados con OpenCV.
    * **Factor Físico:** Monitoreo perimetral asíncrono pasivo por RSSI mediante un hardware llavero (ESP32-C3).
* **Umbral Adaptativo Calibrado:** Tolerancia ajustada a `98` para mitigar variaciones extremas de luz en entornos nocturnos, reduciendo a cero los falsos positivos por sombras.
* **Aislamiento por Hardware y Software:** Comunicación desacoplada en disco mediante el estado dinámico de `status_ble.txt` para garantizar la ejecución concurrente sin colisiones en hilos de Windows.
* **Control de Mitigación Real:** Invocación directa a bajo nivel de la API de Windows (`user32.dll`) con un búfer de estabilización óptica inicial de 15 frames para evitar bloqueos espurios al arranque.

---

## ## Arquitectura de Archivos del Proyecto

A continuación se detalla la función técnica de cada componente modular presente en el repositorio:

### Carpetas del Sistema
* `/alertas`: Repositorio local automatizado donde el hilo de mitigación guarda de manera asíncrona las capturas fotográficas (`.jpg`) con marcas de tiempo forenses cuando detecta un rostro intruso o una anomalía perimetral.
* `/datos`: Almacenamiento seguro de estructuras de datos locales, llaves de sesión y firmas criptográficas simétricas.

### Scripts Principales de Ejecución
* `app_ghost.py`: El demonio principal del sistema (Main Daemon). Inicializa los hilos de ejecución concurrentes, gestiona el bucle de control, orquesta la lógica de validación cruzada y procesa las excepciones para mantener el terminal desbloqueado.
* `gui_ghost.py`: Interfaz Gráfica de Usuario (GUI). Provee el entorno visual para la administración local del sistema, permitiendo visualizar los logs del demonio, configurar los puertos de comunicación y arrancar el servicio de forma intuitiva.

### Módulos de Visión Artificial (Inteligencia Artificial)
* `captura_rostro.py`: Script de enrolamiento inicial. Accede al canal óptico local mediante OpenCV (`cv2.VideoCapture`) para capturar las matrices de imágenes del rostro del operador legítimo y guardarlas en crudo para el posterior entrenamiento.
* `entrenador.py`: Ejecuta el procesamiento matemático. Toma las muestras de rostros locales y compila el algoritmo de Histogramas de Patrones Binarios Locales (LBPH), exportando el mapa de características entrenado.
* `modelo_rostro_felipe.xml`: Archivo serializado resultante del entrenamiento biométrico. Contiene la firma matemática y las ponderaciones de los patrones binarios del operador legítimo para la toma de decisiones en tiempo real.
* `test_ia.py` / `test_ia_v1.4.py`: Núcleo de Visión Computacional integrado en producción. Implementa la lógica de filtrado histórico de promedios de confianza, lectura perimetral del factor BLE, HUD militarizado y el disparador crítico de bloqueo mediante el Kernel de Windows (`LockWorkStation`).

### Módulos de Radiofrecuencia y Contingencia Criptográfica
* `detector_ble.py`: Script encargado del escaneo asíncrono y pasivo del espacio libre utilizando la interfaz Bleak. Implementa callbacks de captura continua para interceptar el paquete de *advertising* de la dirección MAC unívoca del llavero físico, calculando de manera fluida el RSSI sin saturar el stack de red.
* `recovery_handler.py`: Módulo CLI criptográfico de contingencia. Actúa como consola de rescate y bypass administrativo seguro en caso de pérdida o avería del token físico de hardware, validando credenciales mediante derivación de claves con funciones seguras PBKDF2.

### Archivos de Hardware y Logs
* `test_led_esp32.ino`: Firmware en C++ para el microcontrolador embebido ESP32-C3. Configura el chip periférico para actuar como un Beacon emisor continuo de tramas BLE de proximidad y manipula los estados de los pines LED físicos para indicar visualmente el estado del enlace.
* `estado.txt` / `status.txt` / `status_ble.txt`: Búferes dinámicos de intercambio de estados en disco y logs de comunicación inter-procesos.
* `registro_seguridad.txt` / `log_seguridad.txt`: Archivos de almacenamiento persistente que registran en texto plano el histórico de eventos del sistema, caídas de señal, marcas de tiempo de bloqueos y alertas de acceso administrativo.

---

## Requisitos del Entorno

Para levantar el entorno local de desarrollo y ejecución de la solución, la estación de trabajo debe contar con:

* **Sistema Operativo:** Windows 10 / Windows 11 (Requisito estricto por uso de API nativas de `user32.dll`).
* **Lenguaje de Programación:** Python 3.11 o superior.
* **Bibliotecas Core:** `opencv-python`, `opencv-contrib-python`, `numpy`, `bleak`.
* **IDE Recomendado:** Visual Studio Code.

---

## 💻 Manual de Ejecución Operativa

El despliegue perimetral seguro de Ghost-Protocol requiere la inicialización concurrente de sus dos capas de control en terminales independientes dentro de la raíz del proyecto:

1. **Despliegue del Factor Físico (RF/BLE):** Inicializar el demonio de escucha asíncrona del hardware portátil en la **Terminal 1**:
   ```bash
   python detector_ble.py