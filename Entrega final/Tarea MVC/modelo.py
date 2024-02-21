from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re
# ##############################################
# MODELO
# ##############################################


def conexion():
    con = sqlite3.connect("mibase.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE clientes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre varchar(20) NOT NULL,
             apellido varchar(20),
             plan varchar(20),
             precio real)
    """
    cursor.execute(sql)
    con.commit()

try:
    conexion()
except:
    print("Hay un error")

def limpiarCampos(a_val, b_val, c_val, d_val):
    a_val.set("")
    b_val.set("")
    c_val.set("")
    d_val.set("")


def alta(nombre, apellido, plan, precio, tree):
    patron="^[A-Za-záéíóú]*$"  #regex para el campo cadena
    if(re.match(patron, nombre) and re.match(patron, apellido) and nombre != " "):
        print(nombre, apellido, plan, precio)
        con=conexion()
        cursor=con.cursor()
        data=(nombre, apellido, plan, precio)
        sql="INSERT INTO clientes(nombre, apellido, plan, precio) VALUES(?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print("Estoy en alta todo ok")
        actualizar_treeview(tree)
    else:
        showerror("Error","Error en algun campo")


def borrar(tree):
    valor = tree.selection()
    print(valor)   #('I005',)
    item = tree.item(valor)
    print(item)    #{'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
    print(item['text'])
    mi_id = item['text']

    con=conexion()
    cursor=con.cursor()
    #mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM clientes WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)



def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM clientes ORDER BY id ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4]))

def crear_fila_entrada(row, nombre, textvariable, width):
    label = Label(text=nombre, bg="black", fg="white")
    label.grid(row=row, column=1, sticky=W)
    entry = Entry(textvariable=textvariable, width=width)
    entry.grid(row=row, column=1)
    return entry


def callback(eventObject):
    # Obtener la opción seleccionada.
    #seleccion = combo.get()

    if(eventObject == "Basico"):
        LabelPrecio = Label(text="4.000", bg="black", fg="white")
        LabelPrecio.grid(row=4, column=1)
        LabelPrecio.config(font=10)
        d_val=4000
    elif(eventObject == "Medio"):
        LabelPrecio = Label(text="6.000", bg="black", fg="white")
        LabelPrecio.grid(row=4, column=1)
        LabelPrecio.config(font=10)
        d_val=6000
    elif(eventObject == "Premuim"):
        LabelPrecio = Label(text="8.000", bg="black", fg="white")
        LabelPrecio.grid(row=4, column=1)
        LabelPrecio.config(font=10)
        d_val=8000
    else:
        LabelPrecio = Label(text="10.000", bg="black", fg="white")
        LabelPrecio.grid(row=4, column=1)
        LabelPrecio.config(font=10)
        d_val=10000

    return d_val