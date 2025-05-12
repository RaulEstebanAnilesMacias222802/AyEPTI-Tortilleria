import customtkinter as ctk
import pyodbc
import pdfkit
from tkcalendar import DateEntry
from jinja2 import Environment, FileSystemLoader

class ReportesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        
        self.server = 'DESKTOP-7FA4G9M'
        self.database = 'Tortilleria'
        self.trusted_connection = 'Yes'
        self.connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection={self.trusted_connection};TrustServerCertificate=Yes';
        conn = pyodbc.connect(self.connection_string)
        def connection(self):
            try:
                conn = pyodbc.connect(self.connection_string)
                return conn
            except Exception as e:
                print("Error de conexión", f"No se pudo conectar a la base de datos: {str(e)}")
                return None
        conn = connection(self)
        self.cursor = conn.cursor()
        # Configuración de columnas para centrar los elementos
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        
        # --- Frame para los botones (centrado) ---
        # --- Frame para los campos de fecha (centrado) ---
        fecha_frame = ctk.CTkFrame(self, fg_color="transparent")
        fecha_frame.grid(row=0, column=1, pady=10, sticky="nsew")
        fecha_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Label y Entry para Fecha 1
        lbl_fecha1 = ctk.CTkLabel(
            fecha_frame, 
            text="Fecha 1:", 
            font=("Arial", 14, "bold"),
            text_color='black'
        )
        lbl_fecha1.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="e")

        self.cal_fecha1 = DateEntry(
            fecha_frame,
            width=12,
            background="darkblue",
            foreground="white",
            date_pattern="dd/mm/yyyy",
            font=("Arial", 12)
        )
        self.cal_fecha1.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="w")

        # Label y Entry para Fecha 2
        lbl_fecha2 = ctk.CTkLabel(
            fecha_frame, 
            text="Fecha 2:", 
            font=("Arial", 14, "bold"),
            text_color='black'
        )
        lbl_fecha2.grid(row=0, column=2, padx=(10, 5), pady=5, sticky="e")

        self.cal_fecha2 = DateEntry(
            fecha_frame,
            width=12,
            background="darkblue",
            foreground="white",
            date_pattern="dd/mm/yyyy",
            font=("Arial", 12)
        )
        self.cal_fecha2.grid(row=0, column=3, padx=(0, 10), pady=5, sticky="w")

        # --- Frame para la tabla (debajo de los botones) ---
        self.scroll_vertical = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_vertical.grid(row=1, column=1, columnspan=1, padx=20, pady=10, sticky="nsew")
        self.scroll_vertical.grid_columnconfigure(0, weight=1)
        self.scroll_horizontal = ctk.CTkScrollableFrame(
            self.scroll_vertical, 
            orientation="horizontal",  # Scroll horizontal
            fg_color="transparent"
        )
        self.scroll_horizontal.configure(height=300)
        self.scroll_horizontal.pack(fill="both", expand=True)

        # Encabezados de la tabla
        encabezados = ["Producto","Día","Mes", "Año", "Cantidad", "Total"]
        for col, encabezado in enumerate(encabezados):
            ctk.CTkLabel(
                self.scroll_horizontal, 
                text=encabezado, 
                font=("Arial", 14, "bold"),
                corner_radius=0,
                fg_color="#2b2b2b",
                text_color="white",
                width=100,
                height=30
            ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        #Botones
        self.botones = ctk.CTkFrame(self, fg_color="transparent")
        self.botones.grid(row=2, column=1, columnspan=1, padx=20, pady=10, sticky="nsew")
        self.botones.grid_columnconfigure((0,1), weight=1)
        #Botón para mostrar reporte semanal
        self.btn_semanal = ctk.CTkButton(
            self.botones, 
            text="Mostrar reporte", 
            fg_color="#fff593", 
            text_color="black", 
            font=("Arial", 20, "bold"), 
            hover_color="#fcec49",
            height=40,
            command=self.cargar_datos
        )
        self.btn_semanal.grid(row=0, column=0, padx=5, pady=20, sticky="nsew")
        #Botón para generar reporte semanal
        self.btn_semanal = ctk.CTkButton(
            self.botones, 
            text="Generar Reporte", 
            fg_color="#7dffb9", 
            text_color="black", 
            font=("Arial", 20, "bold"), 
            hover_color="#41fa96",
            height=40,
            command=self.generar_pdf
        )
        self.btn_semanal.grid(row=0, column=1, padx=5, pady=20, sticky="nsew")

    def obtener_fechas(self):
        return self.cal_fecha1.get_date(), self.cal_fecha2.get_date()

    def cargar_datos(self):
        self.cursor.execute(f"EXEC SP_ReporteVentasPorRango '{self.cal_fecha1.get_date()}', '{self.cal_fecha2.get_date()}'")
        for row, (Producto, Dia, Mes, Anio, CantidadTotal, TotalGenerado) in enumerate(self.cursor.fetchall(), start=1):
            ctk.CTkLabel(
                self.scroll_horizontal, 
                text=Producto,
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=0, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                self.scroll_horizontal, 
                text=str(Dia),
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=1, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                self.scroll_horizontal, 
                text=str(Mes),
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=2, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                self.scroll_horizontal, 
                text=str(Anio),
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=3, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                self.scroll_horizontal, 
                text=str(CantidadTotal),
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=4, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                self.scroll_horizontal,
                text=str('{0:.2f}'.format(TotalGenerado)),
                fg_color="#f0f0f0",
                text_color="black",
                width=120,
                height=30
            ).grid(row=row, column=5, padx=5, pady=5, sticky="ew")

    def generar_pdf(self):
        try:
            # Obtener fechas de los calendarios
            fecha_inicio = self.cal_fecha1.get_date().strftime("%d/%m/%Y")
            fecha_fin = self.cal_fecha2.get_date().strftime("%d/%m/%Y")

            # Datos de ejemplo (reemplaza con tus datos reales)
            encabezados = ["Producto","Día","Mes", "Año", "Cantidad", "Total"]
            self.cursor.execute(f"EXEC SP_ReporteVentasPorRango '{self.cal_fecha1.get_date()}', '{self.cal_fecha2.get_date()}'")
            datos = self.cursor.fetchall()

            # Renderizar plantilla HTML con Jinja2
            env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("reporte_template.html")
            html = template.render(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                encabezados=encabezados,
                datos=datos
            )

            # Configurar pdfkit (ajusta la ruta de wkhtmltopdf si es necesario)
            ruta = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=ruta)
            
            # Generar PDF
            pdfkit.from_string(
                html,
                "reporte.pdf",
                configuration=config,
                options={"enable-local-file-access": ""}
            )

            print("✅ PDF generado correctamente como 'reporte.pdf'")
        except Exception as e:
            print(f"❌ Error al generar PDF: {e}")
