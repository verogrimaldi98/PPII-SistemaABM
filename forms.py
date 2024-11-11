import customtkinter
import sqlite3

class FormularioBase(customtkinter.CTkToplevel):
    db_name = 'database.db'
    def __init__(self, parent, titulo):
        super().__init__(parent)
        
        self.title("Nuevo registro")
        self.geometry("490x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.grid_columnconfigure(0, weight=1)

        self.configurar_frames()

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
        self.crear_combobox_estado()

        # ----- FRAME BOTONES -----
        self.btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=6, column=0, columnspan=2, padx=60, pady=(20, 10), sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)

        self.btn_guardar = customtkinter.CTkButton(self.btn_frame, text="Guardar", command=self.guardar_datos)
        self.btn_guardar.grid(row=0, column=0)
        self.btn_cancelar = customtkinter.CTkButton(self.btn_frame, text="Cancelar", command=self.destroy)
        self.btn_cancelar.grid(row=0, column=1)

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
        self.box_genero = customtkinter.CTkComboBox(self.frame_formulario, values=opciones_genero)
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
        self.box_provincia = customtkinter.CTkComboBox(self.frame_formulario, values=opciones_provincia)
        self.box_provincia.grid(row=4, column=1)
        self.box_provincia.set("Seleccionar")

        opciones_institucion = self.obtener_opciones("instituciones", "nombre")
        self.label_institucion = customtkinter.CTkLabel(self.frame_formulario, text="Instituto:")
        self.label_institucion.grid(row=4, column=2, padx=(20, 10), pady=0)
        self.box_institucion = customtkinter.CTkComboBox(self.frame_formulario, values=opciones_institucion)
        self.box_institucion.grid(row=4, column=3, padx=(0, 20))
        self.box_institucion.set("Seleccionar")

        # ----- ROW 5 (TIPO) -----
        opciones_tipo = self.obtener_opciones("tipo", "nombre")
        self.label_tipo = customtkinter.CTkLabel(self.frame_formulario, text="Tipo:")
        self.label_tipo.grid(row=6, column=0, padx=(20, 10), pady=(0, 10))
        self.box_tipo = customtkinter.CTkComboBox(self.frame_formulario, values=opciones_tipo, command=self.elegir_tipo)
        self.box_tipo.grid(row=6, column=1, pady=(0, 10))
        self.box_tipo.set("Seleccionar")

    def elegir_tipo(self, selection):
        if selection == "Órgano":
            opciones = self.obtener_opciones("organos", "nombre")
        elif selection == "Tejido":
            opciones = self.obtener_opciones("tejidos", "nombre")
        else:
            opciones = []

        if opciones:
            self.box_elemento = customtkinter.CTkComboBox(
                self.frame_formulario, 
                values=opciones)
            self.label_elemento = customtkinter.CTkLabel(self.frame_formulario, text="Elem:")
            self.label_elemento.grid(row=6, column=2, padx=(20, 10), pady=(0, 10))
            self.box_elemento.grid(row=6, column=3, padx=(0, 20), pady=(0, 10))
            self.box_elemento.set("Seleccionar")

    def crear_combobox_estado(self):
        raise NotImplementedError("Subclases deben implementar 'crear_combobox_estado'")

    def obtener_opciones(self, tabla, columna):
        query = f"SELECT {columna} FROM {tabla}"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            opciones = [fila[0] for fila in resultados]
        return opciones

    def solo_numero(self, texto):
        return texto.isdigit() or texto == ""

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()

class FormularioDonador(FormularioBase):
    def __init__(self, parent):
        super().__init__(parent, "Agregar Donador")
        self.btn_guardar.configure(command=self.guardar_donador)

    def crear_combobox_estado(self):
        self.opciones_estadoDonador = self.obtener_opciones("estadoDonadores", "nombre")
        self.label_estado = customtkinter.CTkLabel(self.frame_formulario, text="Estado:")
        self.label_estado.grid(row=5, column=0, padx=(20, 10), pady=10)
        self.box_estado = customtkinter.CTkComboBox(self.frame_formulario, values=self.opciones_estadoDonador)
        self.box_estado.grid(row=5, column=1, pady=10)
        self.box_estado.set("Seleccionar")

    def guardar_donador(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        dni = self.entry_dni.get()
        edad = self.entry_edad.get()
        genero = self.box_genero.get()
        telefono = self.entry_telefono.get()
        provincia = self.box_provincia.get()
        estado = self.box_estado.get()
        institucion = self.box_institucion.get()
        tipo = self.box_tipo.get()
        elemento = self.box_elemento.get()
        query = "INSERT INTO donadores (nombre, apellido, dni, edad, genero_id, telefono, provincia_id, estado_id, institucion_id, tipo_id, elemento_id) "
        parameters = nombre, apellido, dni, edad, genero, telefono, provincia, estado, institucion, tipo, elemento
        self.run_query(query, parameters)
        print("datos guardador")

class FormularioReceptor(FormularioBase):
    def __init__(self, parent):
        super().__init__(parent, "Agregar Receptor")

    def crear_combobox_estado(self):
        opciones_estadoReceptor = self.obtener_opciones("estadoReceptores", "nombre")
        self.label_estado = customtkinter.CTkLabel(self.frame_formulario, text="Estado:")
        self.label_estado.grid(row=5, column=0, padx=(20, 10), pady=10)
        self.box_estado = customtkinter.CTkComboBox(self.frame_formulario, values=opciones_estadoReceptor)
        self.box_estado.grid(row=5, column=1, pady=10)
        self.box_estado.set("Seleccionar")