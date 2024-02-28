from tkinter import Tk, Frame, Label, StringVar, Listbox, Scrollbar
from tkinter import ttk  # Importa ttk para utilizar el Notebook
import threading
import tkinter
from .controlador import Controlador

miVentana = Tk()
miVentana.title("Félix Alexis Sánchez López")
miVentana.resizable(0,0)
miVentana.geometry("320x230")

# Cargar el icono desde un archivo PNG
try:
    icono = tkinter.PhotoImage(file="ejercicio4/imagenes/icon-32.png")
    miVentana.iconphoto(True, icono)
except tkinter.TclError as e:
    print("No se pudo cargar el icono:", e)    

estadoTemp = StringVar()
estadoLumin = StringVar()

def finalizar():
    controlador.finalizar()

def leerSensores():
    controlador.leerSensores()

# Crear los widgets
notebook = ttk.Notebook(miVentana)
notebook.pack(fill='both', expand=True)

frame1 = Frame(notebook)
frame2 = Frame(notebook)
frame3 = Frame(notebook)

notebook.add(frame3, text='Registros')
notebook.add(frame1, text='Temperatura')  # Agrega una pestaña para la temperatura
notebook.add(frame2, text='Luminosidad')  # Agrega una pestaña para la luminosidad

# Widgets para la pestaña de Temperatura
Label(frame1, text="Temperatura").grid(row=0, column=0, padx=10, pady=5, sticky="we")
Label(frame1, textvariable=estadoTemp, width=6, borderwidth=2, relief="groove",
        fg="green", font=("Courier New", 15, "bold")).grid(row=1,
        column=0, padx=10, pady=5, sticky="wesn")

scroll_temp = Scrollbar(frame1, orient="vertical")
lstbox_temp = Listbox(frame1, height=5, yscrollcommand=scroll_temp.set)

scroll_temp.grid(row=2, column=1, sticky='ns')
lstbox_temp.grid(row=2, column=0, padx=5, pady=5, sticky="wesn")
scroll_temp.configure(command=lstbox_temp.yview)

# Widgets para la pestaña de Luminosidad
Label(frame2, text="Luminosidad").grid(row=0, column=0, padx=10, pady=5, sticky="we")
Label(frame2, textvariable=estadoLumin, width=6, borderwidth=2, relief="groove",
        fg="red", font=("Courier New", 15, "bold")).grid(row=1,
        column=0, padx=10, pady=5, sticky="wesn")

scroll_lumin = Scrollbar(frame2, orient="vertical")
lstbox_lumin = Listbox(frame2, height=5, yscrollcommand=scroll_lumin.set)

scroll_lumin.grid(row=2, column=1, sticky='ns')
lstbox_lumin.grid(row=2, column=0, padx=5, pady=5, sticky="wesn")
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
