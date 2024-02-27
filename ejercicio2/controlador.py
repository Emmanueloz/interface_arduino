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

        self.crud = Crud('localhost', 'root', '123456', 'arduino_bd', '3308')

        if self.arduino is None:
            print("No se puede continuar. Arduino no está conectado.")
            return

        if not self.crud.init_connection()[0]:
            print("No se puede continuar. Error al conectar con la base de datos.")
            return

        self.id_componente_leds = self.obtener_o_crear_ids_componentes_leds()

    def __del__(self):
        if self.arduino:
            self.arduino.close()
            print("Puerto serial cerrado.")

    def obtener_o_crear_ids_componentes_leds(self):
        ids_leds = []
        for i in range(1, 4):
            nombre_led = f"led_{i}_raul"
            componente, error = self.crud.select_componentes_tipo_nombre("actuador", nombre_led)
            if componente:
                ids_leds.append(componente[0])
            else:
                id_componente, error = self.crud.insert_componente(
                    "actuador", nombre_led, f"Descripción del LED {i}")
                if id_componente:
                    print(f"Componente LED insertado con ID: {id_componente}")
                    ids_leds.append((id_componente,))
                else:
                    print(f"Error al insertar componente LED {i}: {error}")
        return ids_leds

    def _enviar_comando(self, nLed, estado):
        try:
            if not self.arduino.is_open:
                print("El puerto serial está cerrado.")
                return None

            if not 0 < nLed <= len(self.id_componente_leds):
                print(f"Número de LED fuera de rango. Solo se permiten LEDs del 1 al {len(self.id_componente_leds)}.")
                return None

            id_componente = self.id_componente_leds[nLed - 1]
            comando = f"{nLed}:{estado}"
            self.arduino.write(comando.encode())
            time.sleep(0.1)
            respuesta = self.arduino.readline().decode("utf-8").strip()
            valor = int(respuesta)

            id_registro, error = self.crud.insert_registro(id_componente, valor)
            if id_registro:
                print("Registro insertado en la base de datos.")
            else:
                print(f"Error al insertar registro en la base de datos: {error}")

            print(f"Respuesta de Arduino: {valor}")
            return valor
        except (ValueError, serial.SerialException) as e:
            print(f"Error al enviar el comando: {e}")
            return None

    def encender_led(self, nLed):
        try:
            nLed = int(nLed)
            if nLed <= 0:
                raise ValueError("Número de LED debe ser un entero positivo.")
            return self._enviar_comando(nLed, 1)
        except ValueError as e:
            print(f"Error: {e}")
            return None

    def apagar_led(self, nLed):
        try:
            nLed = int(nLed)
            if nLed <= 0:
                raise ValueError("Número de LED debe ser un entero positivo.")
            return self._enviar_comando(nLed, 0)
        except ValueError as e:
            print(f"Error: {e}")
            return None
