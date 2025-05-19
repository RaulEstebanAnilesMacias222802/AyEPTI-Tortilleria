import customtkinter as ctk
from datetime import datetime
import pyodbc
from Conexion import connection_string

class VentasPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.usuario_actual = None
        self.id_usuario = None
        self.carrito_items = []
        self.filas_carrito = []

        try:
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()
            self.conn.autocommit = False
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conn = None
            self.cursor = None

        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        main_frame.grid_columnconfigure(0, minsize=1200)
        main_frame.grid_columnconfigure(1, minsize=800)
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
        
        # Cargar productos desde la base de datos
        self.cargar_productos(contenido_ventas)

        # Frame derecho - CARRITO
        carrito_frame = ctk.CTkFrame(main_frame, fg_color="transparent", corner_radius=10)
        carrito_frame.grid(row=0, column=1, sticky="nsew", padx=(0,10))

        carrito_label = ctk.CTkLabel(carrito_frame, text="Carrito", font=("Arial", 20, "bold"),
                                    text_color="#B1D800", fg_color="transparent")
        carrito_label.pack(anchor="w")

        carrito_line = ctk.CTkFrame(carrito_frame, fg_color="#B1D800", height=2)
        carrito_line.pack(fill="x", pady=(0, 5))

        # Tabla visual
        self.carrito_tabla = ctk.CTkFrame(carrito_frame, fg_color="white")
        self.carrito_tabla.pack(fill="both", expand=True, padx=5, pady=5)

        # Encabezados tabla
        headers = ["Producto", "Cantidad", "Total", "Borrar"]
        for col, texto in enumerate(headers):
            header = ctk.CTkLabel(self.carrito_tabla, text=texto, font=("Arial", 13, "bold"), text_color="black")
            header.grid(row=0, column=col, padx=5, pady=5)

        self.total_label = ctk.CTkLabel(carrito_frame, text="Total: $0.00", font=("Arial", 16), text_color="black")
        self.total_label.pack(pady=10)

        # Configuración del cuadro de ticket
        self.cuadro_ticket = ctk.CTkFrame(self, width=450, height=600, fg_color="white", border_width=1, border_color="#B1D800")
        self.cuadro_ticket.pack_propagate(False)
        self.cuadro_ticket.place_forget()
        
        # Frame para el contenido del ticket (scrollable)
        self.ticket_container = ctk.CTkScrollableFrame(self.cuadro_ticket, fg_color="white")
        self.ticket_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón para cerrar el ticket
        self.btn_cerrar_ticket = ctk.CTkButton(self.cuadro_ticket, text="Cerrar", command=self.ocultar_ticket, 
                                            font=("Arial", 14, "bold"), fg_color="#B1D800", text_color="white", 
                                            hover_color="#9fc000", width=100)
        self.btn_cerrar_ticket.pack(pady=(0, 10))

        # Botón TICKET
        boton_mostrar = ctk.CTkButton(carrito_frame, text="TICKET", command=self.mostrar_ticket, 
                                    font=("Arial", 16, "bold"), fg_color="#B1D800", text_color="white", 
                                    hover_color="#9fc000")
        boton_mostrar.pack(pady=20)

        finalizar_btn = ctk.CTkButton(carrito_frame, text="Finalizar Compra", font=("Arial", 16, "bold"),
                                    fg_color="#B1D800", text_color="white", hover_color="#9fc000",
                                    command=self.finalizar_compra)
        finalizar_btn.pack(pady=10)

    def cargar_productos(self, parent):
        """Carga los productos desde la base de datos y los muestra en la interfaz"""
        try:
            if self.conn is None:
                self.conn = pyodbc.connect(connection_string)
                self.cursor = self.conn.cursor()

            query = "SELECT IDproducto, Nombre, Precio FROM Producto"
            self.cursor.execute(query)
            productos = self.cursor.fetchall()

            for producto in productos:
                id_producto, nombre, precio = producto
                precio = float(precio)
                self.agregar_producto(parent, nombre, precio, id_producto)

        except Exception as e:
            print(f"Error al cargar productos: {e}")

    def agregar_producto(self, parent, nombre, precio, id_producto):
        producto_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        producto_frame.pack(fill="x", pady=5, padx=5)
        producto_frame.grid_columnconfigure(1, weight=1)
        producto_frame.grid_columnconfigure(2, weight=0)

        imagen = ctk.CTkLabel(producto_frame, text="", width=100, height=100, corner_radius=10, fg_color="lightgray")
        imagen.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        nombre_label = ctk.CTkLabel(producto_frame, text=nombre, font=("Arial", 16, "bold"), text_color="#74c900")
        nombre_label.grid(row=0, column=1, sticky="w")

        precio_label = ctk.CTkLabel(producto_frame, text=f"Precio: ${precio:.2f}", font=("Arial", 14), text_color="black")
        precio_label.grid(row=1, column=1, sticky="w")

        cantidad_label = ctk.CTkLabel(producto_frame, text="Cantidad:", font=("Arial", 14), text_color="black")
        cantidad_label.grid(row=2, column=1, sticky="w", padx=(0,5))

        cantidad_entry = ctk.CTkEntry(producto_frame, width=50, font=("Arial", 14))
        cantidad_entry.insert(0, "1")
        cantidad_entry.grid(row=2, column=1, sticky="w", padx=(80, 10))

        agregar_btn = ctk.CTkButton(producto_frame, text="Agregar al carrito", font=("Arial", 12, "bold"),
                                  fg_color="#B1D800", text_color="white", hover_color="#9fc000",
                                  command=lambda: self.agregar_al_carrito(
                                      id_producto, nombre, precio, cantidad_entry.get()))
        agregar_btn.grid(row=5, column=2, pady=0, padx=(0, 5), sticky="w")

    def agregar_al_carrito(self, id_producto, nombre, precio, cantidad):
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                return
        except ValueError:
            return

        # Verificar si el producto ya está en el carrito
        for item in self.filas_carrito:
            if item["id_producto"] == id_producto:
                # Actualizar cantidad si ya existe
                nueva_cantidad = int(item["cantidad_entry"].get()) + cantidad
                item["cantidad_entry"].delete(0, 'end')
                item["cantidad_entry"].insert(0, str(nueva_cantidad))
                self.actualizar_cantidad(item)
                return

        total = precio * cantidad
        row = len(self.filas_carrito) + 1

        lbl_producto = ctk.CTkLabel(self.carrito_tabla, text=nombre, font=("Arial", 13), text_color="black")
        lbl_producto.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        cantidad_entry = ctk.CTkEntry(self.carrito_tabla, width=50, font=("Arial", 13))
        cantidad_entry.insert(0, str(cantidad))
        cantidad_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

        lbl_total = ctk.CTkLabel(self.carrito_tabla, text=f"${total:.2f}", font=("Arial", 13), text_color="black")
        lbl_total.grid(row=row, column=2, padx=5, pady=5, sticky="w")

        btn_borrar = ctk.CTkButton(self.carrito_tabla, text="X", width=30, height=30,
                                fg_color="#ff4444", hover_color="#cc0000",
                                command=lambda: self.eliminar_del_carrito(row))
        btn_borrar.grid(row=row, column=3, padx=5, pady=5)

        # Guardar referencias
        fila = {
            "row": row,
            "id_producto": id_producto,
            "precio_unitario": precio,
            "cantidad_entry": cantidad_entry,
            "lbl_total": lbl_total,
            "widgets": [lbl_producto, cantidad_entry, lbl_total, btn_borrar],
            "nombre": nombre
        }
        self.filas_carrito.append(fila)

        # Evento para actualizar total al modificar cantidad
        cantidad_entry.bind("<KeyRelease>", lambda event: self.actualizar_cantidad(fila))

        self.actualizar_total()

    def actualizar_cantidad(self, fila):
        try:
            nueva_cantidad = int(fila["cantidad_entry"].get())
            if nueva_cantidad < 0:
                nueva_cantidad = 0
                fila["cantidad_entry"].delete(0, 'end')
                fila["cantidad_entry"].insert(0, "0")
        except ValueError:
            nueva_cantidad = 0
            fila["cantidad_entry"].delete(0, 'end')
            fila["cantidad_entry"].insert(0, "0")

        nuevo_total = fila["precio_unitario"] * nueva_cantidad
        fila["lbl_total"].configure(text=f"${nuevo_total:.2f}")
        self.actualizar_total()

    def eliminar_del_carrito(self, row):
        for fila in self.filas_carrito:
            if fila["row"] == row:
                for widget in fila["widgets"]:
                    widget.destroy()
                self.filas_carrito.remove(fila)
                break
        self.actualizar_total()

    def actualizar_total(self):
        total = 0
        for fila in self.filas_carrito:
            try:
                cantidad = int(fila["cantidad_entry"].get())
                if cantidad < 0:
                    cantidad = 0
            except ValueError:
                cantidad = 0
            total += cantidad * fila["precio_unitario"]

        self.total_label.configure(text=f"Total: ${total:.2f}")

    def mostrar_ticket(self):
        self.actualizar_ticket()
        self.cuadro_ticket.place(relx=0.5, rely=0.5, anchor="center")
        # Limpiar el campo de pago si existe
        if hasattr(self, 'pago_entry'):
            self.pago_entry.delete(0, 'end')
        # Limpiar el frame de cambio si existe
        if hasattr(self, 'cambio_frame'):
            for widget in self.cambio_frame.winfo_children():
                widget.destroy()

    def ocultar_ticket(self):
        self.cuadro_ticket.place_forget()

    def actualizar_ticket(self):
        # Limpiar el contenido anterior del ticket
        for widget in self.ticket_container.winfo_children():
            widget.destroy()
        
        # Agregar el encabezado del ticket
        cuadro_label = ctk.CTkLabel(self.ticket_container, text="TICKET DE COMPRA", font=("Arial", 18, "bold"), 
                                text_color="#B1D800")
        cuadro_label.pack(anchor="center", pady=(0, 10))
        
        cuadro_line = ctk.CTkFrame(self.ticket_container, fg_color="#B1D800", height=2)
        cuadro_line.pack(fill="x", pady=(0, 10))
        
        # Agregar información de fecha/hora
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        fecha_label = ctk.CTkLabel(self.ticket_container, text=f"Fecha: {fecha_hora}", 
                                font=("Arial", 12), text_color="black")
        fecha_label.pack(anchor="w", pady=(0, 15))
        
        # Agregar información del vendedor
        if hasattr(self, 'nombre_usuario'):
            vendedor_label = ctk.CTkLabel(self.ticket_container, text=f"Vendedor: {self.nombre_usuario}", 
                                        font=("Arial", 12), text_color="black")
            vendedor_label.pack(anchor="w", pady=(0, 15))
        
        # Agregar los productos del carrito
        if not self.filas_carrito:
            vacio_label = ctk.CTkLabel(self.ticket_container, text="El carrito está vacío", 
                                    font=("Arial", 14), text_color="gray")
            vacio_label.pack(pady=20)
        else:
            # Encabezados de la tabla
            headers_frame = ctk.CTkFrame(self.ticket_container, fg_color="transparent")
            headers_frame.pack(fill="x", pady=(0, 5))
            
            ctk.CTkLabel(headers_frame, text="Producto", font=("Arial", 12, "bold"), 
                        text_color="black", width=180, anchor="w").pack(side="left")
            ctk.CTkLabel(headers_frame, text="Cant.", font=("Arial", 12, "bold"), 
                        text_color="black", width=50, anchor="center").pack(side="left", padx=5)
            ctk.CTkLabel(headers_frame, text="P.Unit.", font=("Arial", 12, "bold"), 
                        text_color="black", width=70, anchor="center").pack(side="left", padx=5)
            ctk.CTkLabel(headers_frame, text="Total", font=("Arial", 12, "bold"), 
                        text_color="black", width=70, anchor="center").pack(side="left")
            
            # Línea divisoria
            ctk.CTkFrame(self.ticket_container, fg_color="#e0e0e0", height=1).pack(fill="x", pady=5)
            
            self.total_compra = 0  # Guardamos el total como atributo para usarlo después
            
            # Agregar cada producto
            for fila in self.filas_carrito:
                try:
                    cantidad = int(fila["cantidad_entry"].get())
                    if cantidad <= 0:
                        continue
                        
                    producto_frame = ctk.CTkFrame(self.ticket_container, fg_color="transparent")
                    producto_frame.pack(fill="x", pady=2)
                    
                    precio_unitario = fila["precio_unitario"]
                    total_producto = precio_unitario * cantidad
                    self.total_compra += total_producto
                    
                    # Mostrar nombre del producto
                    ctk.CTkLabel(producto_frame, text=fila['nombre'], font=("Arial", 12), 
                                text_color="black", width=180, anchor="w").pack(side="left")
                    ctk.CTkLabel(producto_frame, text=str(cantidad), font=("Arial", 12), 
                                text_color="black", width=50, anchor="center").pack(side="left", padx=5)
                    ctk.CTkLabel(producto_frame, text=f"${precio_unitario:.2f}", font=("Arial", 12), 
                                text_color="black", width=70, anchor="center").pack(side="left", padx=5)
                    ctk.CTkLabel(producto_frame, text=f"${total_producto:.2f}", font=("Arial", 12), 
                                text_color="black", width=70, anchor="center").pack(side="left")
                
                except ValueError:
                    continue
            
            # Línea divisoria antes del total
            ctk.CTkFrame(self.ticket_container, fg_color="#e0e0e0", height=1).pack(fill="x", pady=10)
            
            # Mostrar el total
            total_frame = ctk.CTkFrame(self.ticket_container, fg_color="transparent")
            total_frame.pack(fill="x", pady=(0, 20))
            
            ctk.CTkLabel(total_frame, text="TOTAL:", font=("Arial", 14, "bold"), 
                        text_color="black").pack(side="left", padx=(120, 10))
            ctk.CTkLabel(total_frame, text=f"${self.total_compra:.2f}", font=("Arial", 14, "bold"), 
                        text_color="#B1D800").pack(side="left")
            
            # Sección de pago
            pago_frame = ctk.CTkFrame(self.ticket_container, fg_color="transparent")
            pago_frame.pack(fill="x", pady=(10, 5))
            
            ctk.CTkLabel(pago_frame, text="Pago:", font=("Arial", 14, "bold"), 
                        text_color="black").pack(side="left", padx=(100, 10))
            
            self.pago_entry = ctk.CTkEntry(pago_frame, width=100, font=("Arial", 14))
            self.pago_entry.pack(side="left")
            
            # Botón para calcular cambio
            calcular_btn = ctk.CTkButton(pago_frame, text="Calcular", font=("Arial", 12),
                                    command=self.calcular_cambio, width=80)
            calcular_btn.pack(side="left", padx=10)
            
            # Frame para mostrar el cambio
            self.cambio_frame = ctk.CTkFrame(self.ticket_container, fg_color="transparent")
            self.cambio_frame.pack(fill="x", pady=(0, 20))
        
        # Mensaje de agradecimiento
        gracias_label = ctk.CTkLabel(self.ticket_container, text="¡Gracias por su compra!", 
                                font=("Arial", 14), text_color="#B1D800")
        gracias_label.pack(pady=(20, 0))

    def calcular_cambio(self):
        # Limpiar el frame de cambio si ya tenía contenido
        for widget in self.cambio_frame.winfo_children():
            widget.destroy()
        
        try:
            pago = float(self.pago_entry.get())
            cambio = pago - self.total_compra
            
            if cambio < 0:
                ctk.CTkLabel(self.cambio_frame, text="Pago insuficiente", 
                            font=("Arial", 14), text_color="#ff0000").pack()
            else:
                ctk.CTkLabel(self.cambio_frame, text="Cambio:", 
                            font=("Arial", 14, "bold"), text_color="black").pack(side="left", padx=(120, 10))
                ctk.CTkLabel(self.cambio_frame, text=f"${cambio:.2f}", 
                            font=("Arial", 14, "bold"), text_color="#B1D800").pack(side="left")
        except ValueError:
            ctk.CTkLabel(self.cambio_frame, text="Ingrese un valor válido", 
                        font=("Arial", 14), text_color="#ff0000").pack()

    def set_usuario(self, id_usuario, nombre_usuario):
        """Establece el usuario actual para registrar las ventas"""
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario

    def finalizar_compra(self):
        if not self.filas_carrito:
            return

        try:
            # Verificar que tenemos un usuario válido
            if not hasattr(self, 'id_usuario'):
                raise Exception("No se ha identificado al usuario")

            # Calcular el total de la venta
            total = 0
            for fila in self.filas_carrito:
                cantidad = int(fila["cantidad_entry"].get())
                total += cantidad * fila["precio_unitario"]

            # Insertar la venta y obtener el ID
            query_venta = """
            INSERT INTO Venta (Total, Fecha, IDusuario) 
            OUTPUT INSERTED.IDventa
            VALUES (?, GETDATE(), ?)
            """
            self.cursor.execute(query_venta, (total, self.id_usuario))
        
            # Obtener el ID de la venta insertada
            id_venta = self.cursor.fetchone()[0]
        
            # Insertar los detalles de la venta
            for fila in self.filas_carrito:
                cantidad = int(fila["cantidad_entry"].get())
                if cantidad > 0:
                    query_detalle = """
                    INSERT INTO Detalles_Venta (IDventa, IDproducto, Cantidad) 
                    VALUES (?, ?, ?)
                    """
                    self.cursor.execute(query_detalle, (id_venta, fila["id_producto"], cantidad))

            # Confirmar la transacción
            self.conn.commit()

            # Limpiar el carrito
            for item in self.filas_carrito:
                for widget in item["widgets"]:
                    widget.destroy()

            self.filas_carrito.clear()
            self.actualizar_total()
        
            # Mostrar mensaje de éxito
            ctk.CTkLabel(self.carrito_tabla, text="¡Venta registrada con éxito!", font=("Arial", 16, "bold"),
                        text_color="#00A14A").grid(row=1, column=0, columnspan=4, pady=20)

            # Mostrar el ticket
            self.mostrar_ticket()

        except Exception as e:
            print(f"Error al finalizar compra: {e}")
            if self.conn:
                self.conn.rollback()
            # Mostrar mensaje de error
            ctk.CTkLabel(self.carrito_tabla, text=f"Error al registrar venta: {str(e)}", font=("Arial", 16, "bold"),
                        text_color="#ff0000").grid(row=1, column=0, columnspan=4, pady=20)
