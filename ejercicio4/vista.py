from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
from ejercicio4 import controlador

class Vista:
    def __init__(self):
        self.miVentana = Tk()
        self.miVentana.title("Aplicaciones de Iot")
        self.miVentana.resizable(0,0)
        self.miVentana.geometry("320x230")

        self.frame1 = Frame(self.miVentana)
        self.frame1.pack(fill='both', expand=True)

        Label(self.frame1, text="..:: Temperatura y Luminosidad ::..").grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="we")

        Label(self.frame1, text="Temperatura").grid(row=1, column=0, padx=10, pady=5, sticky="we")
        Label(self.frame1, text="Luminosidad").grid(row=1, column=2, padx=10, pady=5, sticky="we")

        self.estadoTemp = StringVar()
        self.estadoLumin = StringVar()

        Label(self.frame1, textvariable=self.estadoTemp, width=6, borderwidth=2, relief="groove", fg="green", bg="black", font=("Courier New", 15, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="wesn")
        Label(self.frame1, textvariable=self.estadoLumin, width=6, borderwidth=2, relief="groove", fg="red", bg="black", font=("Courier New", 15, "bold")).grid(row=2, column=2, padx=5, pady=5, sticky="wesn")
        
        scroll_temp = Scrollbar(self.frame1, orient="vertical")
        self.lstbox_temp = Listbox(self.frame1, height=5, yscrollcommand=scroll_temp.set)

        scroll_temp.grid(row=3, column=1, sticky='ns')
        self.lstbox_temp.grid(row=3, column=0, padx=5, pady=5, sticky="wesn")
        scroll_temp.configure(command=self.lstbox_temp.yview)

        scroll_lumin = Scrollbar(self.frame1, orient="vertical")
        self.lstbox_lumin = Listbox(self.frame1, height=5, yscrollcommand=scroll_lumin.set)

        scroll_lumin.grid(row=3, column=3, sticky='ns')
        self.lstbox_lumin.grid(row=3, column=2, padx=5, pady=5, sticky="wesn")
        scroll_lumin.configure(command=self.lstbox_lumin.yview)

    def iniciar(self):
        self.miVentana.mainloop()

# Ejemplo de uso
vista = Vista()
vista.iniciar()
