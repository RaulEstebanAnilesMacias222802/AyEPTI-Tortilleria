import customtkinter as ctk
from ventas import VentasPage
from inventario import InventarioPage
from reportes import ReportesPage
from Header import Topbar
from Login import LoginApp

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1444x1024")
        self.title("Tortillería Murisol")

        # Barra superior
        self.top_bar = Topbar(self, self.show_page)
        self.top_bar.grid(row=0, column=0, sticky="nsew")

        # Contenedor de páginas
        container = ctk.CTkFrame(self, fg_color="white")
        container.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Diccionario de páginas
        self.frames = {}
        for PageClass in (LoginApp, VentasPage, InventarioPage, ReportesPage):
            page = PageClass(container)
            self.frames[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Mostrar la página de ventas por defecto
        self.show_page("LoginApp")

    def show_page(self, page_name):
        """Muestra la página seleccionada"""
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
