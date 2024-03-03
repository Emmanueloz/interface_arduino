from tkinter import Tk, Frame, Button, Label, StringVar, Scrollbar
from ejercicio1.controlador import Controlador
from tkinter import ttk 
import tkinter
class Vista:
    def __init__(self):
        self.miVentana = Tk()
        self.miVentana.title("Roberto Carlos Nuñez Cruz")
        self.miVentana.resizable(0, 0)
        self.miVentana.geometry("350x200")

        # Cargar el icono desde un archivo PNG
        try:
            icono = tkinter.PhotoImage(file="ejercicio1/imagenes/led.png")
            self.miVentana.iconphoto(True, icono)
        except tkinter.TclError as e:
            print("No se pudo cargar el icono:", e)

        self.frame1 = Frame(self.miVentana)
        self.frame1.pack(fill='both', expand=True)

        #Pestañas agregadas

        self.notebook = ttk.Notebook(self.miVentana)
        self.notebook.pack(fill='both', expand=True)

        self.frame1 = Frame(self.notebook)
        self.frame2 = Frame(self.notebook)

        self.notebook.add(self.frame1, text='Inicio') 
        self.notebook.add(self.frame2, text='Registros') 
        

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

        def actualizar_registros():
            for item in tree.get_children():
                tree.delete(item)
            registros_led, error = self.controlador.mostrar_registros_led()
            for registro in registros_led:
                tree.insert("", "end", values=("Led", registro[0], registro[1], registro[2])) 



        #Scrollbar
        scroll_dato = Scrollbar(self.frame2, orient = "vertical")
        scroll_dato.grid(row= 1, column = 4, sticky='ns')        
        #Columnas para que los registros se muestren
        tree = ttk.Treeview(self.frame2 , height=5, yscrollcommand=scroll_dato.set)
        scroll_dato.configure(command=tree.yview)
        tree.grid(row=1, column=0, columnspan=4, padx=5, sticky="we")
        tree["columns"] = ("Actuador", "Valor", "Fecha", "Hora")
        tree.column("#0", width=0, stretch="no")
        tree.column("Actuador", anchor="center", width="90")
        tree.column("Fecha", anchor="center", width="80")
        tree.column("Hora", anchor="center", width="85")
        tree.column("Valor", anchor="center", width="60")

        tree.heading("#0", text="", anchor="w")
        tree.heading("Actuador", text="Actuador")
        tree.heading("Valor", text="Valor")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")

        boton_actualizar = Button(self.frame2, text="Actualizar", command= actualizar_registros)
        boton_actualizar.grid(row=0, column=2, padx=5, sticky="e")

        resultado_led, error = self.controlador.mostrar_registros_led()

        for registro in resultado_led:
            tree.insert("", "end", values=("ledroberto", registro[0], registro[1], registro[2]))



    def iniciar(self):
        self.miVentana.mainloop()

vista = Vista()
vista.iniciar()
