import threading
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
        self.estaCorriendo = False       
        try:
            self.arduino = serial.Serial('COM2', 9600, timeout=1)
            time.sleep(2)
            print(self.arduino)           
            self.hiloSensores = threading.Thread(target=self.leer_sensores, daemon=True)
            self.hiloSensores.start()
        except Exception as e:
            print("No se puede conectar con Arduino:", e)
            self.vista.estadoTemp.set("No se puede conectar con Arduino")
            self.vista.estadoLumin.set("No se puede conectar con Arduino")
    
    def leer_sensores(self):
        while self.estaCorriendo:
            datos = self.arduino.readline().decode('utf-8').strip()
            if datos:
                posicion = datos.index(":")
                sensor = datos[:posicion]
                valor = datos[posicion + 1:]
                if sensor == '3':
                    self.vista.estadoTemp.set(valor)
                    self.vista.lstbox_temp.insert("end", valor)
                    self.vista.lstbox_temp.see("end")
                    # Insertar registro en la base de datos
                    idComponente = 1  # Suponiendo que el componente de temperatura tiene ID 1
                    self.crud.insert_registro(idComponente, float(valor))
                elif sensor == '2':
                    self.vista.estadoLumin.set(valor)
                    self.vista.lstbox_lumin.insert("end", valor)
                    self.vista.lstbox_lumin.see("end")
                    # 
                    idComponente = 2  # 
                    self.crud.insert_registro(idComponente, float(valor))

    def __del__(self):
        self.estaCorriendo = False
        self.crud.close_connection()