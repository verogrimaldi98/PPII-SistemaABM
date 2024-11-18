import customtkinter
from index import User
from PIL import Image
import sqlite3

db_name = 'database.db'

class FormularioBase(customtkinter.CTkToplevel):
    def __init__(self, parent, titulo, valores_iniciales=None):
        super().__init__(parent)
        
        self.title("Nuevo registro")
        self.geometry("490x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.grid_columnconfigure(0, weight=1)

        self.valores_iniciales = valores_iniciales or {}

        self.configurar_frames()
        self.rellenar_formulario()
    def configurar_frames(self):
        # ----- FRAME TITULO -----
        self.title_frame = customtkinter.CTkFrame(self)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="new")
        self.label_frame = customtkinter.CTkLabel(self.title_frame, text="Ingresar datos:", font=("Arial", 16))
        self.label_frame.pack(fill="both", expand=True, anchor="center")

        # ----- FRAME TITULO FORMULARIO -----
        self.frame_formulario = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame_formulario.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="sew")

        # Registro de la función de validación para números
        vcmd = (self.register(self.solo_numero), "%P")

        self.crear_entradas_formulario(vcmd)

        # ----- FRAME BOTONES -----
        self.btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=6, column=0, columnspan=2, padx=60, pady=(10, 10), sticky="nsew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        self.btn_frame.grid_columnconfigure(2, weight=1)

        trash_icon = customtkinter.CTkImage(Image.open("img/delete-icon.png"), size=(25, 25))
        self.btn_limpiar = customtkinter.CTkButton(self.btn_frame, text="", image=trash_icon, fg_color="transparent", hover=False, width=20, command=self.limpiar_formulario)
        self.btn_limpiar.grid(row=0, column=0, padx=(0, 5))

        self.btn_guardar = customtkinter.CTkButton(self.btn_frame, text="Guardar", fg_color="#05ab08", hover_color="#09820d", command=self.guardar_datos)
        self.btn_guardar.grid(row=0, column=1, padx=5)
        self.btn_cancelar = customtkinter.CTkButton(self.btn_frame, text="Cancelar", command=self.destroy)
        self.btn_cancelar.grid(row=0, column=2, padx=(5, 0))

    def guardar_datos(self):

        raise NotImplementedError("Subclases deben implementar el método de guardado")

    def crear_entradas_formulario(self, vcmd):
        # ----- ROW 1 (NOMBRE Y APELLIDO) -----
        self.label_nombre = customtkinter.CTkLabel(self.frame_formulario, text="Nombre:")
        self.label_nombre.grid(row=1, column=0, padx=(20, 10), pady=(10, 0))
        self.entry_nombre = customtkinter.CTkEntry(self.frame_formulario)
        self.entry_nombre.grid(row=1, column=1, pady=(10, 0))

        self.label_apellido = customtkinter.CTkLabel(self.frame_formulario, text="Apellido:")
        self.label_apellido.grid(row=1, column=2, padx=10, pady=(10, 0))
        self.entry_apellido = customtkinter.CTkEntry(self.frame_formulario)
        self.entry_apellido.grid(row=1, column=3, padx=(0, 20), pady=(10, 0))

        # ----- ROW 2 (DNI Y EDAD) -----
        self.label_dni = customtkinter.CTkLabel(self.frame_formulario, text="DNI:")
        self.label_dni.grid(row=2, column=0, pady=(10, 0))
        self.entry_dni = customtkinter.CTkEntry(self.frame_formulario, validate="key", validatecommand=vcmd)
        self.entry_dni.grid(row=2, column=1, pady=(10, 0))

        self.label_telefono = customtkinter.CTkLabel(self.frame_formulario, text="Teléfono:")
        self.label_telefono.grid(row=2, column=2, pady=(10, 0))
        self.entry_telefono = customtkinter.CTkEntry(self.frame_formulario, validate="key", validatecommand=vcmd)
        self.entry_telefono.grid(row=2, column=3, padx=(0, 20), pady=(10, 0))

        # ----- ROW 3 (TELEFONO Y GENERO) -----
        opciones_genero = self.obtener_opciones("generos", "nombre")
        self.label_genero = customtkinter.CTkLabel(self.frame_formulario, text="Genero:")
        self.label_genero.grid(row=3, column=0, pady=10)
        self.box_genero = customtkinter.CTkComboBox(self.frame_formulario, values=list(opciones_genero.keys()), state="readonly")
        self.box_genero.grid(row=3, column=1, pady=10)
        self.box_genero.set("Seleccionar")

        self.label_edad = customtkinter.CTkLabel(self.frame_formulario, text="Edad:")
        self.label_edad.grid(row=3, column=2, pady=10)
        self.entry_edad = customtkinter.CTkEntry(self.frame_formulario, validate="key", validatecommand=vcmd)
        self.entry_edad.grid(row=3, column=3, padx=(0, 20), pady=10)

        # ----- ROW 4 (INSTITUTO) -----
        opciones_provincia = self.obtener_opciones("provincias", "nombre")
        self.label_provincia = customtkinter.CTkLabel(self.frame_formulario, text="Provincia:")
        self.label_provincia.grid(row=4, column=0, pady=0)
        self.box_provincia = customtkinter.CTkComboBox(self.frame_formulario, values=list(opciones_provincia.keys()), state="readonly")
        self.box_provincia.grid(row=4, column=1)
        self.box_provincia.set("Seleccionar")

        opciones_institucion = self.obtener_opciones("instituciones", "nombre")
        self.label_institucion = customtkinter.CTkLabel(self.frame_formulario, text="Instituto:")
        self.label_institucion.grid(row=4, column=2, padx=(20, 10), pady=0)
        self.box_institucion = customtkinter.CTkComboBox(self.frame_formulario, values=list(opciones_institucion.keys()), state="readonly")
        self.box_institucion.grid(row=4, column=3, padx=(0, 20))
        self.box_institucion.set("Seleccionar")

        # ----- ROW 5 (TIPO) -----
        opciones_tipo = self.obtener_opciones("tipo", "nombre")
        self.label_tipo = customtkinter.CTkLabel(self.frame_formulario, text="Tipo:")
        self.label_tipo.grid(row=6, column=0, padx=(20, 10), pady=(0, 10))
        self.box_tipo = customtkinter.CTkComboBox(self.frame_formulario, values=list(opciones_tipo.keys()), state="readonly", command=self.elegir_tipo)
        self.box_tipo.grid(row=6, column=1, pady=(0, 10))
        self.box_tipo.set("Seleccionar")

        self.label_estado = customtkinter.CTkLabel(self.frame_formulario, text="Estado:")
        self.label_estado.grid(row=5, column=0, padx=(20, 10), pady=10)

        self.box_tipo.bind("<<ComboboxSelected>>", lambda event: self.elegir_tipo(self.box_tipo.get()))
    
    def elegir_tipo(self, selection):
        if selection == "Órgano":
            opciones = self.obtener_opciones("organos", "nombre")
        elif selection == "Tejido":
            opciones = self.obtener_opciones("tejidos", "nombre")
        else:
            opciones = []

        if hasattr(self, "box_elemento") and hasattr(self, "label_elemento"):
            self.box_elemento.configure(values=list(opciones.keys()))
            self.box_elemento.set("Seleccionar")
        else:
            self.label_elemento = customtkinter.CTkLabel(self.frame_formulario, text="Elem:")
            self.label_elemento.grid(row=6, column=2, padx=(20, 10), pady=(0, 10))

            self.box_elemento = customtkinter.CTkComboBox(self.frame_formulario, values=list(opciones.keys()), state="readonly")
            self.box_elemento.grid(row=6, column=3, padx=(0, 20), pady=(0, 10))
            self.box_elemento.set("Seleccionar")

    def obtener_opciones(self, tabla, columna):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, {columna} FROM {tabla}")
        opciones = cursor.fetchall()
        conn.close()
        return {nombre: id_ for id_, nombre in opciones}

    def solo_numero(self, texto):
        return texto.isdigit() or texto == ""

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_apellido.delete(0, "end")
        self.entry_dni.delete(0, "end")
        self.entry_edad.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.box_genero.set("Seleccionar")
        self.box_provincia.set("Seleccionar")
        self.box_estado.set("Seleccionar")
        self.box_institucion.set("Seleccionar")
        self.box_tipo.set("Seleccionar")
        self.box_elemento.set("Seleccionar")

    def rellenar_formulario(self):
        if "nombre" in self.valores_iniciales:
            self.entry_nombre.insert(0, self.valores_iniciales["nombre"])
        if "apellido" in self.valores_iniciales:
            self.entry_apellido.insert(0, self.valores_iniciales["apellido"])
        if "dni" in self.valores_iniciales:
            self.entry_dni.insert(0, self.valores_iniciales["dni"])
        if "edad" in self.valores_iniciales:
            self.entry_edad.insert(0, self.valores_iniciales["edad"])
        if "telefono" in self.valores_iniciales:
            self.entry_telefono.insert(0, self.valores_iniciales["telefono"])
        if "genero_id" in self.valores_iniciales:
            self.box_genero.set(self.valores_iniciales["genero_id"])
        if "provincia_id" in self.valores_iniciales:
            self.box_provincia.set(self.valores_iniciales["provincia_id"])
        if "estado_id" in self.valores_iniciales:
            self.box_estado.set(self.valores_iniciales["estado_id"])
        if "institucion_id" in self.valores_iniciales:
            self.box_institucion.set(self.valores_iniciales["institucion_id"])
        if "tipo_id" in self.valores_iniciales:
            self.box_tipo.set(self.valores_iniciales["tipo_id"])
        if "elemento_id" in self.valores_iniciales:
            self.box_elemento.set(self.valores_iniciales["elemento_id"])

class FormularioDonador(FormularioBase):
    def __init__(self, parent, valores_iniciales=None):
        super().__init__(parent, "Agregar Donador", valores_iniciales)
        self.btn_guardar.configure(command=self.guardar_donantes)
        
        self.opciones_estadoDonador = self.obtener_opciones("estadoDonadores", "nombre")
        self.box_estado = customtkinter.CTkComboBox(self.frame_formulario, values=list(self.opciones_estadoDonador.keys()), state="readonly")
        self.box_estado.grid(row=5, column=1, pady=10)
        self.box_estado.set("Seleccionar")
        
        self.label_elemento = customtkinter.CTkLabel(self.frame_formulario, text="Elem:")
        self.label_elemento.grid(row=6, column=2, padx=(20, 10), pady=(0, 10))
        self.box_elemento = customtkinter.CTkComboBox(self.frame_formulario, values=[], state="readonly")
        self.box_elemento.grid(row=6, column=3, padx=(0, 20), pady=(0, 10))
        self.box_elemento.set("Seleccionar")

    def guardar_donantes(self):
        opciones_dict = {
            "genero": self.obtener_opciones("generos", "nombre"),
            "provincia": self.obtener_opciones("provincias", "nombre"),
            "institucion": self.obtener_opciones("instituciones", "nombre"),
            "tipo": self.obtener_opciones("tipo", "nombre"),
            "estado": self.opciones_estadoDonador
        }
        if self.box_tipo.get() == "Órgano":
            opciones_dict["elemento"] = self.obtener_opciones("organos", "nombre")
        elif self.box_tipo.get() == "Tejido":
            opciones_dict["elemento"] = self.obtener_opciones("tejidos", "nombre")

        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        dni = self.entry_dni.get()
        edad = self.entry_edad.get()
        genero = opciones_dict["genero"][self.box_genero.get()]
        telefono = self.entry_telefono.get()
        provincia = opciones_dict["provincia"][self.box_provincia.get()]
        estado = opciones_dict["estado"][self.box_estado.get()]
        institucion = opciones_dict["institucion"][self.box_institucion.get()]
        tipo = opciones_dict["tipo"][self.box_tipo.get()]
        elemento = opciones_dict["elemento"].get(self.box_elemento.get(), None)

        if elemento is None:
            print(f"Error: '{self.box_elemento.get()}' no encontrado en opciones_dict['elemento']")
            return

        query = """
            INSERT INTO donantes 
            (nombre, apellido, dni, edad, genero_id, telefono, provincia_id, estado_id, institucion_id, tipo_id, elemento_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (nombre, apellido, dni, edad, genero, telefono, provincia, estado, institucion, tipo, elemento)
        self.run_query(query, parameters)
        self.destroy()
        print("Datos guardados.")

class FormularioReceptor(FormularioBase):
    def __init__(self, parent, valores_iniciales=None):
        super().__init__(parent, "Agregar Receptor", valores_iniciales)
        self.btn_guardar.configure(command=self.guardar_receptores)

        self.opciones_estadoReceptor = self.obtener_opciones("estadoReceptores", "nombre")
        self.box_estado = customtkinter.CTkComboBox(self.frame_formulario, values=list(self.opciones_estadoReceptor.keys()), state="readonly")
        self.box_estado.grid(row=5, column=1, pady=10)
        self.box_estado.set("Seleccionar")

        self.label_elemento = customtkinter.CTkLabel(self.frame_formulario, text="Elem:")
        self.label_elemento.grid(row=6, column=2, padx=(20, 10), pady=(0, 10))
        self.box_elemento = customtkinter.CTkComboBox(self.frame_formulario, values=[], state="readonly")
        self.box_elemento.grid(row=6, column=3, padx=(0, 20), pady=(0, 10))
        self.box_elemento.set("Seleccionar")

    def guardar_receptores(self):
        opciones_dict = {
            "genero": self.obtener_opciones("generos", "nombre"),
            "provincia": self.obtener_opciones("provincias", "nombre"),
            "institucion": self.obtener_opciones("instituciones", "nombre"),
            "tipo": self.obtener_opciones("tipo", "nombre"),
            "estado": self.opciones_estadoReceptor
        }
        if self.box_tipo.get() == "Órgano":
            opciones_dict["elemento"] = self.obtener_opciones("organos", "nombre")
        elif self.box_tipo.get() == "Tejido":
            opciones_dict["elemento"] = self.obtener_opciones("tejidos", "nombre")

        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        dni = self.entry_dni.get()
        edad = self.entry_edad.get()
        genero = opciones_dict["genero"][self.box_genero.get()]
        telefono = self.entry_telefono.get()
        provincia = opciones_dict["provincia"][self.box_provincia.get()]
        estado = opciones_dict["estado"][self.box_estado.get()]
        institucion = opciones_dict["institucion"][self.box_institucion.get()]
        tipo = opciones_dict["tipo"][self.box_tipo.get()]
        elemento = opciones_dict["elemento"].get(self.box_elemento.get(), None)

        if elemento is None:
            print(f"Error: '{self.box_elemento.get()}' no encontrado en opciones_dict['elemento']")
            return

        query = """
            INSERT INTO receptores 
            (nombre, apellido, dni, edad, genero_id, telefono, provincia_id, estado_id, institucion_id, tipo_id, elemento_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (nombre, apellido, dni, edad, genero, telefono, provincia, estado, institucion, tipo, elemento)
        self.run_query(query, parameters)
        self.limpiar_formulario()
        self.destroy()
        print("Datos guardados.")