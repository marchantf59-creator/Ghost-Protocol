# Directorio de Datos y Firmas Local del Sistema

Este directorio funciona como el almacenamiento restringido para las estructuras de datos, persistencia de variables locales y los archivos de configuracion criptografica ocupados por el sistema Ghost-Protocol.

## Componentes y Modelos Almacenados

La carpeta contiene los recursos criticos necesarios para que el demonio de control (app_ghost.py) valide los factores de autenticacion sin depender de servicios de computacion en la nube (Edge Computing):

1. Archivo de Base Biometrica: Guarda el modelo de rostros entrenado en formato serializado XML (modelo_rostro_felipe.xml), el cual contiene los histogramas de patrones binarios calculados por el modulo entrenador.py.
2. Registros de Auditoria: Almacena el historial en texto plano de caidas de conexion, variaciones de señal y logs operativos del sistema de ciberseguridad.

## Directivas de Seguridad Local

* Control de Acceso: El contenido de este directorio debe ser modificado exclusivamente de forma automatizada por los scripts locales de administracion durante las fases de enrolamiento o calibracion de hardware.
* Integridad de los Datos: Cualquier alteracion manual o inyeccion externa en los archivos binarios o mapas de caracteristicas provocara un error de consistencia matematica en el backend de Python, gatillando la directiva de bloqueo preventivo del sistema operativo Windows por sospecha de manipulacion.
