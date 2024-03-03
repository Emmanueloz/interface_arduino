import time
from crud import Crud
from arduno import ArduinoSerial

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
            ##self.arduino = arduno.Serial('COM2', 9600, timeout=1)
            self.arduino = ArduinoSerial('COM2', 9600, 1)
            self.arduino.conectar()
            time.sleep(1)
            print(self.arduino.arduino)
            #self.arduino.write(b'E')
            self.arduino.enviar_dato('E')
            time.sleep(0.1)
            #valor = int(self.arduino.readline().decode('utf-8'))
            valor = int(self.arduino.recibir_dato())
            print(valor)
            if valor == 0:
                self.vista.estadoLed.set("LED APAGADO")
            elif valor == 1:
                self.led_encendido =True
                self.vista.estadoLed.set("LED ENCENDIDO")
        except Exception as e:
            print("No se pudo conectar con Arduino:", e)
            self.vista.barraEstado.set("No se pudo conectar con Arduino")

    def buscar_id_componente(self):
        try:
            resultado,error = self.crud.select_componentes_tipo_nombre('actuador','ledroberto')
            if resultado is None:
                id_componente, error = self.crud.insert_componente(
                    tipo = "actuador", nombre="ledroberto", descripcion="se registro"
                )
                return id_componente
            
            id_componente = resultado[0]
            return id_componente
        except:
            print("error")
    
    def mostrar_registros_led(self):
        resultado_led, error = self.crud.select_registros(tipo='actuador', nombre='ledroberto')

        if error:
            return None, f"Error al obtener los registros: {error}"
        
        return resultado_led, None
            

    def encenderLed(self):
        if not self.led_encendido:
            ##self.arduino.write(b'e')
            self.arduino.enviar_dato('e')
            time.sleep(0.5)
            #valor = int(self.arduino.readline().decode('utf-8'))
            valor = int(self.arduino.recibir_dato())
            print(valor)
            if valor == 1:
                self.vista.estadoLed.set("LED ENCENDIDO")
                self.vista.barraEstado.set("")
                idComponente = self.buscar_id_componente()
                self.crud.insert_registro(idComponente = idComponente, valor=valor)
                self.led_encendido = True
        else:
            print("El led esta encendido nose guardo ningun registro")

    def apagarLed(self):
        if self.led_encendido:
            #self.arduino.write(b'a')
            self.arduino.enviar_dato('a')
            time.sleep(0.5)
            #valor = int(self.arduino.readline().decode('utf-8'))
            valor = int(self.arduino.recibir_dato())
            print(valor)
            if valor == 0:
                self.vista.estadoLed.set("LED APAGADO")
                self.vista.barraEstado.set("")
                idComponente = self.buscar_id_componente()
                self.crud.insert_registro(idComponente=idComponente, valor=valor)
                self.led_encendido = False
        else:
            print("El led esta apagado nose guardo ningun registro")

            
    
    def __del__(self):
        self.crud.close_connection()
