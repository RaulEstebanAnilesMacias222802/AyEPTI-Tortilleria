import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login - Tortillería Marisol #2")
        self.geometry("600x400")
        self.resizable(False, False)

        # Fondo
        bg_image = Image.open("Tortillas.jpg")
        self.bg_image = ctk.CTkImage(light_image=bg_image, size=(600, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Marco blanco semi-redondeado (contenedor del login)
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

    def login(self):
        usuario = self.entry_user.get()
        contraseña = self.entry_pass.get()

        if usuario == "admin" and contraseña == "verde001":
            messagebox.showinfo("Login exitoso", "Bienvenido al sistema.")
            self.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            self.entry_user.delete(0, 'end')
            self.entry_pass.delete(0, 'end')

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
