import serial
import time
from crud import Crud  

class Controlador:
    def __init__(self, estadoTemp, estadoLumin, lstbox_temp, lstbox_lumin):
        
        self.estadoTemp = estadoTemp  # Estado de temperatura
        self.estadoLumin = estadoLumin  # Estado de luminosidad
        self.lstbox_temp = lstbox_temp  # Lista de temperatura
        self.lstbox_lumin = lstbox_lumin  # Lista de luminosidad

        # Inicializa la conexión a la base de datos
        self.crud = Crud(host='172.20.10.4', user='root', password='2004loco#with', database='arduino_bd')
        success, error = self.crud.init_connection()  # Intenta iniciar la conexión
        if not success:
            print(f"Error al conectar a la base de datos: {error}")  # Muestra un mensaje de error si la conexión falla

        # Inicializa la conexión al puerto serie Arduino
        self.arduino = serial.Serial('COM2', 9600, timeout=1)  # Conexión al puerto COM2 a 9600 baudios
        time.sleep(2)  # Espera 2 segundos para que la conexión se estabilice
        print("Conexión establecida Con Arduino")  # Muestra un mensaje indicando que la conexión se ha establecido correctamente
        
    def verificar_y_insertar(self,nombre_sensor, tipo_sensor):
        # Verifica si ya existe un componente con el mismo nombre y tipo en la base de datos
        existing_component, error_message = self.crud.select_componentes_tipo_nombre(tipo_sensor, nombre_sensor)
        if existing_component is None:
            print(f"Error al verificar el componente existente: {error_message}")
            return None
        if not existing_component:
            # Si no existe, inserta el componente en la base de datos
            _, error_message = self.crud.insert_componente(tipo_sensor, nombre_sensor, f"Descripcion de {nombre_sensor}")
            if error_message:
                print(f"Error al insertar el componente: {error_message}")
                return None           
    def leerSensores(self):
        estaCorriendo = True
        while estaCorriendo:
            # Verifica si el sensor ya está registrado en la base de datos
            existing_sensor, error = self.crud.select_componentes_tipo_nombre(tipo='actuador', nombre='sensor')
            if existing_sensor:
                id_componente = existing_sensor[0]  # Obtiene el ID del componente
            else:
                # Si no está registrado, lo inserta en la base de datos
                tipo= 'actuador'
                nombre = 'sensor'
                descripcion = 'se inserto movimientos'
                id_componente, error, = self.crud.insert_componente(tipo, nombre, descripcion)
                if error:
                    return f"Error al insertar sensor {error}"  # Muestra un mensaje de error si falla la inserción
                
            # Lee los datos del Arduino
            datos = self.arduino.readline().decode('utf-8').strip()
            if datos:
                posicion = datos.index(":")
                sensor = datos[:posicion]
                valor = datos[posicion+1:]
                if sensor == '3':
                    # Si el sensor es de temperatura
                    self.estadoTemp.set(valor)  # Actualiza el estado de la temperatura
                    self.lstbox_temp.insert("end", valor)  # Agrega el valor a la lista de temperatura
                    self.lstbox_temp.see("end")  # Asegura que el nuevo valor sea visible
                    id_registro, error = self.crud.insert_registro(idComponente=id_componente, valor=float(valor)) 
                    if error:
                        print(f"Error al insertar registro de temperatura en la base de datos: {error}")
                elif sensor == '2':
                    # Si el sensor es de luminosidad
                    self.estadoLumin.set(valor)  # Actualiza el estado de la luminosidad
                    self.lstbox_lumin.insert("end", valor)  # Agrega el valor a la lista de luminosidad
                    self.lstbox_lumin.see("end")  # Asegura que el nuevo valor sea visible
                    id_registro, error = self.crud.insert_registro(idComponente=id_componente, valor=float(valor))  
                    if error:
                        print(f"Error al insertar registro de luminosidad en la base de datos: {error}")
                        
    def finalizar(self):
        # Cierra la conexión a la base de datos y al puerto serie Arduino
        self.crud.close_connection()
        self.arduino.close()  # Comentario sobre el cierre de las conexiones
