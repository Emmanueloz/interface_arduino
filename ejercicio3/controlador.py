import sys
import serial
import time
from crud import Crud

class Controlador:
    def __init__(self, estadoServo1, estadoServo2, servo1, servo2, barraEstado):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'arduino_bd'
        self.crud = Crud(self.host, self.user, self.password, self.database)
        self.result, self.error = self.crud.init_connection()

        if not self.result:
            print(f"Error al conectar a la base de datos: {self.error}")
            sys.exit(1)

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
            estadoServo1.set(str(estados[0]))
            estadoServo2.set(estados[1])
            servo2.set(estados[1])
        else:
            print("No se recibieron datos...")
            barraEstado.set("ERROR al conectar con Arduino")

    def control_servo1(self, grados_servo1):
        if grados_servo1 != "":
            if grados_servo1.isdigit():
                grados_servo1 = int(grados_servo1)
                if 0 <= grados_servo1 <= 180:
                    self.arduino.write(f"1:{grados_servo1}".encode('ascii'))
                    time.sleep(0.1)

                    estadoS1 = self.arduino.readline().decode('utf-8')
                    estadoServo1.set(estadoS1.strip())

                    id_componente_servo1, error_componente_servo1 = self.crud.insert_componente(
                        tipo='servo', nombre='Servo 1', descripcion=f'Descripcion del Servo 1 ({grados_servo1} grados)')

                    if error_componente_servo1:
                        return ('Error', f"Error al insertar componente del Servo 1 en la base de datos: {error_componente_servo1}", 'error')

                    id_registro_servo1, error_registro_servo1 = self.crud.insert_registro(id_componente_servo1, grados_servo1)

                    if error_registro_servo1:
                        return ('Error', f"Error al insertar registro del Servo 1 en la base de datos: {error_registro_servo1}", 'error')
                    else:
                        return ('Éxito', f"Servo 1 registrado en la base de datos. ID del componente: {id_componente_servo1}, ID del registro: {id_registro_servo1}", 'info')

                else:
                    return ('CUIDADO', 'El valor del Servo 1 debe estar entre 0 y 180', 'warning')
            else:
                return ('Error', 'Solo valores numéricos para el Servo 1', 'error')
        else:
            return ('Error', 'Introduce un valor para el Servo 1', 'error')

    def control_servo2(self, grados_servo2):
        self.arduino.write(f"2:{grados_servo2}".encode('ascii'))
        time.sleep(0.1)

        estadoS2 = self.arduino.readline().decode('utf-8')
        estadoServo2.set(estadoS2.strip())

        try:
            id_componente_servo2, error_componente_servo2 = self.crud.insert_componente(
                tipo='servo', nombre='Servo 2', descripcion=f'Descripcion del Servo 2 ({grados_servo2} grados)')

            if error_componente_servo2:
                return ('Error', f"Error al insertar componente del Servo 2 en la base de datos: {error_componente_servo2}", 'error')

            id_registro_servo2, error_registro_servo2 = self.crud.insert_registro(id_componente_servo2, grados_servo2)

            if error_registro_servo2:
                return ('Error', f"Error al insertar registro del Servo 2 en la base de datos: {error_registro_servo2}", 'error')
            else:
                return ('Éxito', f"Servo 2 registrado en la base de datos. ID del componente: {id_componente_servo2}, ID del registro: {id_registro_servo2}", 'info')

        except Exception as e:
            return ('Error', f"Error al interactuar con la base de datos: {e}", 'error')
