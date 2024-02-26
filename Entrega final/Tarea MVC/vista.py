from tkinter import *
from tkinter import ttk, messagebox
from modelo import Modelo

class Vista:
    """
    Clase que maneja la interfaz de usuario.

    Attributes:
        root: El widget principal de la aplicación.
        modelo: Una instancia del modelo de la aplicación.
        a_val (StringVar): Variable de control para el campo de entrada de nombre.
        b_val (StringVar): Variable de control para el campo de entrada de apellido.
        c_val (StringVar): Variable de control para el campo de entrada de plan.
        d_val (DoubleVar): Variable de control para el campo de entrada de precio.
        entrada1 (Entry): Campo de entrada para el nombre del cliente.
        entrada2 (Entry): Campo de entrada para el apellido del cliente.
        combo_plan (ttk.Combobox): Cuadro de selección para el plan del cliente.
        label_precio_valor (Label): Etiqueta para mostrar el precio del plan seleccionado.
        boton_alta (Button): Botón para agregar un nuevo cliente.
        boton_borrar (Button): Botón para borrar un cliente seleccionado.
        tree (ttk.Treeview): Vista de árbol para mostrar la lista de clientes.
    """

    def __init__(self, root):
        """
        Constructor de la clase Vista.

        Args:
            root: El widget principal de la aplicación.
        """
        self.root = root
        self.root.title("📡 InterSat4 - Sistema para Registrar Clientes de Internet 📡")
        self.root.geometry("800x400")
        self.modelo = Modelo()

        self.titulo = Label(self.root, text="Plantilla de clientes - Ingrese los datos", font=("Arial", 16, "bold"))
        self.titulo.grid(row=0, column=0, columnspan=6, pady=(10, 10), sticky="we")

        # Variables de control
        self.a_val = StringVar()
        self.b_val = StringVar()
        self.c_val = StringVar()
        self.d_val = DoubleVar()

        # Crear filas de entrada
        self.entrada1 = self.crear_fila_entrada(1, "Nombre", self.a_val, 30)
        self.entrada2 = self.crear_fila_entrada(2, "Apellido", self.b_val, 30)

        # Label y Combobox para Plan y Precio
        self.label_plan = Label(self.root, text="Plan", bg="black", fg="white")
        self.label_plan.grid(row=3, column=0, sticky=W)
        self.combo_plan = ttk.Combobox(self.root, width=27, state="readonly", values=["Basico", "Medio", "Premium", "Especial"])
        self.combo_plan.grid(row=3, column=1, columnspan=2, sticky=W)
        self.combo_plan.bind("<<ComboboxSelected>>", self.callback)

        self.label_precio = Label(self.root, text="Precio", bg="black", fg="white")
        self.label_precio.grid(row=4, column=0, sticky=W)
        self.label_precio_valor = Label(self.root, text="0.0", bg="black", fg="white")
        self.label_precio_valor.grid(row=4, column=1, sticky=W)

        # Botones
        self.boton_alta = Button(self.root, text="Alta", command=self.alta_cliente)
        self.boton_alta.grid(row=6, column=1)

        self.boton_borrar = Button(self.root, text="Borrar", command=self.borrar_cliente)
        self.boton_borrar.grid(row=7, column=1)

        # Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"]=("col1", "col2", "col3", "col4")
        self.tree.column("#0", width=90, minwidth=50, anchor=W)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.column("col4", width=200, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Apellido")
        self.tree.heading("col3", text="Plan")
        self.tree.heading("col4", text="Precio")
        self.tree.grid(row=10, column=0, columnspan=4)

        self.actualizar_treeview()

    def crear_fila_entrada(self, row, nombre, textvariable, width):
        """
        Método para crear una fila de entrada de texto.

        Args:
            row (int): Índice de fila.
            nombre (str): Etiqueta para la entrada de texto.
            textvariable (StringVar): Variable de control para la entrada de texto.
            width (int): Ancho de la entrada de texto.

        Returns:
            Entry: La entrada de texto creada.
        """
        label = Label(self.root, text=nombre, bg="black", fg="white")
        label.grid(row=row, column=0, sticky=W)
        entry = Entry(self.root, textvariable=textvariable, width=width)
        entry.grid(row=row, column=1)
        return entry

    def callback(self, eventObject):
        """
        Método de devolución de llamada para actualizar el precio según el plan seleccionado.
        """
        plan_seleccionado = self.combo_plan.get()
        if plan_seleccionado == "Basico":
            self.label_precio_valor.config(text="4.000")
            self.d_val.set(4000)
        elif plan_seleccionado == "Medio":
            self.label_precio_valor.config(text="6.000")
            self.d_val.set(6000)
        elif plan_seleccionado == "Premium":
            self.label_precio_valor.config(text="8.000")
            self.d_val.set(8000)
        elif plan_seleccionado == "Especial":
            self.label_precio_valor.config(text="10.000")
            self.d_val.set(10000)

    def alta_cliente(self):
        """
        Método para agregar un nuevo cliente.
        """
        nombre = self.a_val.get()
        apellido = self.b_val.get()
        plan = self.combo_plan.get()
        precio = self.d_val.get()

        if nombre and apellido and plan:
            if self.modelo.alta_cliente(nombre, apellido, plan, precio):
                messagebox.showinfo("Éxito", "Cliente agregado correctamente")
                self.actualizar_treeview()
            else:
                messagebox.showerror("Error", "Error al agregar cliente")
        else:
            messagebox.showerror("Error", "Complete todos los campos")

    def borrar_cliente(self):
        """
        Método para borrar un cliente seleccionado.
        """
        item_seleccionado = self.tree.selection()
        if item_seleccionado:
            cliente_id = item_seleccionado[0]
            if self.modelo.borrar_cliente(cliente_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.actualizar_treeview()
            else:
                messagebox.showerror("Error", "Error al eliminar cliente")
        else:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")

    def actualizar_treeview(self):
        """
        Método para actualizar el Treeview con la lista de clientes.
        """
        registros = self.tree.get_children()
        for registro in registros:
            self.tree.delete(registro)

        clientes = self.modelo.obtener_clientes()
        for cliente in clientes:
            self.tree.insert("", 0, text=cliente[0], values=(cliente[1], cliente[2], cliente[3], cliente[4]))
