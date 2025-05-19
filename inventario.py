import customtkinter as ctk
import pyodbc
from tkinter import simpledialog, messagebox
from Conexion import connection_string

class InventarioPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")

        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()

        self.setup_ui()
        self.cargar_datos()

    def setup_ui(self):
        headers = ["Producto", "Cantidad", "Precio", ""]  # Última columna para acciones
        column_widths = [250, 80, 100, 120]

        self.tabla_frame = ctk.CTkFrame(self, fg_color="#f4f4f4", corner_radius=10, height=300)
        self.tabla_frame.pack(padx=20, pady=(10, 10), fill="both", expand=True)

        for i, (header, width) in enumerate(zip(headers, column_widths)):
            header_frame = ctk.CTkFrame(self.tabla_frame, fg_color="#E0E0E0", height=30)
            header_frame.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            header_frame.grid_propagate(False)
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 14, "bold"),
                text_color="black"
            )
            header_label.pack(fill="both", expand=True)
        
        self.tabla_frame.grid_columnconfigure(0, weight=3)
        self.tabla_frame.grid_columnconfigure(1, weight=1)
        self.tabla_frame.grid_columnconfigure(2, weight=1)
        self.tabla_frame.grid_columnconfigure(3, weight=1)

    def cargar_datos(self):
        try:
            self.cursor.execute("""
                SELECT 
                    p.IDproducto,
                    p.Nombre,
                    p.cantidad,
                    p.Precio,
                    (p.cantidad - ISNULL(SUM(dv.Cantidad), 0)) as Stock
                FROM Producto p
                LEFT JOIN Detalles_venta dv ON p.IDproducto = dv.IDproducto
                GROUP BY p.IDproducto, p.Nombre, p.cantidad, p.Precio
                ORDER BY p.IDproducto
            """)

            for widget in self.tabla_frame.winfo_children():
                if widget.grid_info().get("row", 0) > 0:
                    widget.destroy()

            for row_idx, row in enumerate(self.cursor.fetchall(), start=1):
                id_producto, nombre, cantidad, precio, stock = row

                cantidad_valida = cantidad if cantidad is not None else "No Disponible"
                precio_valido = f"${float(precio):.2f}" if precio is not None else "No Disponible"
                nombre_valido = nombre or "No Disponible"

                is_bajo_stock = isinstance(cantidad, int) and cantidad <= 5 and cantidad > 0
                row_bg_color = "#FFCCCC" if is_bajo_stock else "#FFFFFF"

                # Crear fila con formato
                for col_idx, value in enumerate([nombre_valido, cantidad_valida, precio_valido]):
                    cell_frame = ctk.CTkFrame(self.tabla_frame, fg_color=row_bg_color, height=30)
                    cell_frame.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky="nsew")
                    cell_frame.grid_propagate(False)
                    cell_label = ctk.CTkLabel(
                        cell_frame,
                        text=str(value),
                        font=("Arial", 12),
                        text_color="#333333"
                    )
                    cell_label.pack(fill="both", expand=True)

                # Frame para botones
                acciones_frame = ctk.CTkFrame(self.tabla_frame, fg_color=row_bg_color, height=30)
                acciones_frame.grid(row=row_idx, column=3, padx=1, pady=1, sticky="nsew")
                acciones_frame.grid_propagate(False)

                nombre_lower = nombre_valido.strip().lower()
                if nombre_lower in ["tortilla de harina", "totopos"]:
                    boton = ctk.CTkButton(
                        acciones_frame,
                        text="Resurtir",
                        fg_color="#00A14A",
                        hover_color="#1565C0",
                        text_color="white",
                        font=("Arial", 10),
                        width=60,
                        height=24,
                        corner_radius=6,
                        command=lambda nombre=nombre: self.abrir_dialogo_edicion(nombre)
                    )
                    boton.pack(side="left", padx=(2, 4), pady=2)

                # Símbolo de advertencia si está en rojo (bajo stock)
                if is_bajo_stock:
                    advertencia_label = ctk.CTkLabel(
                        acciones_frame,
                        text="⚠️",
                        font=("Arial", 16, "bold"),
                        text_color="#C62828"
                    )
                    advertencia_label.pack(side="left", padx=(4, 0), pady=2)

        except pyodbc.Error as e:
            self.mostrar_error(f"Error al cargar datos:\n{str(e)}")

    def mostrar_error(self, mensaje):
        for widget in self.tabla_frame.winfo_children():
            if widget.grid_info().get("row", 0) > 0:
                widget.destroy()

        ctk.CTkLabel(
            self.tabla_frame,
            text=mensaje,
            text_color="#C62828",
            font=("Arial", 12, "bold"),
            wraplength=550,
            justify="left"
        ).grid(row=1, column=0, columnspan=4, pady=20, padx=10)

    def abrir_dialogo_edicion(self, nombre_producto):
        cantidad_nueva = simpledialog.askinteger(
            "Editar Cantidad",
            f"Ingrese la nueva cantidad para '{nombre_producto}':",
            minvalue=0
        )
        if cantidad_nueva is not None:
            try:
                self.cursor.execute(
                    "UPDATE Producto SET cantidad = ? WHERE Nombre = ?",
                    (cantidad_nueva, nombre_producto)
                )
                self.conn.commit()
                self.cargar_datos()
                messagebox.showinfo("Éxito", f"Cantidad actualizada para '{nombre_producto}'.")
            except pyodbc.Error as e:
                messagebox.showerror("Error SQL", str(e))
