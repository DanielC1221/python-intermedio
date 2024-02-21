from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from modelo import crear_fila_entrada, alta, actualizar_treeview, borrar, limpiarCampos, callback

# ##############################################
# VISTA
# ##############################################

def vista_menu(root):

    #miFrame = Tk()
    
    barraMenu=Menu(root)
    root.config(menu=barraMenu, width=300, height=300)

    borrarMenu=Menu(barraMenu, tearoff=0)
    borrarMenu.add_command(label="Borrar campos", command=lambda:limpiarCampos(a_val, b_val, c_val, d_val))

    barraMenu.add_cascade(label="Borrar campos", menu=borrarMenu)

    root.title("📡 InterSat4 - Sistema para Registrar Clientes de Internet 📡")
    #root.configure(bg="#A9A9A9")

    # Agregar imagenes
    imagen = PhotoImage(file="intersat4.png", width=400, height=400)
    imagen_label = Label(root, image=imagen, bg="white")
    imagen_label.grid(row=0, column=6, rowspan=8, padx=5, pady=5, sticky="e")

    imagen_label.image = imagen # mantenga una referencia!


    titulo = Label(root, text="Plantilla de clientes - Ingrese los datos", font=("Arial", 16, "bold"), fg="black", bg="white")
    titulo.grid(row=0, column=0, columnspan=6, pady=(10, 10), sticky="we")

    # Variables de control
    a_val = StringVar()
    b_val = StringVar()
    c_val = StringVar()
    d_val = DoubleVar()

    # Crear filas de entrada, variando la de
    entrada1 = crear_fila_entrada(1, "Nombre", a_val, 30)
    entrada2 = crear_fila_entrada(2, "Apellido", b_val, 30)
    #entrada3 = crear_fila_entrada(3, "Plan", c_val, 30)
    #entrada4 = crear_fila_entrada(4, "Precio", d_val, 30)
    entrada3 = Label(text="Plan", bg="black", fg="white")
    entrada3.grid(row=3, column=1, sticky=W)
    entrada4 = Label(text="Precio", bg="black", fg="white")
    entrada4.grid(row=4, column=1, sticky=W)
    LabelPrecio = Label(text="0.0", bg="black", fg="white")
    LabelPrecio.grid(row=4, column=1)
    LabelPrecio.config(font=10)



    combo = ttk.Combobox(
        width=27,
        state="readonly",
        values=["Basico", "Medio", "Premium", "Especial"]
    )
    combo.place(x=265, y=190)


    combo.bind("<<ComboboxSelected>>", callback)

        

    # --------------------------------------------------
    # TREEVIEW
    # --------------------------------------------------
    tree = ttk.Treeview(root)
    tree["columns"]=("col1", "col2", "col3", "col4")
    tree.column("#0", width=90, minwidth=50, anchor=W)
    tree.column("col1", width=200, minwidth=80)
    tree.column("col2", width=200, minwidth=80)
    tree.column("col3", width=200, minwidth=80)
    tree.column("col4", width=200, minwidth=80)
    tree.heading("#0", text="ID")
    tree.heading("col1", text="Nombre")
    tree.heading("col2", text="Apellido")
    tree.heading("col3", text="Plan")
    tree.heading("col4", text="Precio")
    tree.grid(row=10, column=0, columnspan=4)


    # BOTONES
    boton_alta=Button(root, text="Alta", command=lambda:alta(a_val.get(), b_val.get(), combo.get(), d_val.get(), tree))
    boton_alta.grid(row=6, column=1)

    #boton_consulta=Button(root, text="Consultar", command=lambda:consultar())
    #boton_consulta.grid(row=7, column=1)

    boton_borrar=Button(root, text="Borrar", command=lambda:borrar(tree))
    boton_borrar.grid(row=7, column=1)
    
    actualizar_treeview(tree)
    #root.mainloop()