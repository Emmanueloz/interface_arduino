from tkinter import Tk, Frame, Button, Label, Entry, StringVar, IntVar, Scale, messagebox
import serial
import time

miVentana = Tk()
miVentana.title("Gustavo Alexander Medina Cifuentes")
miVentana.resizable(0, 0)
miVentana.geometry("290x290")

estadoServo1 = StringVar()
estadoServo2 = StringVar()
barraEstado = StringVar()
servo1 = StringVar()
servo2 = IntVar()

def control_servo1():
    if servo1.get() != "":
        if servo1.get().isdigit():
            grados = int(servo1.get())
            if 0 <= grados <= 180:
                arduino.write(f"1:{grados}".encode('ascii'))
                time.sleep(0.1)
                estadoS1 = arduino.readline().decode('utf-8')
                estadoServo1.set(estadoS1.strip())
            else:
                messagebox.showwarning("CUIDADO", "El valor debe estar entre 0 y 180")
        else:
            messagebox.showerror("ERROR", "Solo valores numéricos")
    else:
        messagebox.showerror("ERROR", "Introduce un valor en la caja")

def control_servo2():
    arduino.write(f"2:{servo2.get()}".encode('ascii'))
    time.sleep(0.1)
    estadoS2 = arduino.readline().decode('utf-8')
    estadoServo2.set(estadoS2.strip())

frame1 = Frame(miVentana)
frame1.pack(fill='both', expand=True)

Label(frame1, text="..:: control de 2 Servomotores ::..").grid(row=0, column=0, columnspan=3, padx=5, sticky="we")

Label(frame1, text="Servo 1").grid(row=1, column=0, padx=10, pady=5, sticky="we")
Label(frame1, text="Servo 2").grid(row=1, column=1, padx=5, pady=5, sticky="we")

Label(frame1, textvariable=estadoServo1, width=6, borderwidth=2, relief="groove", fg="green", bg="black",
      font=("Courier New", 15, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="wesn")

Label(frame1, textvariable=estadoServo2, width=6, borderwidth=2, relief="groove", fg="green", bg="black",
      font=("Courier New", 15, "bold")).grid(row=2, column=1, padx=5, pady=5, sticky="wesn")

Entry(frame1, textvariable=servo1, width=6, justify="center").grid(row=3, column=0, padx=10, pady=5, sticky="wesn")

Scale(frame1, variable=servo2, from_=0, to=180, orient="vertical", tickinterval=30, length=200).grid(row=1, column=2,
                                                                                                   rowspan=4, padx=5,
                                                                                                   pady=5)

Button(frame1, width=8, text="Enviar", command=control_servo1).grid(row=4, column=0, sticky="w", padx=10, pady=5)

Button(frame1, width=8, text="Enviar", command=control_servo2).grid(row=4, column=1, sticky="e", padx=5, pady=5)

Label(frame1, textvariable=barraEstado, width=20, bd=2, fg="red").grid(row=5, column=0, columnspan=3, padx=5, pady=10,
                                                                        sticky="we")

arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)
print(arduino)
arduino.write("3:0".encode())
time.sleep(0.1)
datos = arduino.readline().decode('utf-8')
print(datos)
if datos:
    print("Datos recibidos...")
    estados = eval(datos)
    estadoServo1.set(str(estados[0]))
    estadoServo2.set(estados[1])
    servo2.set(estados[1])
else:
    print("No se recibieron datos...")
    barraEstado.set("ERROR al conectar con Arduino")

miVentana.mainloop()
