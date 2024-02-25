import serial
import time
from crud import Crud

class Controlador:
    def __init__(self, estadoTemp, estadoLumin, lstbox_temp, lstbox_lumin):
        self.estadoTemp = estadoTemp
        self.estadoLumin = estadoLumin
        self.lstbox_temp = lstbox_temp
        self.lstbox_lumin = lstbox_lumin

        # Inicializar la conexión a la base de datos
        self.crud = Crud(host='localhost', user='root', password='', database='arduino_bd')
        success, error = self.crud.init_connection()
        if not success:
            print(f"Error al conectar a la base de datos: {error}")
            

        # Inicializar la conexión al puerto serie Arduino
        self.arduino = serial.Serial('COM2', 9600, timeout=1)
        time.sleep(2)  # Esperar a que se estabilice la conexión
        print("Conexión con Arduino establecida")
        
    def verificar_y_insertar(self,nombre_sensor, tipo_sensor):
        existing_component, error_message = self.crud.select_componentes_tipo_nombre(tipo_sensor, nombre_sensor)
        if existing_component is None:
            print(f"Error al vereficar el componente existente: {error_message}")
            return None
        if not existing_component:
            _, error_message = self.crud.insert_componente(tipo_sensor, nombre_sensor, f"Descripcion de {nombre_sensor}")
            if error_message:
                print(f"Error al insertar el componente: {error_message}")
                return None
            
    def leerSensores(self):
        estaCorriendo = True
        while estaCorriendo:
            existing_sensor, error = self.crud.select_componentes_tipo_nombre(tipo='actuador', nombre='sensor')
            if existing_sensor:
                id_componente = existing_sensor[0]
            else:
                tipo= 'actuador'
                nombre = 'sensor'
                descripcion = 'se inserto movimientos'
                id_componente, error, = self.crud.insert_componente(tipo, nombre, descripcion)
                
                if error:
                    return f"Error inserting sensor {error}"            
            datos = self.arduino.readline().decode('utf-8').strip()
            if datos:
                posicion = datos.index(":")
                sensor = datos[:posicion]
                valor = datos[posicion+1:]
                if sensor == '3':
                    self.estadoTemp.set(valor)
                    self.lstbox_temp.insert("end", valor)
                    self.lstbox_temp.see("end")
                    id_registro, error = self.crud.insert_registro(idComponente=id_componente, valor=float(valor)) 
                    if error:
                        print(f"Error al insertar registro de temperatura en la base de datos: {error}")
                    
                elif sensor == '2':
                    self.estadoLumin.set(valor)
                    self.lstbox_lumin.insert("end", valor)
                    self.lstbox_lumin.see("end")
                
                    id_registro, error = self.crud.insert_registro(idComponente=id_componente, valor=float(valor))  
                    if error:
                        print(f"Error al insertar registro de luminosidad en la base de datos: {error}")
                        

    def finalizar(self):
        # Cerrar la conexión a la base de datos y al puerto serie Arduino
        self.crud.close_connection()
        self.arduino.close()