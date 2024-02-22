import serial
import time
from crud import Crud

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.crud = Crud("tu_host", "tu_usuario", "tu_contraseña", "tu_base_de_datos")
        self.crud.init_connection()
        self.led_encendido = False
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
        if not self.led_encendido:
            self.arduino.write(b'e')
            time.sleep(0.5)
            valor = int(self.arduino.readline().decode('utf-8'))
            print(valor)
            if valor == 1:
                self.vista.estadoLed.set("LED ENCENDIDO")
                self.vista.barraEstado.set("")
                self.crud.insert_registro_led(idComponente = 1, accion="Encendido")
                self.led_encendido = True
        else:
            print("El led esta encendido nose guardo ningun registro")

    def apagarLed(self):
        if self.led_encendido:
            self.arduino.write(b'a')
            time.sleep(0.5)
            valor = int(self.arduino.readline().decode('utf-8'))
            print(valor)
            if valor == 0:
                self.vista.estadoLed.set("LED APAGADO")
                self.vista.barraEstado.set("")
                self.crud.insert_registro_led(idComponente=1, accion="Apagado")
                self.led_encendido = False
        else:
            print("El led esta apagado nose guardo ningun registro")

            
    
    def __del__(self):
        self.crud.close_connection()
