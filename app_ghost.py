import flet as ft
import time
import os
import threading

def main(page: ft.Page):
    page.title = "GHOST-PROTOCOL CONTROL"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    
    texto_estado = ft.Text("ESTADO: INICIALIZANDO", size=22, weight="bold", color="white")
    circulo = ft.Container(
        content=ft.Text("🔒", size=60),
        width=180, height=180, bgcolor="#2e7d32",
        border_radius=90, border=ft.Border.all(4, "white"),
    )

    def monitor_ia():
        while True:
            try:
                if os.path.exists("status.txt"):
                    with open("status.txt", "r") as f:
                        estado = f.read().strip()
                    
                    if estado == "ALERTA":
                        texto_estado.value = "ESTADO: ¡INTRUSO!"
                        texto_estado.color = "#ff4b4b"
                        circulo.bgcolor = "#b71c1c"
                        circulo.content = ft.Text("⚠️", size=60)
                    else:
                        texto_estado.value = "ESTADO: PROTEGIDO"
                        texto_estado.color = "#4caf50"
                        circulo.bgcolor = "#2e7d32"
                        circulo.content = ft.Text("🔒", size=60)
                    page.update()
            except: pass
            time.sleep(0.5)

    contenido = ft.Column([
        ft.Container(height=50),
        ft.Text("GHOST-PROTOCOL", size=32, weight="bold", color="blue"),
        ft.Text("SISTEMA DE IDENTIDAD ACTIVO", size=12, color="#94a3b8"),
        ft.Container(height=40),
        circulo,
        ft.Container(height=40),
        texto_estado,
        ft.Text("🔋 Batería Token: 85%", size=16, color="#cbd5e1"),
        ft.Container(height=30),
        ft.Button("MODO EMERGENCIA", color="white", bgcolor="#b71c1c")
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Container(content=contenido, padding=20))
    threading.Thread(target=monitor_ia, daemon=True).start()

if __name__ == "__main__":
    ft.run(main) # Actualizado a .run() como sugirió el Warning