from serial import Serial,SerialException
from time import sleep

class ArduinoSerial:
    arduino: Serial = None
    # Constructor

    def __init__(self, puerto, velocidad=9600, time=2):
        self.puerto = puerto
        self.velocidad = velocidad
        self.time = time

    def conectar(self):
        try:
            self.arduino = Serial(
                port=self.puerto, baudrate=self.velocidad,)
            sleep(2)
        except SerialException as e:
            return f"Error en la conexión: {e}"

    def enviar_dato(self, dato):
        try:
            self.arduino.write(dato.encode())
        except Exception as e:
            return f"Error el arduino no esta conectado: {e}"

    def recibir_dato(self):
        try:
            # recibir_dato = self.arduino.readline().decode().strip()
            result = []
            while self.arduino.in_waiting > 0:
                result.append(self.arduino.readline().decode("utf-8").strip())
            # print(result)
            return result[-1]
        except Exception as e:
            return f"Error al recibir los datos: {e}"

    def cerrar_arduino(self):
        if self.arduino is not None:
            if self.arduino.is_open:
                self.arduino.close()
                return "Conexión cerrada"
            else:
                return "El puerto ya esta cerrado"
        else:
            return "Arduino no conectado"
