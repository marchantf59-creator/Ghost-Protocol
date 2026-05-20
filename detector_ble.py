import asyncio
from bleak import BleakScanner

async def monitorear_llave():
    print(">>> GHOST-PROTOCOL: Escaneando TODO el perímetro Bluetooth...")
    
    while True:
        # Usamos discover de forma que nos devuelva el dispositivo y sus datos de anuncio por separado
        dispositivos = await BleakScanner.discover(timeout=3.0, return_adv=True)
        
        print(f"\n--- Dispositivos detectados en este ciclo ({len(dispositivos)}): ---")
        
        # Ahora recorremos usando la estructura nueva de bleak
        for direccion, (d, adv) in dispositivos.items():
            nombre = d.name if d.name else 'Desconocido'
            rssi = adv.rssi # Aquí sacamos la señal de forma correcta
            
            print(f"-> MAC: {direccion} | Nombre: {nombre} | Señal: {rssi} dBm")
            
            # Buscamos tu llave por su nombre en mayúsculas o su dirección MAC física
            if "GHOST" in nombre.upper() or direccion.lower() == "98:3d:ae:52:f9:2c":
                print(f"   [¡ALERTA!] ¡Misión cumplida! Se encontró la llave maestra.")
        
        await asyncio.sleep(2)

try:
    asyncio.run(monitorear_llave())
except KeyboardInterrupt:
    print("\nDetector detenido por el usuario.")