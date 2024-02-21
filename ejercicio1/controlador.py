import serial
import time
from tkinter import StringVar
from vista import miVentana, btn_ON, btn_OFF, lbl_estado, lbl_barraEstado

class Controlador:
    def __init__(self):
        self.estadoLed = StringVar()
        self.barraEstado = StringVar()

        self.arduino = serial.Serial('COM2', 9600, timeout=1)
        time.sleep(2)
        print(self.arduino)
        self.arduino.write("E".encode())
        time.sleep(0.1)
        valor = int(self.arduino.readline().decode('utf-8'))
        print(valor)
        if valor == 0:
            self.estadoLed.set("LED APAGADO")
        elif valor == 1:
            self.estadoLed.set("LED ENCENDIDO")

        lbl_estado.config(textvariable=self.estadoLed)
        lbl_barraEstado.config(textvariable=self.barraEstado)

        btn_ON.config(command=self.encenderLed)
        btn_OFF.config(command=self.apagarLed)

    def encenderLed(self):
        self.arduino.write("e".encode())
        time.sleep(0.5)
        valor = int(self.arduino.readline().decode('utf-8'))
        print(valor)
        if valor == 1:
            self.estadoLed.set("LED ENCENDIDO")
            self.barraEstado.set("")

    def apagarLed(self):
        self.arduino.write("a".encode())
        time.sleep(0.5)
        valor = int(self.arduino.readline().decode('utf-8'))
        print(valor)
        if valor == 0:
            self.estadoLed.set("LED APAGADO")
            self.barraEstado.set("")

controlador = Controlador()
miVentana.mainloop()
