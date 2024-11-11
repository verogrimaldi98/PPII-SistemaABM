import customtkinter
from main import *

class IndexWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inicio de sesión")
        customtkinter.set_appearance_mode("light")
        self.geometry("350x450")

        self.resizable(False, False)
        self.transient()
        self.grab_set()
        self.focus_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.labelTitle = customtkinter.CTkLabel(self, text="Iniciar sesión", anchor="w", font=("Arial Bold", 24))
        self.labelTitle.grid(row=0, column=0, columnspan=3, pady=(50, 20), sticky="n")
        
        # ----- FORM FRAME / INICIO DE SESIÓN -----
        self.frameEmail = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frameEmail.grid(row=1, column=0, columnspan=3, pady=10, sticky="n")

        self.labelEmail = customtkinter.CTkLabel(self.frameEmail, text="Email:", font=("Arial", 14), anchor="w")
        self.labelEmail.grid(row=0, column=0, sticky="w")
        self.entryEmail = customtkinter.CTkEntry(self.frameEmail, width=200, fg_color="#EEEEEE", border_width=1, text_color="#000000")
        self.entryEmail.grid(row=1, column=0, pady=(5, 0), sticky="w")

        self.labelcontrasenia = customtkinter.CTkLabel(self.frameEmail, text="Contraseña:", font=("Arial", 14), anchor="w")
        self.labelcontrasenia.grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.entrycontrasenia = customtkinter.CTkEntry(self.frameEmail, width=200, fg_color="#EEEEEE", border_width=1, text_color="#000000")
        self.entrycontrasenia.grid(row=3, column=0, pady=(5, 0), sticky="w")
        
        # ----- BOTONES -----
        self.btnIngresar = customtkinter.CTkButton(self, text="Ingresar", font=("Arial Bold", 12), text_color="#ffffff", width=200)
        self.btnIngresar.grid(row=2, column=0, columnspan=3, pady=(20, 0), padx=(0, 0))

        self.btnVisualizar = customtkinter.CTkButton(self, text="Solo visualizar registros", width=200, command=lambda : solo_visualizar(self))
        self.btnVisualizar.grid(row=3, column=0, columnspan=3, pady=(10, 0), padx= 0)

        def solo_visualizar(self):
            self.destroy()
            vizualizar_registros = UserVisualizador()
            vizualizar_registros.mainloop()

if __name__ == '__main__':
    app = IndexWindow()
    app.mainloop()