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


def control_servo1(arduino, servo1, estadoServo1, barraEstado):
    if servo1.get() != "":
        if servo1.get().isdigit():
            grados_servo1 = int(servo1.get())
            if 0 <= grados_servo1 <= 180:
                arduino.write(f"1:{grados_servo1}".encode('ascii'))
                time.sleep(0.1)

                estadoS1 = arduino.readline().decode('utf-8')

                estadoServo1.set(estadoS1.strip())

                id_componente_servo1, error_componente_servo1 = crud.insert_componente(
                    tipo='servo', nombre='Servo 1', descripcion=f'Descripcion del Servo 1 ({grados_servo1} grados)')

                if error_componente_servo1:
                    messagebox.showerror("ERROR", f"Error al insertar componente del Servo 1 en la base de datos: {error_componente_servo1}")
                    return

                id_registro_servo1, error_registro_servo1 = crud.insert_registro(id_componente_servo1, grados_servo1)

                if error_registro_servo1:
                    messagebox.showerror("ERROR", f"Error al insertar registro del Servo 1 en la base de datos: {error_registro_servo1}")
                else:
                    messagebox.showinfo("Éxito", f"Servo 1 registrado en la base de datos. ID del componente: {id_componente_servo1}, ID del registro: {id_registro_servo1}")

            else:
                messagebox.showwarning("CUIDADO", "El valor del Servo 1 debe estar entre 0 y 180")
        else:
            messagebox.showerror("ERROR", "Solo valores numéricos para el Servo 1")
    else:
        messagebox.showerror("ERROR", "Introduce un valor para el Servo 1")


def control_servo2(arduino, servo2, estadoServo2, barraEstado):
    print("Entrando a control_servo2")
    grados_servo2 = servo2.get()

    arduino.write(f"2:{grados_servo2}".encode('ascii'))
    time.sleep(0.1)

    estadoS2 = arduino.readline().decode('utf-8')
    estadoServo2.set(estadoS2.strip())

    try:
        id_componente_servo2, error_componente_servo2 = crud.insert_componente(
            tipo='servo', nombre='Servo 2', descripcion=f'Descripcion del Servo 2 ({grados_servo2} grados)')

        if error_componente_servo2:
            messagebox.showerror("ERROR", f"Error al insertar componente del Servo 2 en la base de datos: {error_componente_servo2}")
            return
        id_registro_servo2, error_registro_servo2 = crud.insert_registro(id_componente_servo2, grados_servo2)

        if error_registro_servo2:
            messagebox.showerror("ERROR", f"Error al insertar registro del Servo 2 en la base de datos: {error_registro_servo2}")
        else:
            messagebox.showinfo("Éxito", f"Servo 2 registrado en la base de datos. ID del componente: {id_componente_servo2}, ID del registro: {id_registro_servo2}")

    except Exception as e:
        messagebox.showerror("ERROR", f"Error al interactuar con la base de datos: {e}")
