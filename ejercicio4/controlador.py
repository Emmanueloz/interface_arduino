from crud import Crud

class Controlador:
    def __init__(self):
        # Detalles de conexión a la base de datos
        host = 'localhost'
        user = 'root'
        password = ''
        database = 'arduino_bd'

        # Inicializar el objeto Crud con los detalles de la conexión
        self.crud = Crud(host, user, password, database)

        # Intentar establecer la conexión al iniciar el controlador
        result, error = self.crud.init_connection()
        if error:
            print(f"Error al conectar a la base de datos: {error}")
        else:
            print("Conexión establecida correctamente.")

    def obtener_componentes(self):
        """Obtiene todos los componentes de la base de datos."""
        componentes, error = self.crud.select_componentes()
        if error:
            return None, error
        return componentes, None

    def agregar_componente(self, tipo, nombre, descripcion):
        """Agrega un nuevo componente a la base de datos."""
        fila_afectada, error = self.crud.insert_componente(tipo, nombre, descripcion)
        if error:
            return None, error
        return fila_afectada, None

    def obtener_registros(self, id_componente=None):
        """Obtiene los registros de la base de datos."""
        registros, error = self.crud.select_registros(id_componente)
        if error:
            return None, error
        return registros, None

    def agregar_registro(self, id_componente, valor):
        """Agrega un nuevo registro a la base de datos."""
        fila_afectada, error = self.crud.insert_registro(id_componente, valor)
        if error:
            return None, error
        return fila_afectada, None

    def agregar_sensor_por_tipo(self, tipo_sensor, nombre_sensor, descripcion_sensor):
        """Agrega un nuevo sensor a la base de datos según el tipo especificado."""
        fila_afectada, error = self.crud.insert_sensor(tipo_sensor, nombre_sensor, descripcion_sensor)
        if error:
            return None, error
        return fila_afectada, None
