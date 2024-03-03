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
        # Insertar un componente para cada LED si no existen
        self.id_componentes_led = {}  # Inicializar el diccionario
        for num_led in range(1, 4):
            nombre_led = f"led_{num_led}_Raul"
            id_componente, error = self.crud.select_componentes_tipo_nombre("actuador", nombre_led)
            if error:
                print(f"Error al consultar componente {nombre_led}: {error}")
                continue

            if id_componente:
                print(f"ID del componente {nombre_led} encontrado: {id_componente[0]}")
                self.id_componentes_led[nombre_led] = id_componente[0]
            else:
                print(f"No se encontró el componente {nombre_led} en la base de datos. Insertando...")

                # Insertar el componente en la base de datos si no existe
                descripcion_led = f"Descripción del LED {num_led}"
                id_componente_insertado, error_insertar = self.crud.insert_componente("actuador", nombre_led, descripcion_led)
                if id_componente_insertado:
                    print(f"Componente {nombre_led} insertado con ID: {id_componente_insertado}")
                    self.id_componentes_led[nombre_led] = id_componente_insertado  # Guardar el ID en el diccionario
                else:
                    print(f"Error al insertar componente {nombre_led}: {error_insertar}")

        # Insertar nuevos componentes si no se encontraron componentes LED
        if not self.id_componentes_led:
            try:
                for num_led in range(1, 4):
                    nombre_led = f"led_{num_led}_Raul"
                    descripcion_led = f"Descripción del LED {num_led}"
                    id_componente_insertado, error_insertar = self.crud.insert_componente("actuador", nombre_led, descripcion_led)
                    if id_componente_insertado:
                        print(f"Componente {nombre_led} insertado con ID: {id_componente_insertado}")
                        self.id_componentes_led[nombre_led] = id_componente_insertado  # Guardar el ID en el diccionario
                    else:
                        print(f"Error al insertar componente {nombre_led}: {error_insertar}")
            except Exception as e:
                print(f"Error al insertar componentes: {e}")

    def mostrar_registros_leds(self):
        registros_led1, error_led1 = self.crud.select_registros(tipo='actuador', nombre='led_1_Raul')
        registros_led2, error_led2 = self.crud.select_registros(tipo='actuador', nombre='led_2_Raul')
        registros_led3, error_led3 = self.crud.select_registros(tipo='actuador', nombre='led_3_Raul')

        if error_led1 or error_led2 or error_led3:
            return None, f"Error al obtener los registros: {error_led1 or error_led2 or error_led3}"

        return registros_led1, registros_led2, registros_led3, None

    def consultar_arduino(self):
        if self.arduino is None:
            print("Error: Arduino no está conectado.")
            return None

        try:
            self.arduino.write('4:0'.encode())
            time.sleep(0.1)
            datos = self.arduino.readline().decode('utf-8')
            print(datos)
            if datos:
                return eval(datos)
            return None 
        except serial.SerialException as e:
            print(f"Error al consultar Arduino: {e}")
            return None

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
        if self.arduino is None:
            print("No se puede enviar el comando. Arduino no está conectado.")
            return None

        comando = f"{nLed}:{estado}"
        try:
            if self.arduino.is_open:
                print(f"Enviando comando a Arduino: {comando}")
                self.arduino.write(comando.encode())
                time.sleep(0.1)
                respuesta = self.arduino.readline().decode("utf-8").strip()
                valor = int(respuesta)
                if valor is not None:
                    print(self.id_componentes_led)
                    result, error = self.crud.insert_registro(self.id_componentes_led[f'led_{nLed}_Raul'], valor)

                print(f"Respuesta de Arduino: {valor}")
                return valor
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
            if nLed < 0:
                raise ValueError("Número de LED no puede ser negativo.")
            if f"led_{nLed}_Raul" not in self.id_componentes_led:
                raise ValueError("ID de componente no encontrado para el LED especificado.")
        except ValueError as e:
            print(f"Error: {e}")
            return None
        
        return self._enviar_comando(nLed, 1)

    def apagar_led(self, nLed):
        try:
            nLed = int(nLed)
            if nLed <= 0:
                raise ValueError("Número de LED debe ser un entero positivo.")
            return self._enviar_comando(nLed, 0)
            if nLed < 0:
                raise ValueError("Número de LED no puede ser negativo.")
            if f"led_{nLed}_Raul" not in self.id_componentes_led:
                raise ValueError("ID de componente no encontrado para el LED especificado.")
        except ValueError as e:
            print(f"Error: {e}")
            return None
