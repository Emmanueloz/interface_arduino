import serial
import time

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

    def control_servo1(self, grados):
        if grados.isdigit():
            grados = int(grados)
            if 0 <= grados <= 180:
                # Verificar si la nueva posición es diferente de la actual
                if grados != self.posicion_actual_servo1:
                    self.arduino.write(f"1:{grados}".encode('ascii'))
                    time.sleep(0.1)
                    estado_s1 = self.arduino.readline().decode('utf-8')
                    # Actualizar la posición actual del servo1
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
            if 0 <= grados <= 180 and grados != self.posicion_actual_servo2:
                self.arduino.write(f"2:{grados}".encode('ascii'))
                time.sleep(0.1)
                estado_s2 = self.arduino.readline().decode('utf-8')
                # Actualizar la posición actual del servo2
                self.posicion_actual_servo2 = grados
                return estado_s2.strip()

        return "NO SE HA CAMBIADO LA POSICIÓN DEL SERVO2"