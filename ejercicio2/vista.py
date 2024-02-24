from tkinter import *
from .controlador import Controlador

class Vista:
    def __init__(self, ventana):
        self.miVentana = ventana
        self.miVentana.title("Aplicaciones IoT")
        self.miVentana.resizable(0, 0)
        self.miVentana.geometry("260x170")

        self.controlador = Controlador()

        self.estadoLed1 = StringVar()
        self.estadoLed2 = StringVar()
        self.estadoLed3 = StringVar()
        self.barraEstado = StringVar()
        self.led1 = IntVar()
        self.led2 = IntVar()
        self.led3 = IntVar()

        self.frame1 = Frame(self.miVentana)
        self.frame1.pack(fill='both', expand=True)

        Label(self.frame1, text="..:: Control de 3 Leds ::..").grid(row=0, column=0, columnspan=2, padx=5, pady=5,
                                                                    sticky="we")
        Checkbutton(self.frame1, text="Led 1", variable=self.led1, onvalue=1,
                    offvalue=0, command=self.control_led1).grid(row=1, column=0, padx=10, pady=10)
        Checkbutton(self.frame1, text="Led 2", variable=self.led2, onvalue=1,
                    offvalue=0, command=self.control_led2).grid(row=2, column=0, padx=10, pady=10)
        Checkbutton(self.frame1, text="Led 3", variable=self.led3, onvalue=1,
                    offvalue=0, command=self.control_led3).grid(row=3, column=0, padx=10, pady=10)

        Label(self.frame1, textvariable=self.estadoLed1, width=20, borderwidth=2, relief="groove", fg="green",
              font=("Courier new", 10, "bold"), anchor='w').grid(row=1, column=1, padx=5, pady=5, sticky="w") 
        Label(self.frame1, textvariable=self.estadoLed2, width=20, borderwidth=2, relief="groove", fg="orange",
              font=("Courier new", 10, "bold"), anchor='w').grid(row=2, column=1, padx=5, pady=5, sticky="w")
        Label(self.frame1, textvariable=self.estadoLed3, width=20, borderwidth=2, relief="groove", fg="red",
              font=("Courier new", 10, "bold"), anchor='w').grid(row=3, column=1, padx=5, pady=5, sticky="w")
        Label(self.frame1, textvariable=self.barraEstado, width=20, bd=2, fg="red").grid(row=4,
                                                                                         column=1, columnspan=2,
                                                                                         padx=5, pady=5, sticky="we")

        self.inicializar_leds()

    def control_led1(self):
        try:
            if self.led1.get() == 1:
                if self.controlador.encender_led(1) == 1:
                    self.estadoLed1.set("Led 1 Encendido")
            elif self.led1.get() == 0:
                if self.controlador.apagar_led(1) == 0:
                    self.estadoLed1.set("Led 1 Apagado")
        except Exception as e:
            self.barraEstado.set("Error: " + str(e))

    def control_led2(self):
        try:
            if self.led2.get() == 1:
                if self.controlador.encender_led(2) == 1:
                    self.estadoLed2.set("Led 2 Encendido")
            elif self.led2.get() == 0:
                if self.controlador.apagar_led(2) == 0:
                    self.estadoLed2.set("Led 2 Apagado")
        except Exception as e:
            self.barraEstado.set("Error: " + str(e))

    def control_led3(self):
        try:
            if self.led3.get() == 1:
                if self.controlador.encender_led(3) == 1:
                    self.estadoLed3.set("Led 3 Encendido")
            elif self.led3.get() == 0:
                if self.controlador.apagar_led(3) == 0:
                    self.estadoLed3.set("Led 3 Apagado")
        except Exception as e:
            self.barraEstado.set("Error: " + str(e))

    def inicializar_leds(self):
        try:
            datos = self.controlador.arduino.readline().decode('utf-8')
            if datos:
                estados = eval(datos)
                self.estadoLed1.set("Led 1 Encendido" if estados[0] == 1 else "Led 1 Apagado")
                self.estadoLed2.set("Led 2 Encendido" if estados[1] == 1 else "Led 2 Apagado")
                self.estadoLed3.set("Led 3 Encendido" if estados[2] == 1 else "Led 3 Apagado")
                self.led1.set(estados[0])
                self.led2.set(estados[1])
                self.led3.set(estados[2])
        except Exception as e:
            self.barraEstado.set("Error al conectar con Arduino: " + str(e))


miVentana = Tk()
vista = Vista(miVentana)
miVentana.mainloop()
