import serial
import time
from crud import Crud

class Controlador:
    def __init__(self, port='COM2', baudrate=9600, timeout=1):
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=timeout)
            time.sleep(2)  # Esperar a que Arduino se inicialice
        except serial.SerialException as e:
            print(f"Error al conectar con el puerto {port}: {e}")
            self.arduino = None

        host = 'localhost'
        user = 'root'
        password = ''
        database = 'arduino_bd'

        self.crud = Crud(host, user, password, database)

        # Obtener el ID del componente para los LEDs
        self.id_componente_leds = self.obtener_id_componente_leds()

    def obtener_id_componente_leds(self):
        # Suponiendo que ya hay un componente LED registrado en la base de datos con el mismo ID para los 3 LEDs
        # Puedes implementar la lógica para obtener el ID del componente LED de la base de datos aquí
        return 1  # ID de ejemplo

    def _enviar_comando(self, nLed, estado):
        if self.arduino is None:
            print("No se pudo enviar el comando. Arduino no está conectado.")
            return None

        comando = f"{nLed}:{estado}"
        try:
            self.arduino.write(comando.encode())
            time.sleep(0.1)
            respuesta = self.arduino.readline().decode("utf-8").strip()
            valor = int(respuesta)
            
            # Insertar registro en la tabla de registros
            if valor is not None:
                fecha = time.strftime('%Y-%m-%d')
                hora = time.strftime('%H:%M:%S')
                self.crud.insert_registro(self.id_componente_leds, valor, fecha, hora)
            
            return valor
        except (ValueError, serial.SerialException) as e:
            print(f"Error: {e}")
            return None

    def encender_led(self, nLed):
        try:
            nLed = int(nLed)
            if nLed < 0:
                raise ValueError("Número de LED no puede ser negativo.")
        except ValueError as e:
            print(f"Error: {e}")
            return None
        return self._enviar_comando(nLed, 1)

    def apagar_led(self, nLed):
        try:
            nLed = int(nLed)
            if nLed < 0:
                raise ValueError("Número de LED no puede ser negativo.")
        except ValueError as e:
            print(f"Error: {e}")
            return None
        return self._enviar_comando(nLed, 0)