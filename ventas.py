import customtkinter as ctk
from datetime import datetime

class VentasPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")

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
        
        self.carrito_items = []
        self.filas_carrito = []
        # Cambio de precios no funcional
        self.precios_productos = {
            "Tortillas de maíz": {"1kg": 23, "500g": 12, "250g": 6},
            "Tortillas de harina": {"1kg": 28, "500g": 14, "250g": 7},
            "Totopos": {"1kg": 35, "500g": 18, "250g": 9},
            "Chicharron": {"1kg": 45, "500g": 23, "250g": 12}
        }
        # Cantidad
        self.agregar_producto(contenido_ventas, "Tortillas de maíz", 23, ["1kg", "500g", "250g"])
        self.agregar_producto(contenido_ventas, "Tortillas de harina", 28, ["1kg", "500g", "250g"])
        self.agregar_producto(contenido_ventas, "Totopos", 35, ["1kg", "500g", "250g"])
        self.agregar_producto(contenido_ventas, "Chicharron", 45, ["1kg", "500g", "250g"])

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

    def agregar_producto(self, parent, nombre, precio, opciones):
        producto_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        producto_frame.pack(fill="x", pady=5, padx=5)
        producto_frame.grid_columnconfigure(1, weight=1)
        producto_frame.grid_columnconfigure(2, weight=0)

        imagen = ctk.CTkLabel(producto_frame, text="", width=100, height=100, corner_radius=10, fg_color="lightgray")
        imagen.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        nombre_label = ctk.CTkLabel(producto_frame, text=nombre, font=("Arial", 16, "bold"), text_color="#74c900")
        nombre_label.grid(row=0, column=1, sticky="w")

        precio_label = ctk.CTkLabel(producto_frame, text=f"Precio: ${precio}", font=("Arial", 14), text_color="black")
        precio_label.grid(row=1, column=1, sticky="w")

        cantidad_label = ctk.CTkLabel(producto_frame, text="Cantidad:", font=("Arial", 14), text_color="black")
        cantidad_label.grid(row=2, column=1, sticky="w", padx=(0,5))

        combo_borde = ctk.CTkFrame(producto_frame, fg_color="#cccccc", corner_radius=5)
        combo_borde.grid(row=2, column=1, sticky="w", padx=(80, 10))

        combo = ctk.CTkOptionMenu(
            combo_borde,
            values=opciones,
            fg_color="white",
            text_color="black",
            button_color="white",
            button_hover_color="#f0f0f0" 
        )
        combo.pack(padx=1, pady=1)

        agregar_btn = ctk.CTkButton(producto_frame, text="Agregar al carrito", font=("Arial", 12, "bold"),
                                    fg_color="#B1D800", text_color="white", hover_color="#9fc000",
                                    command=lambda: self.agregar_al_carrito(nombre, precio, combo.get(), 1))
        agregar_btn.grid(row=5, column=2, pady=0, padx=(0, 5), sticky="w")



    def agregar_al_carrito(self, nombre, precio, presentacion, cantidad):
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                return
        except ValueError:
            return

        total = precio * cantidad
        row = len(self.filas_carrito) + 1

        lbl_producto = ctk.CTkLabel(self.carrito_tabla, text=f"{nombre} ({presentacion})", font=("Arial", 13), text_color="black")
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
            "precio_unitario": precio,
            "cantidad_entry": cantidad_entry,
            "lbl_total": lbl_total,
            "widgets": [lbl_producto, cantidad_entry, lbl_total, btn_borrar],
            "nombre": nombre,
            "presentacion": presentacion
        }
        self.filas_carrito.append(fila)

    # Evento para actualizar total al modificar cantidad
        cantidad_entry.bind("<KeyRelease>", lambda event: self.actualizar_cantidad(fila))

        self.actualizar_total()

    def actualizar_cantidad(self,fila):
        try:
            nueva_cantidad = int(fila["cantidad_entry"].get())
            if nueva_cantidad < 0:
                nueva_cantidad = 0
        except ValueError:
            nueva_cantidad = 0

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
            
            total_compra = 0
            
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
                    total_compra += total_producto
                    
                    # Mostrar nombre del producto y presentación
                    nombre_text = f"{fila['nombre']} ({fila['presentacion']})"
                    ctk.CTkLabel(producto_frame, text=nombre_text, font=("Arial", 12), 
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
            ctk.CTkLabel(total_frame, text=f"${total_compra:.2f}", font=("Arial", 14, "bold"), 
                        text_color="#B1D800").pack(side="left")
        
        # Mensaje de agradecimiento
        gracias_label = ctk.CTkLabel(self.ticket_container, text="¡Gracias por su compra!", 
                                font=("Arial", 14), text_color="#B1D800")
        gracias_label.pack(pady=(20, 0))

    def finalizar_compra(self):
        for item in self.filas_carrito:
            for widget in item["widgets"]:
                widget.destroy()
        self.filas_carrito.clear()
        self.carrito_items.clear()
        self.actualizar_total()
        ctk.CTkLabel(self.carrito_tabla, text="¡Gracias por su compra!", font=("Arial", 16, "bold"),
                    text_color="#00A14A").grid(row=1, column=0, columnspan=4, pady=20)