import serial
import time

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        try:
            self.arduino = serial.Serial('COM2', 9600, timeout=1)
            time.sleep(2)
            print(self.arduino)
            self.arduino.write(b'E')
            time.sleep(0.1)
            valor = int(self.arduino.readline().decode('utf-8'))
            print(valor)
            if valor == 0:
                self.vista.estadoLed.set("LED APAGADO")
            elif valor == 1:
                self.vista.estadoLed.set("LED ENCENDIDO")
        except Exception as e:
            print("No se pudo conectar con Arduino:", e)
            self.vista.barraEstado.set("No se pudo conectar con Arduino")

    def encenderLed(self):
        self.arduino.write(b'e')
        time.sleep(0.5)
        valor = int(self.arduino.readline().decode('utf-8'))
        print(valor)
        if valor == 1:
            self.vista.estadoLed.set("LED ENCENDIDO")
            self.vista.barraEstado.set("")

    def apagarLed(self):
        self.arduino.write(b'a')
        time.sleep(0.5)
        valor = int(self.arduino.readline().decode('utf-8'))
        print(valor)
        if valor == 0:
            self.vista.estadoLed.set("LED APAGADO")
            self.vista.barraEstado.set("")
