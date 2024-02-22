from tkinter import Tk, Frame, Button, Label, StringVar
from ejercicio1.robertoControlador import Controlador

class Vista:
    def __init__(self):
        self.miVentana = Tk()
        self.miVentana.title("Roberto Carlos")
        self.miVentana.resizable(0, 0)
        self.miVentana.geometry("300x150")

        self.frame1 = Frame(self.miVentana)
        self.frame1.pack(fill='both', expand=True)

        self.lbl_titulo = Label(self.frame1, text="..:: Control de LED ::..")
        self.lbl_titulo.grid(row=0, column=1, padx=5, pady=5)

        self.btn_ON = Button(self.frame1, width=10, text="Encender", fg="blue")
        self.btn_ON.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.btn_OFF = Button(self.frame1, width=10, text="Apagar", fg="red")
        self.btn_OFF.grid(row=1, column=2, padx=5, pady=5)

        self.estadoLed = StringVar()
        self.lbl_estado = Label(self.frame1, textvariable=self.estadoLed, fg="red", font=("Courier New", 14, "bold"))
        self.lbl_estado.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.barraEstado = StringVar()
        self.lbl_barraEstado = Label(self.frame1, textvariable=self.barraEstado, fg="red", font=("Courier New", 8))
        self.lbl_barraEstado.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.controlador = Controlador(self)

        self.btn_ON.config(command=self.controlador.encenderLed)
        self.btn_OFF.config(command=self.controlador.apagarLed)

    def iniciar(self):
        self.miVentana.mainloop()

vista = Vista()
vista.iniciar()
