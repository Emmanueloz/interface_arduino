import serial
import time
from crud import Crud 

class Controlador:
    def __init__(self):
        self.arduino = serial.Serial('COM2', 9600, timeout=1)
        time.sleep(2)
        print(self.arduino)

        self.arduino.write("3:0".encode())
        time.sleep(0.1)
        datos = self.arduino.readline().decode('utf-8')
        print(datos)

        if datos:
            print("Datos recibidos...")
            estados = eval(datos)
            self.estado_servo1 = str(estados[0])
            self.estado_servo2 = estados[1]
            self.servo2 = estados[1]
        else:
            print("No se recibieron datos...")
            self.barra_estado = "ERROR al conectar con Arduino"
        self.posicion_actual_servo1 = int(self.estado_servo1)
        self.posicion_actual_servo2 = int(self.estado_servo2)
        self.crud = Crud(host='localhost', user='root', password='tavo', database='arduino_bd')
        success, error_message = self.crud.init_connection()

        if not success:
            print(f"Error initializing database connection: {error_message}")
            
    def mostrar_registros_servos(self):
        registros_servo1, error_servo1 = self.crud.select_registros(tipo='actuador', nombre='servo1')
        registros_servo2, error_servo2 = self.crud.select_registros(tipo='actuador', nombre='servo2')

        if error_servo1 or error_servo2:
            return None, f"Error al obtener los registros: {error_servo1 or error_servo2}"

        return registros_servo1, registros_servo2, None




            
    def verificar_y_insertar_componente(self, nombre_servo, tipo_servo):
        existing_component, error_message = self.crud.select_componentes_tipo_nombre(tipo_servo, nombre_servo)
        if existing_component is None:
            print(f"Error al verificar el componente existente: {error_message}")
            return None
        if not existing_component:
            _, error_message = self.crud.insert_componente(tipo_servo, nombre_servo, f"Descripción de {nombre_servo}")
            if error_message:
                print(f"Error al insertar el componente: {error_message}")
                return None

    def control_servo1(self, grados):
        if grados.isdigit():
            grados = int(grados)
            if 0 <= grados <= 180:
                existing_servo, error = self.crud.select_componentes_tipo_nombre(tipo='actuador', nombre='servo1')
                if existing_servo:
                    id_componente = existing_servo[0]  
                else:
                    tipo = 'actuador'
                    nombre = 'servo1'
                    descripcion = 'se inserto una instruccion de servo'
                    id_componente, error = self.crud.insert_componente(tipo, nombre, descripcion)
                    
                    if error:
                        return f"Error inserting component: {error}"


                if grados != self.posicion_actual_servo1:
                    self.arduino.write(f"1:{grados}".encode('ascii'))
                    time.sleep(0.1)
                    estado_s1 = self.arduino.readline().decode('utf-8')
                    self.crud.insert_registro(id_componente, grados)

                    self.posicion_actual_servo1 = grados
                    return estado_s1.strip()
                else:
                    return "NO SE HA CAMBIADO LA POSICIÓN DEL SERVO"
            else:
                return "EL VALOR DEL SERVO DEBE ESTAR EN 0 A 180"
        else:
            return "EL VALOR DEBE SER NUMERICO"

    def control_servo2(self, grados):
        if grados.isdigit():
            grados = int(grados)
            if 0 <= grados <= 180:
                existing_servo, error = self.crud.select_componentes_tipo_nombre(tipo='actuador', nombre='servo2')
                if existing_servo:
                    id_componente = existing_servo[0] 
                else:
                    tipo = 'actuador'
                    nombre = 'servo2'
                    descripcion = 'se inserto una instruccion de servo'
                    id_componente, error = self.crud.insert_componente(tipo, nombre, descripcion)
                    if error:
                        return f"Error inserting component: {error}"

                if grados != self.posicion_actual_servo2:
                    self.arduino.write(f"2:{grados}".encode('ascii'))
                    time.sleep(0.1)
                    estado_s2 = self.arduino.readline().decode('utf-8')

  
                    self.crud.insert_registro(id_componente, grados)

                    self.posicion_actual_servo2 = grados
                    return estado_s2.strip()
                else:
                    return "NO SE HA CAMBIADO LA POSICIÓN DEL SERVO2"
            else:
                return "EL VALOR DEL SERVO DEBE ESTAR EN 0 A 180"
        else:
            return "EL VALOR DEBE SER NUMERICO"