import customtkinter
from tkinter import ttk
from forms import *
from PIL import Image
import sqlite3

db_name = 'database.db'  

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
        self.entrycontrasenia = customtkinter.CTkEntry(self.frameEmail, width=200, fg_color="#EEEEEE", border_width=1, text_color="#000000", show="*")
        self.entrycontrasenia.grid(row=3, column=0, pady=(5, 0), sticky="w")
        
        # ----- BOTONES -----
        self.btnIngresar = customtkinter.CTkButton(self, text="Ingresar", font=("Arial Bold", 12), text_color="#ffffff", width=200, command=self.iniciar_sesion)
        self.btnIngresar.grid(row=2, column=0, columnspan=3, pady=(20, 0), padx=(0, 0))

        self.btnVisualizar = customtkinter.CTkButton(self, text="Solo visualizar registros", width=200, command=lambda : self.solo_visualizar())
        self.btnVisualizar.grid(row=3, column=0, columnspan=3, pady=(10, 0), padx= 0)

    def solo_visualizar(self):
        self.destroy()
        vizualizar_registros = UserVisualizador()
        vizualizar_registros.mainloop()

    def validar_formulario(self):
            """Valida que los campos no estén vacíos."""
            return len(self.entryEmail.get()) > 0 and len(self.entrycontrasenia.get()) > 0

    def iniciar_sesion(self):
        if not self.validar_formulario():
            print("Por favor, completa todos los campos.")
            return

        nombre_usuario = self.entryEmail.get()
        contrasenia = self.entrycontrasenia.get()

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT usuarios.nombre_usuario, roles.nombre
            FROM usuarios
            JOIN roles ON usuarios.rol_id = roles.id
            WHERE usuarios.nombre_usuario = ? AND usuarios.contrasenia = ?
        """, (nombre_usuario, contrasenia))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            usuario, rol = resultado
            print(f"Inicio de sesión exitoso para {usuario} con rol {rol}.")
            if rol == "admin":
                self.destroy()
                admin_window = UserAdmin(usuario)
                admin_window.mainloop()
            elif rol == "altas":
                self.destroy()
                altas_window = UserAltas(usuario)
                altas_window.mainloop()
            else:
                print(f"Rol incorrecto: {rol}")
        else:
            print("Datos incorrectas.")

class User(customtkinter.CTk):
    def __init__(self, nombre_usuario, rol):
        super().__init__()
        self.nombre_usuario = nombre_usuario
        self.rol = rol

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
        frameCampos.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
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
        elif tipo_dato == "Receptores":
            self.tree_view_receptores = tree_view

        self.get_datos(tree_view, tipo_dato)
    
    def get_datos(self, tree_view, tipo_dato):
        registros = tree_view.get_children()
        for registro in registros:
            tree_view.delete(registro)
            
        if tipo_dato == "Donantes":
            query = '''
                SELECT donantes.id, donantes.nombre, donantes.apellido, donantes.dni, donantes.edad, generos.nombre, 
                    donantes.telefono, provincias.nombre, estadoDonadores.nombre, instituciones.nombre, 
                    tipo.nombre, donantes.elemento_id 
                FROM donantes 
                JOIN generos ON donantes.genero_id = generos.id 
                JOIN provincias ON donantes.provincia_id = provincias.id 
                JOIN estadoDonadores ON donantes.estado_id = estadoDonadores.id 
                JOIN instituciones ON donantes.institucion_id = instituciones.id 
                JOIN tipo ON donantes.tipo_id = tipo.id
            '''
        elif tipo_dato == "Receptores":
            query = '''
                SELECT receptores.id, receptores.nombre, receptores.apellido, receptores.dni, receptores.edad, generos.nombre, 
                    receptores.telefono, provincias.nombre, estadoReceptores.nombre, instituciones.nombre, 
                    tipo.nombre, receptores.elemento_id 
                FROM receptores 
                JOIN generos ON receptores.genero_id = generos.id 
                JOIN provincias ON receptores.provincia_id = provincias.id 
                JOIN estadoReceptores ON receptores.estado_id = estadoReceptores.id 
                JOIN instituciones ON receptores.institucion_id = instituciones.id 
                JOIN tipo ON receptores.tipo_id = tipo.id
            '''

        db_rows = self.run_query(query)
        for row in db_rows:
            tree_view.insert("", "end", values=row)
    
    def eliminar_registro(self):
        current_tab = self.tab_view.get()

        tree_view = self.tree_view_donadores if current_tab == "Donantes" else self.tree_view_receptores
        tipo_dato = current_tab

        try:
            selected_items = tree_view.selection()
            if not selected_items:
                raise IndexError("Seleccione un registro para eliminar.")
        except IndexError as e:
            print(e)
            return

        for selected_item in selected_items:
            item_values = tree_view.item(selected_item, "values")
            if not item_values:
                print("El registro seleccionado no tiene valores.")
                continue

            id_registro = item_values[0]
            
            if tipo_dato == "Donantes":
                query = "DELETE FROM donantes WHERE id = ?"
            elif tipo_dato == "Receptores":
                query = "DELETE FROM receptores WHERE id = ?"

            self.run_query(query, (id_registro,))
            tree_view.delete(selected_item)
            print(f"Registro {id_registro} eliminado correctamente.")
          
    def actulizar_registros(self):
        current_tab = self.tab_view.get()
        tree_view = self.tree_view_donadores if current_tab == "Donantes" else self.tree_view_receptores
        tipo_dato = current_tab

        self.get_datos(tree_view, tipo_dato)

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
class UserAdmin(User):
    def __init__(self, nombre_usuario):
        super().__init__(nombre_usuario, rol="admin")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ----- TITULO ADMIN -----
        self.main_title = customtkinter.CTkLabel(self, text="Administrador", font=("Arial", 20))
        self.main_title.grid(row=0, column=0, padx=(30, 10), pady=(10, 0), sticky="w")

        update_icon = customtkinter.CTkImage(Image.open("img/update-icon.png"), size=(30, 30))
        self.update_Btn = customtkinter.CTkButton(self, text="", image=update_icon, fg_color="transparent", hover=False, width=30, command=self.actulizar_registros)
        self.update_Btn.grid(row=0, column=1, columnspan=2, sticky="e", padx=(0, 30), pady=(20, 0))

        # ----- FRAME BOTONES LATERALES -----
        self.menu_frame = customtkinter.CTkFrame(self)
        self.menu_frame.grid(row=1, column=0, padx=(20, 0), pady=(17, 20), sticky="nsw")
        self.addBtnDonador = customtkinter.CTkButton(self.menu_frame, text="Agregar donador", fg_color="#05ab08", hover_color="#09820d", command= self.abrir_formulario_donador)
        self.addBtnDonador.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.addBtnReceptor = customtkinter.CTkButton(self.menu_frame, text="Agregar receptor", fg_color="#05ab08", hover_color="#09820d", command=self.abrir_formulario_receptor)
        self.addBtnReceptor.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.editBtn = customtkinter.CTkButton(self.menu_frame, text="Editar registro", fg_color="#36a4b8", hover_color="#197f92")
        self.editBtn.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.deleteBtn = customtkinter.CTkButton(self.menu_frame, text="Eliminar registro", fg_color="#e01f1f", hover_color="#9c1818", command= self.eliminar_registro)
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
    def __init__(self, nombre_usuario):
        super().__init__(nombre_usuario, rol="altas")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ----- TITULO USUARIO DE ALTAS -----
        self.main_title = customtkinter.CTkLabel(self, text="Dar altas", font=("Arial", 20))
        self.main_title.grid(row=0, column=0, padx=(30, 10), pady=(10, 0), sticky="w")

        update_icon = customtkinter.CTkImage(Image.open("img/update-icon.png"), size=(30, 30))
        self.update_Btn = customtkinter.CTkButton(self, text="", image=update_icon, fg_color="transparent", hover=False, width=30, command=self.actulizar_registros)
        self.update_Btn.grid(row=0, column=1, columnspan=2, sticky="e", padx=(0, 30), pady=(20, 0))

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
        super().__init__(nombre_usuario=None, rol=None)

        self.main_title = customtkinter.CTkLabel(self, text="Visualizador de registros", font=("Arial", 20))
        self.main_title.grid(row=0, column=0, padx=10, pady=(10, 0))

if __name__ == '__main__':
    app = IndexWindow()
    app.mainloop()