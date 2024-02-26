import sqlite3
import re

class Modelo:
    """
    Clase que maneja la lógica de la base de datos.

    Attributes:
        conexion (sqlite3.Connection): La conexión a la base de datos SQLite.
        cursor (sqlite3.Cursor): El cursor para ejecutar consultas SQL.
    """

    def __init__(self):
        """
        Constructor de la clase Modelo. Establece la conexión a la base de datos.
        """
        self.conexion = sqlite3.connect("mibase.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        """
        Método para crear la tabla clientes en la base de datos si no existe.
        """
        sql = """CREATE TABLE IF NOT EXISTS clientes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre VARCHAR(20) NOT NULL,
                 apellido VARCHAR(20),
                 plan VARCHAR(20),
                 precio REAL)
        """
        self.cursor.execute(sql)
        self.conexion.commit()

    def alta_cliente(self, nombre, apellido, plan, precio):
        """
        Método para agregar un nuevo cliente a la base de datos.

        Args:
            nombre (str): El nombre del cliente.
            apellido (str): El apellido del cliente.
            plan (str): El plan del cliente.
            precio (float): El precio del plan del cliente.

        Returns:
            bool: True si se agregó el cliente correctamente, False en caso contrario.
        """
        patron = "^[A-Za-záéíóú ]+$"  # Expresión regular para validar nombre y apellido
        if re.match(patron, nombre) and re.match(patron, apellido):
            try:
                data = (nombre, apellido, plan, precio)
                sql = "INSERT INTO clientes(nombre, apellido, plan, precio) VALUES (?, ?, ?, ?)"
                self.cursor.execute(sql, data)
                self.conexion.commit()
                return True
            except sqlite3.Error as e:
                print("Error al insertar cliente:", e)
                return False
        else:
            return False

    def obtener_clientes(self):
        """
        Método para obtener la lista de clientes desde la base de datos.

        Returns:
            list: Lista de tuplas con los datos de los clientes (id, nombre, apellido, plan, precio).
        """
        try:
            sql = "SELECT * FROM clientes"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error al obtener clientes:", e)
            return []

    def borrar_cliente(self, cliente_id):
        """
        Método para borrar un cliente de la base de datos.

        Args:
            cliente_id (int): El ID del cliente a borrar.

        Returns:
            bool: True si se eliminó el cliente correctamente, False en caso contrario.
        """
        try:
            sql = "DELETE FROM clientes WHERE id = ?"
            self.cursor.execute(sql, (cliente_id,))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print("Error al borrar cliente:", e)
            return False
