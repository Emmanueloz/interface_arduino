import serial
import time
from crud import Crud 
from tkinter import ttk
import tkinter as tk

class Controlador:
    def __init__(self, estadoTemp, estadoLumin, lstbox_temp, lstbox_lumin):
        """
        Inicializa un objeto Controlador.

        Parámetros:
        - estadoTemp: Variable de estado para la temperatura.
        - estadoLumin: Variable de estado para la luminosidad.
        - lstbox_temp: Lista de visualización para la temperatura.
        - lstbox_lumin: Lista de visualización para la luminosidad.
        """
        self.estadoTemp = estadoTemp  # Estado de temperatura
        self.estadoLumin = estadoLumin  # Estado de luminosidad
        self.lstbox_temp = lstbox_temp  # Lista de temperatura
        self.lstbox_lumin = lstbox_lumin  # Lista de luminosidad

        # Inicializa la conexión a la base de datos
        self.crud = Crud(host='localhost', user='root', password='', database='arduino_bd')
        success, error = self.crud.init_connection() 
        if not success: 
            print(f"Error al conectar a la base de datos: {error}") 
            
        try:
            self.arduino = serial.Serial('COM2', 9600, timeout=1)  
            time.sleep(2)  # Espera 2 segundos para que la conexión se estabilice
            print(self.arduino)
            self.arduino.write("1:0".encode())
            time.sleep(0.1)
            datos = self.arduino.readline(). decode ('utf-8')
            print(datos)
            if datos:
                print("datos recibidos")
                estados = eval(datos)
                self.estadoTemp.set(estados[0])
                self.estadoLumin.set(estados[1])
            print("Conexión establecida con Arduino ")  # Muestra un mensaje indicando que la conexión se ha establecido correctamente
        except serial.SerialException as e:
            print(f"Error al conectar con Arduino: {e}")
            
    def mostrar_registros_sensores(self):
            registros_temperatura, error_temperatura = self.crud.select_registros(tipo='actuador', nombre='temperatura')
            registros_luminosidad, error_luminosidad = self.crud.select_registros(tipo='actuador', nombre='luminosidad')

            if error_temperatura or error_luminosidad:
                return None, f"Error al obtener los registros: {error_temperatura or error_luminosidad}"

            return registros_temperatura, registros_luminosidad, None    
        
        
    def verificar_y_insertar(self,nombre_sensor, tipo_sensor):
        """
        Verifica la existencia de un componente en la base de datos y lo inserta si no existe.

        Parámetros:
        - nombre_sensor: Nombre del sensor.
        - tipo_sensor: Tipo del sensor.
        """
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
        """
        Lee los datos de los sensores y los procesa.
        """
        estaCorriendo = True
        while estaCorriendo:
            datos = self.arduino.readline().decode('utf-8').strip()
            if datos:
                posicion = datos.index(":")
                sensor = datos[:posicion]
                valor = datos[posicion+1:]
                if sensor == '3':
                    existing_sensor, error = self.crud.select_componentes_tipo_nombre(tipo='actuador', nombre='temperatura')
                    if existing_sensor:
                        id_componente = existing_sensor[0]  # Obtiene el ID del componente
                    else:
                        # Si no está registrado, lo inserta en la base de datos
                        tipo= 'actuador'
                        nombre = 'temperatura'
                        descripcion = 'se inserto movimientos de temp'
                        id_componente, error, = self.crud.insert_componente(tipo, nombre, descripcion)
                        if error:
                            return f"Error al insertar sensor {error}"  # Muestra un mensaje de error si falla la inserción
                    # Si el sensor es de temperatura
                    self.estadoTemp.set(valor)  # Actualiza el estado de la temperatura
                    self.lstbox_temp.insert("end", valor)  # Agrega el valor a la lista de temperatura
                    self.lstbox_temp.see("end")  # Asegura que el nuevo valor sea visible
                    id_registro, error = self.crud.insert_registro(idComponente=id_componente, valor=float(valor)) 
                    if error:
                        print(f"Error al insertar registro de temperatura en la base de datos: {error}")
                elif sensor == '2':
                    existing_sensor, error = self.crud.select_componentes_tipo_nombre(tipo='actuador', nombre='luminosidad')
                    if existing_sensor:
                        id_componente = existing_sensor[0]  # Obtiene el ID del componente
                    else:
                        # Si no está registrado, lo inserta en la base de datos
                        tipo= 'actuador'
                        nombre = 'luminosidad'
                        descripcion = 'se inserto movimientos de luminosidad'
                        id_componente, error, = self.crud.insert_componente(tipo, nombre, descripcion)
                        if error:
                            return f"Error al insertar sensor {error}"
                    # Si el sensor es de luminosidad
                    self.estadoLumin.set(valor)  # Actualiza el estado de la luminosidad
                    self.lstbox_lumin.insert("end", valor)  # Agrega el valor a la lista de luminosidad
                    self.lstbox_lumin.see("end")  # Asegura que el nuevo valor sea visible
                    id_registro, error = self.crud.insert_registro(idComponente=id_componente, valor=float(valor))  
                    if error:
                        print(f"Error al insertar registro de luminosidad en la base de datos: {error}")
                        
    def finalizar(self): 
        self.estaCorriendo = False      
        self.crud.close_connection()  
        self.arduino.close()
        hiloSensores.join(0.1)
        miVentana.quit()
        miVentana.destroy()  
