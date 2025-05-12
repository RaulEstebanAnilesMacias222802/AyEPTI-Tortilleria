import customtkinter as ctk

class ReportesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        label = ctk.CTkLabel(self, text="Pagina de Reportes", font=("Arial", 24))
        label.pack(pady=50)
