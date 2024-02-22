import serial
import time
import threading

class Controlador:
    def __init__(self, puerto_serial='COM2'):
        self.arduino = serial.Serial(puerto_serial, 9600, timeout=1)
        time.sleep(2)
        print(self.arduino)

    def enviar_comando(self, comando):
        try:
            self.arduino.write(comando.encode())
            time.sleep(0.1)
            datos = self.arduino.readline().decode('utf-8')
            print(datos)
            return datos.strip() if datos else None
        except serial.SerialException as e:
            print(f"Error al enviar el comando: {e}")
            return None

    def cerrar_conexion(self):
        self.arduino.close()

if __name__ == "__main__":
    controlador = Controlador()

    while True:
        print("1: Leer datos de sensores")
        print("2: Otro comando")
        print("3: Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == '1':
            datos = controlador.enviar_comando("1:0")
            if datos:
                print(f"Datos recibidos: {datos}")
            else:
                print("No se recibieron datos.")
        elif opcion == '2':
            # Implementa aquí el manejo de otro comando
            pass
        elif opcion == '3':
            controlador.cerrar_conexion()
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")
