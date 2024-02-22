from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
import serial
import time
import threading

class Vista:
    def __init__(self):
        self.miVentana = Tk()
        self.miVentana.title("Aplicaciones Iot")
        self.miVentana.resizable(0,0)
        self.miVentana.geometry("320x230")

        self.estadoTemp = StringVar()
        self.estadoLumin = StringVar()
        self.barraEstado = StringVar()
        self.estaCorriendo = True

        self.frame1 = Frame(self.miVentana)
        self.frame1.pack(fill='both', expand=True)

        Label(self.frame1, text="..:: Temperatura y luminosidad ::..").grid(row=0,
                column=0, columnspan=4, padx=10, pady=5, sticky="we")
        Label(self.frame1, text="Temperatura").grid(row=1, column=0, padx=10, pady=5, sticky="we")
        Label(self.frame1, text="Luminosidad").grid(row=1, column=2, padx=10, pady=5, sticky="we")

        Label(self.frame1, textvariable=self.estadoTemp, width=6, borderwidth=2, relief="groove",
                fg="green", bg="black", font=("Courier New",15, "bold")).grid(row=2,
                column=0, padx=10, pady=5,  sticky="wesn")

        Label(self.frame1, textvariable=self.estadoLumin, width=6, borderwidth=2, relief="groove",
                fg="red", bg="black", font=("Courier New",15, "bold")).grid(row=2,
                column=2, padx=10, pady=5,  sticky="wesn")
                
        self.scroll_temp = Scrollbar(self.frame1, orient="vertical")
        self.lstbox_temp = Listbox(self.frame1, height=5, yscrollcommand=self.scroll_temp.set)

        self.scroll_temp.grid(row=3, column=1, sticky='ns')
        self.lstbox_temp.grid(row=3, column=0, padx=5, pady=5, sticky="wesn")
        self.scroll_temp.configure(command=self.lstbox_temp.yview)

        self.scroll_lumin = Scrollbar(self.frame1, orient="vertical")
        self.lstbox_lumin = Listbox(self.frame1, height=5, yscrollcommand=self.scroll_lumin.set)

        self.scroll_lumin.grid(row=3, column=3, sticky='ns')
        self.lstbox_lumin.grid(row=3, column=2, padx=5, pady=5, sticky="wesn")
        self.scroll_lumin.configure(command=self.lstbox_lumin.yview)

        Label(self.frame1, textvariable=self.barraEstado, width=20, bd=2, fg="red").grid(row=5,
                column=0, columnspan=4, padx=5, pady=10, sticky="we")

        self.miVentana.protocol('WM_DELETE_WINDOW', self.finalizar)
        self.hiloSensores = threading.Thread(target=self.leerSensores, daemon=True)
        self.arduino = serial.Serial('COM2', 9600, timeout=1)
        time.sleep(2)
        print(self.arduino)

        self.arduino.write("1:0".encode())
        time.sleep(0.1)
        datos = self.arduino.readline().decode('utf-8')
        print(datos)
        if datos:
            print("datos recibidos...")
            estados = eval(datos) # convertir un String en una Tupla
            
            self.estadoTemp.set(estados[0])
            self.estadoLumin.set(estados[1])
        else:
            print("No se recibieron datos..")
            self.barraEstado.set("ERROR al conectar con Arduino")
        
        try:
            self.hiloSensores.start()
        except Exception:
            print("No se pudo lanzar el hilo..")

    def finalizar(self):
        self.estaCorriendo = False
        self.hiloSensores.join(0.1)
        self.miVentana.quit()
        self.miVentana.destroy()
        self.arduino.close
