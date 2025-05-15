import customtkinter as ctk
import pyodbc
import pdfkit
from tkcalendar import DateEntry
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

class ReportesPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        
        self.server = 'DESKTOP-7FA4G9M'
        self.database = 'Tortilleria'
        self.trusted_connection = 'Yes'
        self.connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection={self.trusted_connection};TrustServerCertificate=Yes'
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()

        # Configuración de la cuadrícula
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)

        # Frame para los campos de fecha
        fecha_frame = ctk.CTkFrame(self, fg_color="transparent")
        fecha_frame.grid(row=0, column=1, pady=10, sticky="nsew")

        # Calendario Fecha 1
        lbl_fecha1 = ctk.CTkLabel(fecha_frame, text="Fecha 1:", font=("Arial", 14, "bold"), text_color='black')
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

        # Calendario Fecha 2
        lbl_fecha2 = ctk.CTkLabel(fecha_frame, text="Fecha 2:", font=("Arial", 14, "bold"), text_color='black')
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

        # Botón para cargar datos
        btn_cargar = ctk.CTkButton(
            fecha_frame,
            text="Cargar Datos",
            command=self.cargar_datos,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        btn_cargar.grid(row=0, column=4, padx=10, pady=5)

        # Frame para la tabla con scroll vertical
        self.scroll_vertical = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_vertical.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.scroll_vertical.grid_columnconfigure((0,1,2,3,4,5), weight=1)

        # Inicializar tabla
        self.tabla_frame = None
        self.cargar_datos()

        self.btn_imprimir = ctk.CTkButton(
            self,
            text="Imprimir Reporte",
            command=self.generar_pdf,
            font=("Arial", 16, "bold"),
            text_color="black",
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.btn_imprimir.grid(row=2, column=1, padx=10, pady=5)

    def cargar_datos(self):
        # Obtener fechas formateadas para SQL
        fecha_inicio = self.cal_fecha1.get_date().strftime("%Y-%m-%d")
        fecha_fin = self.cal_fecha2.get_date().strftime("%Y-%m-%d")

        # Limpiar tabla anterior
        if self.tabla_frame:
            self.tabla_frame.destroy()

        # Obtener datos del stored procedure
        try:
            self.cursor.execute(f"EXEC SP_ReporteVentasPorRango '{fecha_inicio}', '{fecha_fin}'")
            datos = self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            datos = []

        # Crear nuevo frame para la tabla
        self.tabla_frame = ctk.CTkFrame(self.scroll_vertical, fg_color="transparent")
        self.tabla_frame.pack(fill="both", expand=True)

        # Encabezados
        encabezados = ["Producto", "Día", "Mes", "Año", "Cantidad", "Total"]
        for col, encabezado in enumerate(encabezados):
            ctk.CTkLabel(
                self.tabla_frame,
                text=encabezado,
                font=("Arial", 12, "bold"),
                fg_color="#2b2b2b",
                text_color="white",
                width=120,
                height=30,
                corner_radius=0
            ).grid(row=0, column=col, padx=2, pady=2, sticky="ew")

        # Datos
        for row, fila in enumerate(datos, start=1):
            for col, valor in enumerate(fila):
                ctk.CTkLabel(
                    self.tabla_frame,
                    text=str(valor),
                    fg_color="#f0f0f0",
                    text_color="black",
                    width=120,
                    height=30,
                    corner_radius=0
                ).grid(row=row, column=col, padx=2, pady=2, sticky="ew")

    def generar_pdf(self):
        try:
            fecha_inicio = self.cal_fecha1.get_date().strftime("%d/%m/%Y")
            fecha_fin = self.cal_fecha2.get_date().strftime("%d/%m/%Y")

            # Obtener datos
            fecha_inicio_sql = self.cal_fecha1.get_date().strftime("%Y-%m-%d")
            fecha_fin_sql = self.cal_fecha2.get_date().strftime("%Y-%m-%d")
            self.cursor.execute(f"EXEC SP_ReporteVentasPorRango '{fecha_inicio_sql}', '{fecha_fin_sql}'")
            datos = self.cursor.fetchall()

            # Renderizar PDF
            env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("reporte_template.html")
            html = template.render(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                encabezados=["Producto", "Día", "Mes", "Año", "Cantidad", "Total"],
                datos=datos
            )

            pdfkit.from_string(
                html,
                "reporte.pdf",
                configuration=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'),
                options={"enable-local-file-access": ""}
            )
            print("✅ PDF generado correctamente")
        except Exception as e:
            print(f"❌ Error al generar PDF: {e}")