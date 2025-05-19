import customtkinter as ctk
from PIL import Image
import tkinter.messagebox as messagebox
import pyodbc
from Conexion import connection_string

class LoginApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.configure(width=600, height=400)

        # Configuración de la base de datos
        self.connection_string = connection_string

        # Fondo
        bg_image = Image.open("Tortillas.jpg")
        self.bg_image = ctk.CTkImage(light_image=bg_image, size=(600, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Contenedor del login
        self.login_frame = ctk.CTkFrame(self, width=300, height=260, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.entry_user = ctk.CTkEntry(self.login_frame, placeholder_text="Usuario")
        self.entry_user.pack(pady=(60, 10), padx=40)
        self.entry_user.bind("<Return>", lambda event: self.login())

        self.entry_pass = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=10, padx=40)
        self.entry_pass.bind("<Return>", lambda event: self.login())

        self.btn_login = ctk.CTkButton(self.login_frame, text="Iniciar Sesión", command=self.login)
        self.btn_login.pack(pady=20)

    def connect_db(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            return conn
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {str(e)}")
            return None

    def login(self):
        usuario = self.entry_user.get()
        contrasena = self.entry_pass.get()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return

        conn = self.connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT IDusuario, Nombre, Rol FROM Usuario WHERE Nombre = ? AND Contrasena = ?"
                cursor.execute(query, (usuario, contrasena))
                user_data = cursor.fetchone()

                if user_data:
                    id_usuario, nombre, rol = user_data
                    messagebox.showinfo("Login exitoso", f"Bienvenido {nombre} ({rol})")
                    
                    # Pasar el usuario a la página de ventas
                    self.master.ventas_page.set_usuario(id_usuario, nombre)
                    
                    # Cambiar a la página de ventas
                    self.master.show_page("VentasPage")
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                    self.entry_user.delete(0, 'end')
                    self.entry_pass.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar credenciales: {str(e)}")
            finally:
                conn.close()