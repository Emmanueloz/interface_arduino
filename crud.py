from datetime import datetime
from mysql.connector import Error, connect


class Crud:
    connection = None

    def __init__(self, host, user, password, database, port=3306):
        """Constructor para la clase Crud

        Args:
            host (str): host de la base de datos
            user (str): usuario de la base de datos
            password (str): contraseña de la base de datos
            database (str): database a la que se conectará
            port (int, optional): Puerto de conexión a la base de datos.Por defecto es 3306.
        """
        try:
            self.connection = connect(
                host=host, user=user, password=password, database=database, port=port)
            return "Conexión exitosa a la base de datos.", None
        except Error as e:
            return None, f"Se produjo un error al conectar a la base de datos: {e}"

    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        self.connection.close()

    def select_componentes(self, idComponente=None):
        """Consulta los componentes de la base de datos

        Args:
            idComponente (int, optional): id del componente a consultar. Por defecto es None.

        Returns:
            str: Es una cadena con los datos de los componentes
            None | str: En caso de error
        """
        try:
            cursor = self.connection.cursor()
            result = ""
            if idComponente is not None:
                sql += "SELECT * FROM componentes WHERE idComponente=%s"
                cursor.execute(sql, (idComponente,))
            else:
                sql = "SELECT * FROM componentes"
                cursor.execute(sql)

            for (idComponente, tipo, nombre, descripcion) in cursor.fetchall():
                result = + f"{idComponente}\t{tipo}\t{nombre}\t{descripcion}"

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
            return cursor.rowcount, None
        except Exception as e:
            self.connection.rollback()
            return None, f"Se produjo un error al insertar el componente: {e}"

    # Crud Operations for Registros table
    def select_registros(self, idRegistro=None):
        """Consulta los registros de la base de datos

        Args:
            idRegistro (int, optional): id del registro a consultar. Por defecto es None.

        Returns:
            str: Es una cadena con los datos de los registros
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

            for (idRegistro, idComponente, valor, fecha, hora) in cursor.fetchall():
                result = + \
                    f"{idRegistro}\t{idComponente}\t{valor}\t{fecha}\t{hora}"

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
            return cursor.rowcount, None
        except Exception as e:
            self.connection.rollback()
            return None, f"Se produjo un error al insertar el registro: {e}"
