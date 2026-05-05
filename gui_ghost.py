import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import os

# ==========================================================
# GHOST-PROTOCOL GUI v1.4 - INTERFAZ DE CONTROL CENTRAL
# ==========================================================

class GhostGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la Ventana
        self.title("GHOST-PROTOCOL - Panel de Control")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configuración de Grid (Layout)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. BARRA LATERAL (Menú)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="GHOST\nPROTOCOL", 
                                      font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=20)

        # SWITCH DE SEGURIDAD (El Botón de Pánico)
        self.seguridad_var = ctk.BooleanVar(value=True)
        self.switch_seguridad = ctk.CTkSwitch(self.sidebar_frame, text="Seguridad Máxima", 
                                              variable=self.seguridad_var,
                                              progress_color="green",
                                              command=self.cambiar_modo)
        self.switch_seguridad.pack(pady=40, padx=20)

        # INDICADOR DE BATERÍA (Simulado)
        self.label_bat = ctk.CTkLabel(self.sidebar_frame, text="🔋 Batería Token: 100%", 
                                     font=ctk.CTkFont(size=12))
        self.label_bat.pack(side="bottom", pady=20)

        # 2. PANEL PRINCIPAL (Cámara)
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.camera_label = ctk.CTkLabel(self.main_frame, text="") # Aquí va el video
        self.camera_label.pack(expand=True, fill="both", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self.main_frame, text="SISTEMA BLOQUEADO", 
                                        font=ctk.CTkFont(size=18, weight="bold"),
                                        text_color="red")
        self.status_label.pack(pady=10)

        # Inicializar Cámara
        self.cap = cv2.VideoCapture(0)
        self.mostrar_video()

    def cambiar_modo(self):
        if self.seguridad_var.get():
            self.status_label.configure(text_color="red")
            print(">>> MODO SEGURIDAD MÁXIMA ACTIVADO")
        else:
            self.status_label.configure(text_color="orange")
            print(">>> MODO EMERGENCIA ACTIVADO (Solo IA)")

    def mostrar_video(self):
        ret, frame = self.cap.read()
        if ret:
            # Convertir imagen de OpenCV (BGR) a formato para Interfaz (RGB)
            cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_img)
            # Redimensionar para que quepa en el panel
            img = img.resize((640, 480))
            img_tk = ImageTk.PhotoImage(image=img)
            
            self.camera_label.img_tk = img_tk
            self.camera_label.configure(image=img_tk)
        
        # Repetir cada 10ms (crea el efecto de video)
        self.after(10, self.mostrar_video)

if __name__ == "__main__":
    app = GhostGui()
    app.mainloop()