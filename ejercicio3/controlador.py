import serial
import time
from crud import Crud
from tkinter import messagebox

class ServoController:
    def __init__(self):
        host = 'localhost'
        user = 'root'
        password = ''
        database = 'arduino_bd'

        self.crud = Crud(host, user, password, database)
        result, error = self.crud.init_connection()

        if not result:
            print(f"Error al conectar a la base de datos: {error}")
            sys.exit(1)

        self.last_servo1_position = None
        self.last_servo2_position = None

    def validate_servo_value(self, value):
        try:
            grados_servo = int(value)
            if 0 <= grados_servo <= 180:
                return grados_servo, None  # Valor válido
            else:
                return None, "El valor debe estar en el rango de 0 a 180"
        except ValueError:
            return None, "Ingrese un valor numérico válido"

    def control_servo1(self, arduino, servo1, estadoServo1, barraEstado):
        nombre_servo1 = 'Servo 1'
        grados_servo1, error_message = self.validate_servo_value(servo1)

        if grados_servo1 is None:
            messagebox.showerror("Error", error_message)
            return

        query = "SELECT * FROM componentes WHERE tipo='servo' AND nombre=%s"
        cursor = self.crud.connection.cursor()
        cursor.execute(query, (nombre_servo1,))
        existing_componente_servo1 = cursor.fetchone()

        if not existing_componente_servo1:
            id_componente_servo1, error_componente_servo1 = self.crud.insert_componente(
                tipo='servo', nombre=nombre_servo1, descripcion=f'Descripcion del Servo 1 ({grados_servo1} grados)')

            if error_componente_servo1:
                print(f"Error al insertar componente del Servo 1 en la base de datos: {error_componente_servo1}")
                return
        else:
            id_componente_servo1 = existing_componente_servo1[0]

        cursor.close()
        if self.last_servo1_position is not None and grados_servo1 == self.last_servo1_position:
            return

        arduino.write(f"1:{grados_servo1}".encode('ascii'))
        time.sleep(0.1)
        estadoS1 = arduino.readline().decode('utf-8')
        estadoServo1.set(estadoS1.strip())

        id_registro_servo1, error_registro_servo1 = self.crud.insert_registro(id_componente_servo1, grados_servo1)

        if error_registro_servo1:
            print(f"Error al insertar registro del Servo 1 en la base de datos: {error_registro_servo1}")
        else:
            print(f"Servo 1 registrado en la base de datos. ID del componente: {id_componente_servo1}, ID del registro: {id_registro_servo1}")
        self.last_servo1_position = grados_servo1

    def control_servo2(self, arduino, servo2, estadoServo2, barraEstado):
        nombre_servo2 = 'Servo 2'
        grados_servo2, error_message = self.validate_servo_value(servo2)

        if grados_servo2 is None:
            messagebox.showerror("Error", error_message)
            return
        
        query = "SELECT * FROM componentes WHERE tipo='servo' AND nombre=%s"
        cursor = self.crud.connection.cursor()
        cursor.execute(query, (nombre_servo2,))
        existing_componente_servo2 = cursor.fetchone()

        if not existing_componente_servo2:
            id_componente_servo2, error_componente_servo2 = self.crud.insert_componente(
                tipo='servo', nombre=nombre_servo2, descripcion=f'Descripcion del Servo 2 ({grados_servo2} grados)')

            if error_componente_servo2:
                print(f"Error al insertar componente del Servo 2 en la base de datos: {error_componente_servo2}")
                return
        else:
            id_componente_servo2 = existing_componente_servo2[0]
        cursor.close()
        if self.last_servo2_position is not None and grados_servo2 == self.last_servo2_position:
            return

        arduino.write(f"2:{grados_servo2}".encode('ascii'))
        time.sleep(0.1)
        estadoS2 = arduino.readline().decode('utf-8')
        estadoServo2.set(estadoS2.strip())

        id_registro_servo2, error_registro_servo2 = self.crud.insert_registro(id_componente_servo2, grados_servo2)

        if error_registro_servo2:
            print(f"Error al insertar registro del Servo 2 en la base de datos: {error_registro_servo2}")
        else:
            print(f"Servo 2 registrado en la base de datos. ID del componente: {id_componente_servo2}, ID del registro: {id_registro_servo2}")
        self.last_servo2_position = grados_servo2
