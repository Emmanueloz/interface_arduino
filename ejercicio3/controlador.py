import serial
import time
from crud import Crud
import sys

host = 'localhost'
user = 'root'
password = ''
database = 'arduino_bd'

crud = Crud(host, user, password, database)
result, error = crud.init_connection()

if not result:
    print(f"Error al conectar a la base de datos: {error}")
    sys.exit(1)


last_servo1_position = None
last_servo2_position = None

def control_servo1(arduino, servo1, estadoServo1, barraEstado):
    global last_servo1_position

    nombre_servo1 = 'Servo 1'
    grados_servo1 = servo1.get()

    query = "SELECT * FROM componentes WHERE tipo='servo' AND nombre=%s"
    cursor = crud.connection.cursor()
    cursor.execute(query, (nombre_servo1,))
    existing_componente_servo1 = cursor.fetchone()

    if not existing_componente_servo1:
        id_componente_servo1, error_componente_servo1 = crud.insert_componente(
            tipo='servo', nombre=nombre_servo1, descripcion=f'Descripcion del Servo 1 ({grados_servo1} grados)')

        if error_componente_servo1:
            print(f"Error al insertar componente del Servo 1 en la base de datos: {error_componente_servo1}")
            return
    else:
        id_componente_servo1 = existing_componente_servo1[0]

    cursor.close()

    # Check if the servo position has changed
    if last_servo1_position is not None and grados_servo1 == last_servo1_position:
        return

    arduino.write(f"1:{grados_servo1}".encode('ascii'))
    time.sleep(0.1)
    estadoS1 = arduino.readline().decode('utf-8')
    estadoServo1.set(estadoS1.strip())

    id_registro_servo1, error_registro_servo1 = crud.insert_registro(id_componente_servo1, grados_servo1)

    if error_registro_servo1:
        print(f"Error al insertar registro del Servo 1 en la base de datos: {error_registro_servo1}")
    else:
        print(f"Servo 1 registrado en la base de datos. ID del componente: {id_componente_servo1}, ID del registro: {id_registro_servo1}")

    # Update last_servo1_position after successful insertion
    last_servo1_position = grados_servo1

def control_servo2(arduino, servo2, estadoServo2, barraEstado):
    global last_servo2_position

    nombre_servo2 = 'Servo 2'
    grados_servo2 = servo2.get()

    query = "SELECT * FROM componentes WHERE tipo='servo' AND nombre=%s"
    cursor = crud.connection.cursor()
    cursor.execute(query, (nombre_servo2,))
    existing_componente_servo2 = cursor.fetchone()

    if not existing_componente_servo2:
        id_componente_servo2, error_componente_servo2 = crud.insert_componente(
            tipo='servo', nombre=nombre_servo2, descripcion=f'Descripcion del Servo 2 ({grados_servo2} grados)')

        if error_componente_servo2:
            print(f"Error al insertar componente del Servo 2 en la base de datos: {error_componente_servo2}")
            return
    else:
        id_componente_servo2 = existing_componente_servo2[0]

    cursor.close()

    # Check if the servo position has changed
    if last_servo2_position is not None and grados_servo2 == last_servo2_position:
        return

    arduino.write(f"2:{grados_servo2}".encode('ascii'))
    time.sleep(0.1)
    estadoS2 = arduino.readline().decode('utf-8')
    estadoServo2.set(estadoS2.strip())

    id_registro_servo2, error_registro_servo2 = crud.insert_registro(id_componente_servo2, grados_servo2)

    if error_registro_servo2:
        print(f"Error al insertar registro del Servo 2 en la base de datos: {error_registro_servo2}")
    else:
        print(f"Servo 2 registrado en la base de datos. ID del componente: {id_componente_servo2}, ID del registro: {id_registro_servo2}")

    # Update last_servo2_position after successful insertion
    last_servo2_position = grados_servo2