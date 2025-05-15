import customtkinter as ctk
from Reportes import ReportesPage

class Topbar(ctk.CTkFrame):
    def __init__(self, master, change_page_callback, **kwargs):
        super().__init__(master, fg_color="#00A14A", height=50, corner_radius=0, **kwargs)
        self.change_page_callback = change_page_callback

        # Logo de la barra superior
        self.logo_label = ctk.CTkLabel(
            self,
            text="Tortillería\nMurisol",
            font=("Arial", 24, "bold"),
            text_color="white",
            fg_color="transparent",
            height=40
        )
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Definir los botones y páginas
        self.buttons = []
        self.button_names = [
            ("Ventas", "VentasPage"),
            ("Inventario", "InventarioPage"),
            ("Reportes", "ReportesPage")
        ]

        # Crear los botones
        for index, (name, page) in enumerate(self.button_names):
            btn = ctk.CTkButton(
                self,
                text=name,
                fg_color="transparent",
                text_color="white",
                font=("Arial", 20, "bold"),
                hover_color="#00A14A",
                command=lambda p=page: self.change_page(p),
                width=100,
                height=40,
                anchor="center"
            )
            btn.grid(row=0, column=index + 1, padx=130, pady=10)
            self.buttons.append(btn)

    def change_page(self, page_name):
        """Cambia la página activa y actualiza los botones"""
        self.change_page_callback(page_name)

        # Actualizar los colores de los botones según la pagina activa
        for btn, (_, page) in zip(self.buttons, self.button_names):
            if page == page_name:
                btn.configure(text_color="yellow", font=("Arial", 20, "bold", "underline"))
            else:
                btn.configure(text_color="white", font=("Arial", 20, "bold"))
