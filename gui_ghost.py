import customtkinter as ctk

# Configuración del tema (Modo Oscuro como todo buen programador)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppGhost(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana Principal
        self.title("GHOST-PROTOCOL v1.0 - CFMC SECURITY")
        self.geometry("900x500")

        # Configuración de columnas (Menú lateral y Panel de Video)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Menú Lateral (Sidebar)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="CFMC SECURITY", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botones del Menú
        self.btn_inicio = ctk.CTkButton(self.sidebar, text="Iniciar Vigilancia", command=self.inicio_evento)
        self.btn_inicio.grid(row=1, column=0, padx=20, pady=10)

        self.btn_alertas = ctk.CTkButton(self.sidebar, text="Ver Alertas", command=self.alertas_evento)
        self.btn_alertas.grid(row=2, column=0, padx=20, pady=10)

        # 2. Panel Central (Donde irá el video después)
        self.main_panel = ctk.CTkFrame(self, corner_radius=15)
        self.main_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.status_label = ctk.CTkLabel(self.main_panel, text="SISTEMA LISTO", font=ctk.CTkFont(size=15))
        self.status_label.pack(expand=True)

    # Funciones de los botones
    def inicio_evento(self):
        print("Iniciando motor de IA...")
        self.status_label.configure(text="SISTEMA EN LÍNEA", text_color="green")

    def alertas_evento(self):
        print("Abriendo carpeta de alertas...")

# Arrancar la aplicación
if __name__ == "__main__":
    app = AppGhost()
    app.mainloop()