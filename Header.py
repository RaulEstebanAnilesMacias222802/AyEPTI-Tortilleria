import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1444x1024")
        self.title("Tortilleria Murisol")
        
        # Barra superior
        self.top_bar = Topbar(self, self.show_page)
        self.top_bar.grid(row=0, column=0, sticky="nsew")
        
        # Paginas
        self.frames = {}
        container = ctk.CTkFrame(self, fg_color="white")
        container.grid(row=1, column=0, sticky="nsew")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Creacion de las paginas
        for F in (VentasPage, InventarioPage, ReportesPage):
            page = F(container)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Mostrar la primera página por defecto
        self.show_page("VentasPage")
        
    def show_page(self, page_name):
        """Muestra la página seleccionada"""
        frame = self.frames[page_name]
        frame.tkraise()

class Topbar(ctk.CTkFrame):
    def __init__(self, master, change_page_callback, **kwargs):
        super().__init__(master, fg_color="#00A14A", height=50, corner_radius=0)

        self.change_page_callback = change_page_callback
        
        self.logo_label = ctk.CTkLabel(self, text="Tortilleria\nMurisol", font=("Arial", 24, "bold"),
                                       text_color="white", fg_color="transparent", height=40)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.buttons = []
        self.button_names = [("Ventas", "VentasPage"), ("Inventario", "InventarioPage"), ("Reportes", "ReportesPage")]
        
        for index, (name, page) in enumerate(self.button_names):
            btn = ctk.CTkButton(self, text=name, fg_color="transparent", text_color="white", font=("Arial", 20, "bold"),
                                hover_color="#00A14A", command=lambda p=page: self.change_page(p))
            btn.grid(row=0, column=index + 1, padx=130, pady=10)
            self.buttons.append(btn)

    def change_page(self, page_name):
        """Cambia la página activa y actualiza los botones"""
        self.change_page_callback(page_name)

        for btn, (_, page) in zip(self.buttons, self.button_names):
            btn.configure(text_color="yellow" if page == page_name else "white")

# Pagina de Ventas
class VentasPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")

        # Frame principal horizontal usando grid
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        main_frame.grid_columnconfigure(0, minsize=1200)
        main_frame.grid_columnconfigure(1, minsize=600)
        main_frame.grid_rowconfigure(0, weight=1)

        # Frame izquierdo
        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        detalles_label = ctk.CTkLabel(left_frame, text="Detalles de Venta", font=("Arial", 20, "bold"),
                                      text_color="#B1D800", fg_color="transparent")
        detalles_label.pack(anchor="w")

        detalles_line = ctk.CTkFrame(left_frame, fg_color="#B1D800", height=2)
        detalles_line.pack(fill="x", pady=(0, 5))

        contenido_ventas = ctk.CTkFrame(left_frame, fg_color="transparent")
        contenido_ventas.pack(fill="both", expand=True)

        # Frame derecho
        carrito_frame = ctk.CTkFrame(main_frame, fg_color="transparent", corner_radius=10)
        carrito_frame.grid(row=0, column=1, sticky="nsew", padx=(0,10))

        carrito_label = ctk.CTkLabel(carrito_frame, text="Carrito", font=("Arial", 20, "bold"),
                                     text_color="#B1D800", fg_color="transparent")
        carrito_label.pack(anchor="w")

        carrito_line = ctk.CTkFrame(carrito_frame, fg_color="#B1D800", height=2)
        carrito_line.pack(fill="x", pady=(0, 5))

        carrito_contenido = ctk.CTkLabel(carrito_frame, text="Aquí irán los productos...", text_color="black")
        carrito_contenido.pack(pady=10)

# Página de Inventario
class InventarioPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        label = ctk.CTkLabel(self, text="Página de Inventario", font=("Arial", 24))
        label.pack(pady=50)

# Página de Reportes
class ReportesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        label = ctk.CTkLabel(self, text="Página de Reportes", font=("Arial", 24))
        label.pack(pady=50)

# Ejecutar la app
app = App()
app.mainloop()
