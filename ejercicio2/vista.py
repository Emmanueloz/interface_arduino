from tkinter import Button, Checkbutton, Scrollbar, Tk, Frame, Label, StringVar, IntVar, ttk
from .controlador import Controlador

class Vista:
    def __init__(self, ventana):
        self.miVentana = ventana
        self.miVentana.title("Raul de Jesus Najera Jimenez")
        self.miVentana.resizable(0, 0)
        self.miVentana.geometry("400x200")

        try:
            self.controlador = Controlador()
            self.datos = self.controlador.consultar_arduino()
        except Exception as e:
            print("Error al conectar con el controlador:", str(e))
            self.controlador = None
            self.datos = None

        self.estadoLed1 = StringVar()
        self.estadoLed2 = StringVar()
        self.estadoLed3 = StringVar()
        self.barraEstado = StringVar()
        self.led1 = IntVar()
        self.led2 = IntVar()
        self.led3 = IntVar()

        if self.datos is not None:
            if self.datos[0] == 0:
                self.estadoLed1.set("Led 1 Apagado")
            if self.datos[0] == 1:
                self.estadoLed1.set("Led 1 Encendido")
                self.led1.set(1)
            if self.datos[1] == 0:
                self.estadoLed2.set("Led 2 Apagado")
            if self.datos[1] == 1:
                self.estadoLed2.set("Led 2 Encendido")
                self.led2.set(1)
            if self.datos[2] == 0:
                self.estadoLed3.set("Led 3 Apagado")
            if self.datos[2] == 1:
                self.estadoLed3.set("Led 3 Encendido")
                self.led3.set(1)

        notebook = ttk.Notebook(self.miVentana)
        notebook.pack(fill='both', expand=True)

        self.frame1 = Frame(notebook)
        self.frame2 = Frame(notebook)

        notebook.add(self.frame1, text='Inicio')
        notebook.add(self.frame2, text='Registros')

        Label(self.frame1, text="..:: Control de 3 Leds ::..").grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")
        Checkbutton(self.frame1, text="Led 1", variable=self.led1, onvalue=1, offvalue=0, command=self.control_led1).grid(row=1, column=0, padx=10, pady=10)
        Checkbutton(self.frame1, text="Led 2", variable=self.led2, onvalue=1, offvalue=0, command=self.control_led2).grid(row=2, column=0, padx=10, pady=10)
        Checkbutton(self.frame1, text="Led 3", variable=self.led3, onvalue=1, offvalue=0, command=self.control_led3).grid(row=3, column=0, padx=10, pady=10)

        Label(self.frame1, textvariable=self.estadoLed1, width=20, borderwidth=2, relief="groove", fg="green", font=("Courier new", 10, "bold"), anchor='w').grid(row=1, column=1, padx=5, pady=5, sticky="w") 
        Label(self.frame1, textvariable=self.estadoLed2, width=20, borderwidth=2, relief="groove", fg="orange", font=("Courier new", 10, "bold"), anchor='w').grid(row=2, column=1, padx=5, pady=5, sticky="w")
        Label(self.frame1, textvariable=self.estadoLed3, width=20, borderwidth=2, relief="groove", fg="red", font=("Courier new", 10, "bold"), anchor='w').grid(row=3, column=1, padx=5, pady=5, sticky="w")
        Label(self.frame1, textvariable=self.barraEstado, width=20, bd=2, fg="red").grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="we")

        self.actualizar_registros()

        scroll_dato = Scrollbar(self.frame2, orient="vertical")
        self.tree = ttk.Treeview(self.frame2,height=5, yscrollcommand=scroll_dato.set)
        scroll_dato.grid(row=1, column=4, sticky='ns')
        scroll_dato.configure(command=self.tree.yview)
        self.tree.grid(row=1, column=0, columnspan=4, padx=5, sticky="we")

        self.tree["columns"] = ("Led", "Valor", "Fecha", "Hora")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("Led", anchor="center", width=60)
        self.tree.column("Fecha", anchor="center", width=80)
        self.tree.column("Hora", anchor="center", width=90)
        self.tree.column("Valor", anchor="center", width=90)
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("Led", text="Led", anchor="center")
        self.tree.heading("Valor", text="Valor", anchor="center")
        self.tree.heading("Fecha", text="Fecha", anchor="center")
        self.tree.heading("Hora", text="Hora", anchor="center")

        Button(self.frame2, text="Actualizar", command=self.actualizar_registros).grid(row=0, column=0, padx=5, pady=5, sticky="w")

    def actualizar_registros(self):
        try:
            registros_led1, registros_led2, registros_led3, error = self.controlador.mostrar_registros_leds()
            if error:
                self.barraEstado.set("Error al obtener registros: " + error)
                return

            # Limpiamos el árbol antes de agregar los nuevos registros
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Agregamos los registros al árbol
            for registro in registros_led1:
                self.tree.insert("", "end", values=("Led 1", registro[0], registro[1], registro[2]))
            for registro in registros_led2:
                self.tree.insert("", "end", values=("Led 2", registro[0], registro[1], registro[2]))
            for registro in registros_led3:
                self.tree.insert("", "end", values=("Led 3", registro[0], registro[1], registro[2]))
        except Exception as e:
            self.barraEstado.set("Error al actualizar registros: " + str(e))

    def control_led1(self):
        self.control_led(1, self.led1, self.estadoLed1)

    def control_led2(self):
        self.control_led(2, self.led2, self.estadoLed2)

    def control_led3(self):
        self.control_led(3, self.led3, self.estadoLed3)

    def control_led(self, nLed, led_var, estado_var):
        try:
            if led_var.get() == 1:
                if self.controlador.encender_led(nLed) == 1:
                    estado_var.set(f"Led {nLed} Encendido")
            elif led_var.get() == 0:
                if self.controlador.apagar_led(nLed) == 0:
                    estado_var.set(f"Led {nLed} Apagado")
        except Exception as e:
            self.barraEstado.set("Error: " + str(e))

            # Actualizar el texto del Label según el estado del LED
            if led_var.get() == 1:
                estado_var.set(f"Led {nLed} Encendido")
            else:
                estado_var.set(f"Led {nLed} Apagado")

miVentana = Tk()
vista = Vista(miVentana)
miVentana.mainloop()
