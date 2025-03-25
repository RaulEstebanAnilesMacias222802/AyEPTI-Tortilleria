import customtkinter as ctk

BUTTON_COLOR = "#1ABC9C"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1444x1024")
        self.title("Tortilleria Murisol")
        
        self.top_bar = Topbar(self)
        self.top_bar.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # Parte de arriba con color, tamaño etc.
class Topbar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#00A14A", height=50, corner_radius=0)

        self.logo_label = ctk.CTkLabel(self, text="Tortilleria\nMurisol", font=("Arial", 24, "bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Crear botones de pestañas
        # Faltaria cambiar esta parte
        self.buttons = []
        self.button_names = ["Ventas", "Inventario", "Reportes"]
        
        for index, name in enumerate(self.button_names):
            btn = ctk.CTkButton(self, text=name, fg_color="transparent", text_color="white", font=("Arial", 20, "bold"),
                                hover_color="#00A14A", command=lambda n=index: self.select_tab(n))
            btn.grid(row=0, column=index+1, padx=130, pady=10)
            self.buttons.append(btn)

    def select_tab(self, selected_index):
        # Cambiar de color los botones
        for index, btn in enumerate(self.buttons):
            if index == selected_index:
                btn.configure(text_color="yellow")  # Boton seleccionado en amarillo
            else:
                btn.configure(text_color="white")   # Restaurar los demas a blanco


# Ejecutar la app
app = App()
app.mainloop()
