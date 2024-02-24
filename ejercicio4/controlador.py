import threading
import serial
import time
from crud import Crud
from ejercicio4.vista import Vista

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.crud = Crud('', '', '', '')
        self.crud.init_connection()
        self.estaCorriendo = True

        self.hiloSensores = threading.Thread(target=self.leerSensores, daemon=True)
        self.arduino = serial.Serial('COM2', 9600, timeout=1)
        time.sleep(2)
        print(self.arduino)

        self.arduino.write("1:0".encode())
        time.sleep(0.1)
        datos = self.arduino.readline().decode('utf-8')
        print(datos)
        if datos:
            print("Datos recibidos..")
            estados = eval(datos)  # Convertir un String en una Tupla
            self.vista.estadoTemp.set(estados[0])
            self.vista.estadoLumin.set(estados[1])
        else:
            print("No se recibieron datos..")
            self.vista.barraEstado.set("Error al conectar con Arduino")

        self.vista.miVentana.protocol('WM_DELETE_WINDOW', self.finalizar)
        self.hiloSensores.start()

    def finalizar(self):
        self.estaCorriendo = False
        self.hiloSensores.join(0.1)
        self.vista.miVentana.quit()
        self.vista.miVentana.destroy()
        self.arduino.close()

    def leerSensores(self):
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
                elif sensor == '2':
                    self.vista.estadoLumin.set(valor)
                    self.vista.lstbox_lumin.insert("end", valor)
                    self.vista.lstbox_lumin.see("end")

controlador = Controlador(Vista)