from tkinter import Tk, Frame, Label, Checkbutton, StringVar, IntVar
from .controlador import Controlador

class Vista:
    def __init__(self, ventana):
        self.miVentana = ventana
        self.miVentana.title("Aplicaciones IoT")
        self.miVentana.resizable(0, 0)
        self.miVentana.geometry("260x170")

        try:
            self.controlador = Controlador()
            self.datos = self.controlador.consultar_arduino()
        except Exception as e:
            print("Error al conectar con el controlador:", str(e))
            self.controlador = None

        self.estadoLed1 = StringVar()
        self.estadoLed2 = StringVar()
        self.estadoLed3 = StringVar()
        self.barraEstado = StringVar()
        self.led1 = IntVar()
        self.led2 = IntVar()
        self.led3 = IntVar()

        if self.datos is not None:
            if self.datos[0] == 0:
                self.estadoLed1.set("LEd 1 Apagado")
            if self.datos[0] == 1:
                self.estadoLed1.set("LEd 1 Encendido")
                self.led1.set(1)
            if self.datos[1] == 0:
                self.estadoLed2.set("LEd 2 Apagado")
            if self.datos[1] == 1:
                self.estadoLed2.set("LEd 2 Encendido")
                self.led2.set(1)
            if self.datos[2] == 0:
                self.estadoLed3.set("LEd 3 Apagado")
            if self.datos[2] == 1:
                self.estadoLed3.set("LEd 3 Encendido")
                self.led3.set(1)



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
        self.control_led(1, self.led1, self.estadoLed1)

    def control_led2(self):
        self.control_led(2, self.led2, self.estadoLed2)

    def control_led3(self):
        self.control_led(3, self.led3, self.estadoLed3)

    def control_led(self, nLed, led_var, estado_var):
        try:
            if self.controlador:
                if led_var.get() == 1:
                    if self.controlador.encender_led(nLed) == 1:
                        estado_var.set(f"Led {nLed} Encendido")
                elif led_var.get() == 0:
                    if self.controlador.apagar_led(nLed) == 0:
                        estado_var.set(f"Led {nLed} Apagado")
        except Exception as e:
            self.barraEstado.set("Error: " + str(e))

    def inicializar_leds(self):
        try:
            if self.controlador:
                # Eliminamos esta parte ya que no es necesaria
                pass
        except Exception as e:
            self.barraEstado.set("Error al conectar con Arduino: " + str(e))

miVentana = Tk()
vista = Vista(miVentana)
miVentana.mainloop()
from tkinter import Tk, Frame, Label, Checkbutton, StringVar, IntVar
from controlador import Controlador

class Vista:
    def __init__(self, ventana):
        self.miVentana = ventana
        self.miVentana.title("Aplicaciones IoT")
        self.miVentana.resizable(0, 0)
        self.miVentana.geometry("260x170")

        try:
            self.controlador = Controlador()
        except Exception as e:
            print("Error al conectar con el controlador:", str(e))
            self.controlador = None

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
        self.control_led(1, self.led1, self.estadoLed1)

    def control_led2(self):
        self.control_led(2, self.led2, self.estadoLed2)

    def control_led3(self):
        self.control_led(3, self.led3, self.estadoLed3)

    def control_led(self, nLed, led_var, estado_var):
        try:
            if self.controlador:
                if led_var.get() == 1:
                    if self.controlador.encender_led(nLed) == 1:
                        estado_var.set(f"LED {nLed} ENCENDIDO")
                    else:
                        estado_var.set(f"Error al encender LED {nLed}")
                elif led_var.get() == 0:
                    if self.controlador.apagar_led(nLed) == 0:
                        estado_var.set(f"LED {nLed} APAGADO")
                    else:
                        estado_var.set(f"Error al apagar LED {nLed}")
        except Exception as e:
            self.barraEstado.set("Error: " + str(e))

    def inicializar_leds(self):
        # No es necesario inicializar los LED aquí, ya que se manejarán dinámicamente por los botones de la interfaz.
        pass

miVentana = Tk()
vista = Vista(miVentana)
miVentana.mainloop()
