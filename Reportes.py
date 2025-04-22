import customtkinter as ctk

class ReportesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        
        # Configuración de columnas para centrar los elementos
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        
        # --- Frame para los botones (centrado) ---
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=0, column=1, sticky="", pady=10)
        button_frame.grid_columnconfigure((0,1), weight=1)

        # Botón Diario
        self.btn_diario = ctk.CTkButton(
            button_frame, 
            text="Reporte Diario", 
            fg_color="#7dffb9", 
            text_color="black", 
            font=("Arial", 20, "bold"), 
            hover_color="#41fa96", 
            width=100, 
            height=40
        )
        self.btn_diario.grid(row=0, column=0, padx=5, pady=20, sticky="nsew")

        # Botón Semanal
        self.btn_semanal = ctk.CTkButton(
            button_frame, 
            text="Reporte Semanal", 
            fg_color="#fff593", 
            text_color="black", 
            font=("Arial", 20, "bold"), 
            hover_color="#fcec49", 
            width=100, 
            height=40
        )
        self.btn_semanal.grid(row=0, column=1, padx=5, pady=20, sticky="nsew")

        # --- Frame para la tabla (debajo de los botones) ---
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.grid(row=1, column=1, columnspan=1, padx=20, pady=10, sticky="nsew")

        # Encabezados de la tabla
        encabezados = ["Reporte", "Fecha DD/MM/YYYY", "Descargar"]
        for col, encabezado in enumerate(encabezados):
            ctk.CTkLabel(
                table_frame, 
                text=encabezado, 
                font=("Arial", 14, "bold"),
                corner_radius=0,
                fg_color="#2b2b2b",
                text_color="white",
                width=200,
                height=30
            ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        # Datos de ejemplo
        datos = [
            ("Ana", 25, "Madrid"),
            ("Luis", 30, "Barcelona"),
            ("Marta", 22, "Valencia")
        ]

        # Filas de datos
        for row, (nombre, edad, ciudad) in enumerate(datos, start=1):
            ctk.CTkLabel(
                table_frame, 
                text=nombre,
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=0, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                table_frame, 
                text=str(edad),
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=1, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                table_frame, 
                text=ciudad,
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=2, padx=5, pady=5, sticky="ew")
