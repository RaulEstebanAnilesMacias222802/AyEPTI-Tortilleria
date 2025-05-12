import customtkinter as ctk

class InventarioPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        # Encabezados
        headers = ["Productos", "Entradas", "Salidas", "Sobrantes", "Cantidades", "Stock"]
        ancho_columnas = [150, 100, 100, 100, 100, 100]

        self.tabla_frame = ctk.CTkFrame(self, fg_color="#f4f4f4", corner_radius=10)
        self.tabla_frame.pack(padx=20, pady=10, fill="both", expand=False)

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.tabla_frame, text=header, font=("Arial", 16, "bold"), text_color="black")
            label.grid(row=0, column=i, padx=5, pady=10)