from datetime import datetime
from mysql.connector import Error, connect


class Crud:
    connection = None

    def __init__(self, host, user, password, database, port=3306):
        """Inicializa el objeto Crud

        Args:
            host (str): Dirección del host
            user (str): Usuario de la base de datos
            password (str): Contraseña del usuario
            database (str): Nombre de la base de datos
            port (int, optional): Puerto de la base de datos. Por defecto es 3306.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def init_connection(self):
        """Inicia la conexión a la base de datos"""
        try:
            self.connection = connect(
                host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            return True, None
        except Error as e:
            return False, f"Se produjo un error al conectar a la base de datos: {e}"

    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        self.connection.close()

    def select_componentes(self, idComponente=None):
        """Consulta los componentes de la base de datos

        Args:
            idComponente (int, optional): id del componente a consultar. Por defecto es None.

        Returns:
            tuple: Lista de componentes
            None | str: En caso de error
        """
        try:
            cursor = self.connection.cursor()
            result = ""
            if idComponente is not None:
                sql = "SELECT * FROM componentes WHERE idComponente=%s"
                cursor.execute(sql, (idComponente,))
            else:
                sql = "SELECT * FROM componentes"
                cursor.execute(sql)

            result = cursor.fetchall()
            cursor.close()
            return result, None
        except Exception as e:
            return None, f"Se produjo un error al seleccionar los datos:  {e}"

    def insert_componente(self, tipo, nombre, descripcion):
        """Inserta un componente en la base de datos

        Args:
            tipo (str): Tipo de componente
            nombre (str): Nombre del componente
            descripcion (str): Descripción del componente

        Returns:
            int: fila afectada
            None | str: En caso de error
        """
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO componentes (tipo,nombre,descripcion) VALUES (%s,%s,%s)"
            values = (tipo, nombre, descripcion)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid, None
        except Exception as e:
            self.connection.rollback()
            return None, f"Se produjo un error al insertar el componente: {e}"

    # Crud Operations for Registros table
    def select_registros(self, idRegistro=None):
        """Consulta los registros de la base de datos

        Args:
            idRegistro (int, optional): id del registro a consultar. Por defecto es None.

        Returns:
            tuple: Lista de registros
            None | str: En caso de error
        """
        try:
            cursor = self.connection.cursor()
            result = ""

            if idRegistro is not None:
                sql = "SELECT * FROM registros WHERE idRegistro=%s"
                cursor.execute(sql, (idRegistro,))
            else:
                sql = "SELECT * FROM registros"
                cursor.execute(sql)

            result = cursor.fetchall()

            cursor.close()
            return result, None
        except Exception as e:
            return None, f"Se produjo un error al seleccionar los datos: {e}"

    def insert_registro(self, idComponente, valor):
        """Inserta un registro en la base de datos

        Args:
            idComponente (int): id del componente
            valor (float): valor del componente

        Returns:
            int: fila afectada
            None | str: En caso de error
        """
        try:
            fecha = datetime.now().date()
            hora = datetime.now().strftime("%H:%M:%S")
            cursor = self.connection.cursor()
            sql = "INSERT INTO registros (idComponente,valor,fecha,hora) VALUES (%s,%s,%s,%s)"
            values = (idComponente, valor, fecha, hora)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid, None
        except Exception as e:
            self.connection.rollback()
            return None, f"Se produjo un error al insertar el registro: {e}"

#LED
    def insert_registro_led(self, idComponente, accion):
        """Inserta un registro relacionado con el encendido del LED en la base de datos

        Args:
            idComponente (int): id del componente (LED)
            accion (str): Acción realizada (Encendido o Apagado)

        Returns:
            int: fila afectada
            None | str: En caso de error
        """
        try:
            fecha = datetime.now().date()
            hora = datetime.now().strftime("%H:%M:%S")
            cursor = self.connection.cursor()
            sql = "INSERT INTO registros (idComponente, accion, fecha, hora) VALUES (%s, %s, %s, %s)"
            values = (idComponente, accion, fecha, hora)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid, None
        except Exception as e:
            self.connection.rollback()
            return None, f"Se produjo un error al insertar el registro del LED: {e}"
