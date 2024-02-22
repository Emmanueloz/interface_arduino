import serial
import time
from crud import Crud

class Controlador:
    def __init__(self, vista):
        host = 'localhost'
        user = 'root'
        password = ''
        database = 'arduino_bd'
        self.vista = vista
        self.crud = Crud(host, user, password, database)
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

    def buscar_id_componente(self):
        try:
            resultado,error = self.crud.select_componentes_tipo_nombre('actuador','led')
            if resultado is None:
                id_actuador_led = resultado[0]
                return id_actuador_led
            else:
                id_componente, error = self.crud.insert_componente(
                    tipo = "actuador", nombre="led", descripcion="se registro"
                ) 
                return id_componente
        except:
            print("error")
            

    def encenderLed(self):
        if not self.led_encendido:
            self.arduino.write(b'e')
            time.sleep(0.5)
            valor = int(self.arduino.readline().decode('utf-8'))
            print(valor)
            if valor == 1:
                self.vista.estadoLed.set("LED ENCENDIDO")
                self.vista.barraEstado.set("")
                idComponente = self.buscar_id_componente()
                self.crud.insert_registro_led(idComponente = idComponente, accion="Encendido")
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
                idComponente = self.buscar_id_componente()
                self.crud.insert_registro_led(idComponente=idComponente, accion="Apagado")
                self.led_encendido = False
        else:
            print("El led esta apagado nose guardo ningun registro")

            
    
    def __del__(self):
        self.crud.close_connection()
