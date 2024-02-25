from tkinter import Tk, Frame, Label, StringVar, IntVar
from tkinter import Listbox, Scrollbar
import serial, time, threading

miVentana = Tk()
miVentana.title("Aplicaciones Iot")
miVentana.resizable(0,0)
miVentana.geometry("320x230")

estadoTemp = StringVar()
estadoLumin = StringVar()
barraEstado = StringVar()
estaCorriendo = True

def finalizar():
    estaCorriendo = False
    hiloSensores.join(0.1)
    miVentana.quit()
    miVentana.destroy()
    arduino.close()
    
def leerSensores():
    while estaCorriendo:
        datos = arduino.readline().decode('utf-8').strip()
        if datos:
            posicion = datos.index(":")
            sensor = datos[:posicion]
            valor = datos[posicion+1:]
            if sensor == '3':
                estadoTemp.set(valor)
                lstbox_temp.insert("end", valor)
                lstbox_temp.see("end")
            elif sensor == '2':
                estadoLumin.set(valor)
                lstbox_lumin.insert("end", valor)
                lstbox_lumin.see("end")
                
#crear los widgets
frame1 = Frame(miVentana)
frame1.pack(fill='both', expand=True)

Label(frame1, text="..:: Temperatura y Luminosidad ::.." ).grid(row=0,
        column=0,  columnspan=4, padx=10, pady=5, sticky="we")

Label(frame1, text="Temperatura").grid(row=1, column=0, padx=10, pady=5, sticky="we")
Label(frame1, text="Luminosidad").grid(row=1, column=2, padx=10, pady=5, sticky="we")

Label(frame1, textvariable=estadoTemp, width=6, borderwidth=2, relief="groove",
        fg="green", bg="black", font=("Courier New", 15, "bold")).grid(row=2,
        column=0, padx=10, pady=5, sticky="wesn")

Label(frame1, textvariable=estadoLumin, width=6, borderwidth=2, relief="groove",
        fg="red", bg="black", font=("Courier New", 15, "bold")).grid(row=2,
        column=2, padx=5, pady=5, sticky="wesn")
        
scroll_temp = Scrollbar(frame1, orient="vertical")
lstbox_temp = Listbox(frame1, height=5, yscrollcommand=scroll_temp.set)

scroll_temp.grid(row=3, column=1, sticky='ns')
lstbox_temp.grid(row=3, column=0, padx=5, pady=5, sticky="wesn")
scroll_temp.configure(command=lstbox_temp.yview)

scroll_lumin = Scrollbar(frame1, orient="vertical")
lstbox_lumin= Listbox(frame1, height=5, yscrollcommand=scroll_lumin.set)

scroll_lumin.grid(row=3, column=3, sticky='ns')
lstbox_lumin.grid(row=3, column=2, padx=5, pady=5, sticky="wesn")
scroll_lumin.configure(command=lstbox_lumin.yview)

#se crea un hilo y se conecta con Arduino.
miVentana.protocol('WM_DELETE_WINDOW', finalizar)
hiloSensores = threading.Thread(target=leerSensores, daemon=True)
arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)
print(arduino)

arduino.write("1:0".encode())
time.sleep(0.1)
datos = arduino.readline().decode('utf-8')
print(datos)
if datos:
    print("datos recibidos..")
    estados = eval(datos) #convertir un String en una Tupla   
    estadoTemp.set(estados[0])
    estadoLumin.set(estados[1])
else:
    print("No se recibieron datos..")
    barraEstado.set("Error al conectar con Arduino")
    
try:
    hiloSensores.start()
except Exception:
    print("No se pudo lanzar el hilo..")
    
miVentana.mainloop() 
 
        