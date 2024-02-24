import serial
import time
from crud import Crud

class Controlador:
    def __init__(self, port='COM2', baudrate=9600, timeout=1):
        try:
            self.arduino = serial.Serial(port, baudrate, timeout=timeout)
            time.sleep(2)
            print(f"Conexión establecida con Arduino en el puerto {port}")
        except serial.SerialException as e:
            print(f"Error al conectar con el puerto {port}: {e}")
            self.arduino = None

        self.crud = Crud('localhost', 'root', '123456', 'arduino_bd', port=3308)

        result, error = self.crud.init_connection()
        if result:
            print("Conexión establecida con la base de datos")
        else:
            print(f"Error al conectar con la base de datos: {error}")
            return

        # Insertar un único componente para los tres LEDs
        try:
            id_componente, error = self.crud.insert_componente(
                "actuador", "led", "Descripción del LED")
            if id_componente:
                print(f"Componente LED insertado con ID: {id_componente}")
                # Asignar el mismo idComponente para los tres LEDs
                self.id_componente_led = id_componente
            else:
                print(f"Error al insertar componente LED: {error}")
        except Exception as e:
            print(f"Error al insertar componente: {e}")

    def _enviar_comando(self, nLed, estado):
        if self.arduino is None:
            print("No se puede enviar el comando. Arduino no está conectado.")
            return None

        comando = f"{nLed}:{estado}"  # No es necesario especificar un componente
        try:
            if self.arduino.is_open:
                print(f"Enviando comando a Arduino: {comando}")
                self.arduino.write(comando.encode())
                time.sleep(0.1)
                respuesta = self.arduino.readline().decode("utf-8").strip()
                valor = int(respuesta)
                if valor is not None:
                    self.crud.insert_registro(self.id_componente_led, valor)
                print(f"Respuesta de Arduino: {valor}")
                return valor
            else:
                print("El puerto serial está cerrado.")
                return None
        except (ValueError, serial.SerialException) as e:
            print(f"Error al enviar el comando: {e}")
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