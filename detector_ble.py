import asyncio
import os
from bleak import BleakScanner

TARGET_MAC = "98:3d:ae:52:f9:2c"
BLE_STATUS_FILE = "status_ble.txt"

def actualizar_estado_ble(rssi, presencial):
    """Escribe de forma rápida y segura el estado de proximidad en el disco."""
    try:
        # Usamos un archivo temporal intermedio para evitar corrupciones de lectura en paralelo
        with open(f"{BLE_STATUS_FILE}.tmp", "w") as f:
            f.write(f"{'PRESENTE' if presencial else 'AUSENTE'}|{rssi}")
        if os.path.exists(f"{BLE_STATUS_FILE}.tmp"):
            os.replace(f"{BLE_STATUS_FILE}.tmp", BLE_STATUS_FILE)
    except Exception as e:
        pass # Silencioso para no romper el callback de alta velocidad

def callback_deteccion(device, advertising_data):
    """Se ejecuta instantáneamente cada vez que entra una trama BLE."""
    # Validamos por MAC estática o por nombre del firmware de la ESP32
    if device.address.lower() == TARGET_MAC or (device.name and "GHOST" in device.name.upper()):
        rssi = advertising_data.rssi
        print(f"   [GHOST-BLE] Dispositivo detectado -> RSSI: {rssi} dBm")
        actualizar_estado_ble(rssi, presencial=True)

async def monitorear_llave():
    print(">>> [GHOST-PROTOCOL] INITIALIZING PASSIVE BLE SCANNER...")
    # Inicializamos el scanner con el callback continuo
    scanner = BleakScanner(detection_callback=callback_deteccion)
    await scanner.start()
    
    ultimo_rssi = -100
    try:
        while True:
            # Si el script óptico necesita leer latidos, aquí confirmamos que el script sigue vivo
            # El callback se encarga de actualizar los datos en tiempo real de forma pasiva
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await scanner.stop()

if __name__ == "__main__":
    try:
        # Inicialización limpia del loop asíncrono
        asyncio.run(monitorear_llave())
    except KeyboardInterrupt:
        print("\n[GHOST-BLE] Scanner detenido por el operador.")