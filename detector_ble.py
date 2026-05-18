import asyncio
from bleak import BleakScanner

# Aquí pondremos la dirección MAC de tu ESP32 cuando lo conectemos mañana
DIRECCION_LLAVE = "TU_ESP32_MAC_AQUI" 

async def monitorear_llave():
    print(">>> GHOST-PROTOCOL: Escaneando llave maestra...")
    
    while True:
        # Escanea los dispositivos Bluetooth cercanos por 3 segundos
        dispositivos = await BleakScanner.discover(timeout=3.0)
        llave_detectada = False
        
        for d in dispositivos:
            # Aquí tu script buscará el nombre o la dirección de tu SuperMini
            if d.name and "ESP32" in d.name:
                print(f"Llave detectada: {d.name} | Señal (RSSI): {d.rssi} dBm")
                llave_detectada = True
                
                # Si la señal es muy baja (ej. menor a -85), significa que te alejaste
                if d.rssi < -85:
                    print("¡ALERTA: Llave demasiado lejos! Preparando bloqueo...")
        
        if not llave_detectada:
            print("¡ALERTA: Llave no encontrada! Perímetro comprometido.")
            # Aquí llamaremos a tu script test_ia_v1.4.py para bloquear
            
        await asyncio.sleep(2) # Espera 2 segundos antes de volver a escanear

# Arranca el bucle de escucha
try:
    asyncio.run(monitorear_llave())
except KeyboardInterrupt:
    print("\nDetector detenido por el usuario.")