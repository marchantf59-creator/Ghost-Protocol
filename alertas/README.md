# Repositorio de Alertas de Intrusion y Registro Forense

Este directorio funciona como el almacenamiento local y automatizado de evidencia automatizada ante eventos de vulneracion perimetral o fallas de autenticacion en el sistema Ghost-Protocol.

## Funcionamiento del Modulo de Mitigacion

Cuando el script principal (app_ghost.py) detecta una de las siguientes condiciones de riesgo, el hilo secundario de mitigacion activa de forma asincrona la camara web mediante OpenCV antes de invocar la API de bloqueo del sistema operativo:

1. Ausencia del Operador: Rostro no detectado en el canal optico local mientras el terminal permanece en estado activo.
2. Intento de Suplantacion: Deteccion de un rostro cuya tasa de confianza matematica en el algoritmo de Histogramas de Patrones Binarios Locales (LBPH) no coincide con el perfil entrenado (modelo_rostro_felipe.xml).
3. Perdida de Factor Fisico: Desconexion o alejamiento del hardware perimetral portatil (ESP32-C3) por debajo del umbral critico de -85 dBm de señal RSSI.

## Estructura de los Archivos Guardados

Los archivos se almacenan en formato binario estandar de imagen (.jpg) utilizando la siguiente nomenclatura automatizada para garantizar la integridad de la linea de tiempo:

* Formato del nombre: intruso_AAAAMMDD_HHMMSS.jpg
* Descripcion: Cada captura almacena el fotograma exacto en escala de grises o color de la region de interes (ROI) analizada por el clasificador Haar Cascade al momento de gatillarse la excepcion de seguridad.

## Directivas de Administracion

* Almacenamiento Volatil: Estas imagenes estan destinadas a la auditoria local inmediata del operador legitimo tras recuperar el acceso seguro mediante el script de contingencia (recovery_handler.py).
* Purga de Datos: Por diseño de seguridad, se recomienda la revision y purga periodica de este directorio para evitar el consumo innecesario de almacenamiento en el disco local de la estacion de trabajo host.
