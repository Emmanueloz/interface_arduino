from tkinter import Tk, Frame, Label, StringVar, IntVar
from tkinter import Listbox, Scrollbar
import serial, time, threading
from ejercicio4.controlador import Controlador

class Vista:
    def __init__(self):
        self.miVentana = Tk()
        self.miVentana.title("Aplicaciones IoT")
        self.miVentana.resizable(0, 0)
        self.miVentana.geometry("320x230")

        self.estadoTemp = StringVar()
        self.estadoLumin = StringVar()
        self.estaCorriendo = True

        self.crear_widgets()

        self.miVentana.protocol('WM_DELETE_WINDOW', self.finalizar)
        self.hiloSensores = threading.Thread(target=self.leer_sensores, daemon=True)
        self.arduino = serial.Serial('COM2', 9600, timeout=1)
        time.sleep(2)

        try:
            self.hiloSensores.start()
        except Exception:
            print("No se pudo lanzar el hilo..")

        self.miVentana.mainloop()

    def finalizar(self):
        self.estaCorriendo = False
        self.hiloSensores.join(0.1)
        self.miVentana.quit()
        self.miVentana.destroy()
        self.arduino.close()

    def leer_sensores(self):
        while self.estaCorriendo:
            datos = self.arduino.readline().decode('utf-8').strip()
            if datos:
                posicion = datos.index(":")
                sensor = datos[:posicion]
                valor = datos[posicion + 1:]
                if sensor == '3':
                    self.estadoTemp.set(valor)
                    self.lstbox_temp.insert("end", valor)
                    self.lstbox_temp.see("end")
                elif sensor == '2':
                    self.estadoLumin.set(valor)
                    self.lstbox_lumin.insert("end", valor)
                    self.lstbox_lumin.see("end")

    def crear_widgets(self):
        frame1 = Frame(self.miVentana)
        frame1.pack(fill='both', expand=True)

        Label(frame1, text="..:: Temperatura y Luminosidad ::..").grid(row=0,
                                                                        column=0, columnspan=4, padx=10, pady=5,
                                                                        sticky="we")

        Label(frame1, text="Temperatura").grid(row=1, column=0, padx=10, pady=5, sticky="we")
        Label(frame1, text="Luminosidad").grid(row=1, column=2, padx=10, pady=5, sticky="we")

        Label(frame1, textvariable=self.estadoTemp, width=6, borderwidth=2, relief="groove",
              fg="green", bg="black", font=("Courier New", 15, "bold")).grid(row=2,
                                                                             column=0, padx=10, pady=5, sticky="wesn")

        Label(frame1, textvariable=self.estadoLumin, width=6, borderwidth=2, relief="groove",
              fg="red", bg="black", font=("Courier New", 15, "bold")).grid(row=2,
                                                                           column=2, padx=5, pady=5, sticky="wesn")

        scroll_temp = Scrollbar(frame1, orient="vertical")
        self.lstbox_temp = Listbox(frame1, height=5, yscrollcommand=scroll_temp.set)

        scroll_temp.grid(row=3, column=1, sticky='ns')
        self.lstbox_temp.grid(row=3, column=0, padx=5, pady=5, sticky="wesn")
        scroll_temp.configure(command=self.lstbox_temp.yview)

        scroll_lumin = Scrollbar(frame1, orient="vertical")
        self.lstbox_lumin = Listbox(frame1, height=5, yscrollcommand=scroll_lumin.set)

        scroll_lumin.grid(row=3, column=3, sticky='ns')
        self.lstbox_lumin.grid(row=3, column=2, padx=5, pady=5, sticky="wesn")

        scroll_lumin.configure(command=self.lstbox_lumin.yview)

# Inicializar la vista
vista = Vista()
