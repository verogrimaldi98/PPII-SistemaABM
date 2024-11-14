import customtkinter
from tkinter import ttk
from forms import *
import sqlite3

class User(customtkinter.CTk):
    db_name = 'database.db'  
    def __init__(self):
        super().__init__()

        self.title('Vizualización de registros')
        customtkinter.set_appearance_mode("light")
        self.geometry("1280x720")

        # ----- TITULO -----
        self.main_title = None

        # ----- PESTAÑAS -----
        self.tab_view = customtkinter.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_view.add("Donantes")
        self.tab_view.add("Receptores")

        self.setup_treeview(self.tab_view.tab("Donantes"), "Donantes")
        self.setup_treeview(self.tab_view.tab("Receptores"), "Receptores")

    def setup_treeview(self, parent_frame, tipo_dato):
        frameCampos = customtkinter.CTkFrame(parent_frame, fg_color="white")
        frameCampos.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="nsew")
        
        parent_frame.grid_rowconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(0, weight=1)
        frameCampos.grid_rowconfigure(0, weight=1)
        frameCampos.grid_columnconfigure(0, weight=1)

        encabezados = ["Id", "Nombre", "Apellido", "DNI", "Edad", "Género", "Teléfono", "Provincia", "Estado", "Institución", "Tipo", "Elemento"]

        tree_view = ttk.Treeview(frameCampos, columns=encabezados, show="headings")
        tree_view.pack(fill="both", expand=True)
        
        for encabezado in encabezados:
            tree_view.heading(encabezado, text=encabezado)
            tree_view.column(encabezado, anchor="center", width=80, stretch=True)
        
        tree_view.grid(row=0, column=0, sticky="nsew")

        if tipo_dato == "Donantes":
            self.tree_view_donadores = tree_view
            query = ''' SELECT donantes.id, donantes.nombre, donantes.apellido, donantes.dni, donantes.edad, generos.nombre, donantes.telefono, provincias.nombre, estadoDonadores.nombre, instituciones.nombre, tipo.nombre, donantes.elemento_id FROM donantes JOIN generos ON donantes.genero_id = generos.id JOIN provincias ON donantes.provincia_id = provincias.id JOIN estadoDonadores ON donantes.estado_id = estadoDonadores.id JOIN instituciones ON donantes.institucion_id = instituciones.id JOIN tipo ON donantes.tipo_id = tipo.id  '''
            self.get_datos(tree_view, query)
        elif tipo_dato == "Receptores":
            self.tree_view_receptores = tree_view
            query = ''' SELECT receptores.id, receptores.nombre, receptores.apellido, receptores.dni, receptores.edad, generos.nombre, receptores.telefono, provincias.nombre, estadoReceptores.nombre, instituciones.nombre, tipo.nombre, receptores.elemento_id FROM receptores JOIN generos ON receptores.genero_id = generos.id JOIN provincias ON receptores.provincia_id = provincias.id JOIN estadoReceptores ON receptores.estado_id = estadoReceptores.id JOIN instituciones ON receptores.institucion_id = instituciones.id JOIN tipo ON receptores.tipo_id = tipo.id  '''
            self.get_datos(tree_view, query)
    
    def get_datos(self, tree_view, query):
        registros = tree_view.get_children()
        for registro in registros:
            tree_view.delete(registro)
            
        db_rows = self.run_query(query)
        for row in db_rows:
            tree_view.insert("", "end", values=row)
    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
class UserAdmin(User):
    def __init__(self):
        super().__init__()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ----- TITULO ADMIN -----
        self.main_title = customtkinter.CTkLabel(self, text="Administrador", font=("Arial", 20))
        self.main_title.grid(row= 0, column= 0, padx=10, pady=(10, 0))

        # ----- FRAME BOTONES LATERALES -----
        self.menu_frame = customtkinter.CTkFrame(self)
        self.menu_frame.grid(row=1, column=0, padx=(20, 0), pady=(17, 20), sticky="nsw")
        self.addBtnDonador = customtkinter.CTkButton(self.menu_frame, text="Agregar donador", fg_color="#05ab08", hover_color="#09820d", command= self.abrir_formulario_donador)
        self.addBtnDonador.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.addBtnReceptor = customtkinter.CTkButton(self.menu_frame, text="Agregar receptor", fg_color="#05ab08", hover_color="#09820d", command=self.abrir_formulario_receptor)
        self.addBtnReceptor.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.editBtn = customtkinter.CTkButton(self.menu_frame, text="Editar registro")
        self.editBtn.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.deleteBtn = customtkinter.CTkButton(self.menu_frame, text="Eliminar registro", fg_color="#e01f1f", hover_color="#9c1818")
        self.deleteBtn.grid(row=3, column=0, padx=10, pady=(10, 0))

        # ----- POSICION DE PESTAÑAS -----
        self.tab_view.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady= (0, 20))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def abrir_formulario_donador(self):
        FormularioDonador(self)

    def abrir_formulario_receptor(self):
        FormularioReceptor(self)

class UserAltas(User):
    def __init__(self):
        super().__init__()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ----- TITULO USUARIO DE ALTAS -----
        self.main_title = customtkinter.CTkLabel(self, text="Usuario de Altas", font=("Arial", 20))
        self.main_title.grid(row= 0, column= 0, padx=10, pady=(10, 0))

        # ----- FRAME BOTONES LATERALES -----
        self.menu_frame = customtkinter.CTkFrame(self)
        self.menu_frame.grid(row=1, column=0, padx=(20, 0), pady=(17, 20), sticky="nsw")
        self.addBtnDonador = customtkinter.CTkButton(self.menu_frame, text="Agregar donador", fg_color="#05ab08", hover_color="#09820d", command=self.abrir_formulario_donador)
        self.addBtnDonador.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.addBtnReceptor = customtkinter.CTkButton(self.menu_frame, text="Agregar receptor", fg_color="#05ab08", hover_color="#09820d", command=self.abrir_formulario_receptor)
        self.addBtnReceptor.grid(row=1, column=0, padx=10, pady=(10, 0))

        # ----- POSICION DE PESTAÑAS -----
        self.tab_view.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady= (0, 20))
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def abrir_formulario_donador(self):
        FormularioDonador(self)

    def abrir_formulario_receptor(self):
        FormularioReceptor(self)

class UserVisualizador(User):
    def __init__(self):
        super().__init__()

        self.main_title = customtkinter.CTkLabel(self, text="Visualizador de registros", font=("Arial", 20))
        self.main_title.grid(row= 0, column= 0, padx=10, pady=(10, 0))

if __name__ == '__main__':
    app = UserAdmin()
    app.mainloop()