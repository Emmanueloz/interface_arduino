from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
import threading
from .controlador import Controlador

miVentana = Tk()
miVentana.title("Aplicaciones Iot")
miVentana.resizable(0,0)
miVentana.geometry("320x230")

estadoTemp = StringVar()
estadoLumin = StringVar()

def finalizar():
    controlador.finalizar()

def leerSensores():
    controlador.leerSensores()

# Crear los widgets
frame1 = Frame(miVentana)
frame1.pack(fill='both', expand=True)

Label(frame1, text="..:: Temperatura y Luminosidad ::.." ).grid(row=0,
        column=0,  columnspan=4, padx=10, pady=5, sticky="we")

Label(frame1, text="Temperatura").grid(row=1, column=0, padx=10, pady=5, sticky="we")
Label(frame1, text="Luminosidad").grid(row=1, column=2, padx=10, pady=5, sticky="we")

Label(frame1, textvariable=estadoTemp, width=6, borderwidth=2, relief="groove",
        fg="green", font=("Courier New", 15, "bold")).grid(row=2,
        column=0, padx=10, pady=5, sticky="wesn")

Label(frame1, textvariable=estadoLumin, width=6, borderwidth=2, relief="groove",
        fg="red", font=("Courier New", 15, "bold")).grid(row=2,
        column=2, padx=5, pady=5, sticky="wesn")

scroll_temp = Scrollbar(frame1, orient="vertical")
lstbox_temp = Listbox(frame1, height=5, yscrollcommand=scroll_temp.set)

scroll_temp.grid(row=3, column=1, sticky='ns')
lstbox_temp.grid(row=3, column=0, padx=5, pady=5, sticky="wesn")
scroll_temp.configure(command=lstbox_temp.yview)

scroll_lumin = Scrollbar(frame1, orient="vertical")
lstbox_lumin = Listbox(frame1, height=5, yscrollcommand=scroll_lumin.set)

scroll_lumin.grid(row=3, column=3, sticky='ns')
lstbox_lumin.grid(row=3, column=2, padx=5, pady=5, sticky="wesn")
scroll_lumin.configure(command=lstbox_lumin.yview)

# Se crea un hilo y se conecta con Arduino.
miVentana.protocol('WM_DELETE_WINDOW', finalizar)
controlador = Controlador(estadoTemp, estadoLumin, lstbox_temp, lstbox_lumin)
hiloSensores = threading.Thread(target=leerSensores, daemon=True)

try:
    hiloSensores.start()
    miVentana.mainloop()
except Exception:
    print("No se pudo lanzar el hilo..")
