from datetime import datetime
from mysql.connector import Error, connect


class Crud:
    connection = None

    def __init__(self, host, user, password, database, port=3306):
        self.connection = connect(
            host=host, user=user, password=password, database=database, port=port)

    def close_connection(self):
        self.connection.close()

    # Crud Operations for Componentes table
    def select_componentes(self, idComponente=None):
        if not self.connection.is_connected():
            raise Exception("Conexión de base de datos ha sido cerrada ")
        cursor = self.connection.cursor()
        sql = "SELECT * FROM componentes"
        if idComponente:
            sql += f" WHERE idComponente={idComponente}"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert_componente(self, tipo, nombre, descripcion):
        if not self.connection.is_connected():
            raise Exception("Conexión de base de datos ha sido cerrada ")
        cursor = self.connection.cursor()
        sql = "INSERT INTO componentes (tipo,nombre,descripcion) VALUES (%s,%s,%s)"
        values = (tipo, nombre, descripcion)
        cursor.execute(sql, values)
        self.connection.commit()
        cursor.close()
        return cursor.lastrowid

    # Crud Operations for Registros table
    def select_registros(self, idRegistro=None):
        if not self.connection.is_connected():
            raise Exception("Database connection has been closed")
        cursor = self.connection.cursor()
        sql = "SELECT * FROM registros"
        if idRegistro:
            sql += f" WHERE idRegistro={idRegistro}"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert_registro(self, idComponente, valor):
        if not self.connection.is_connected():
            raise Exception("Database connection has been closed")
        cursor = self.connection.cursor()
        fecha = datetime.now().date()
        hora = datetime.now().strftime("%H:%M:%S")
        sql = "INSERT INTO registros (idComponente,valor,fecha,hora) VALUES (%s,%s,%s,%s)"
        values = (idComponente, valor, fecha, hora)
        cursor.execute(sql, values)
        self.connection.commit()
        cursor.close()
        return cursor.lastrowid
