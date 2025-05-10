import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import pyodbc

from Header import App

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Login - Tortillería Marisol #2")
        self.geometry("600x400")
        self.resizable(False, False)

        # Configuración de la conexión a la base de datos
        self.server = 'HAZZO'
        self.database = 'Tortilleria'
        self.username = 'sa'
        self.password = 'verde001'
        self.connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'

        # Fondo
        bg_image = Image.open("Tortillas.jpg")
        self.bg_image = ctk.CTkImage(light_image=bg_image, size=(600, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Contenedor del login
        self.login_frame = ctk.CTkFrame(self, width=300, height=260, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Usuario
        self.entry_user = ctk.CTkEntry(self.login_frame, placeholder_text="Usuario")
        self.entry_user.pack(pady=(60, 10), padx=40)

        # Contraseña
        self.entry_pass = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=10, padx=40)

        # Botón de login
        self.btn_login = ctk.CTkButton(self.login_frame, text="Iniciar Sesión", command=self.login)
        self.btn_login.pack(pady=20)

        #Enter
        self.bind("<Return>", lambda event: self.login())

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
                # Credenciales SQL
                query = "SELECT Nombre, Rol FROM Usuario WHERE Nombre = ? AND Contraseña = ?"
                cursor.execute(query, (usuario, contrasena))
                user_data = cursor.fetchone()
                
                if user_data:
                    # El login sale bien
                    nombre, rol = user_data
                    messagebox.showinfo("Login exitoso", f"Bienvenido {nombre} ({rol})")
                    self.destroy()
                    header_app = App()
                    header_app.mainloop()
                else:
                    #El login sale mal
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                    self.entry_user.delete(0, 'end')
                    self.entry_pass.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar credenciales: {str(e)}")
            finally:
                conn.close()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
