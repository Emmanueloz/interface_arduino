from tkinter import Tk, Frame, Button, Label, Entry, StringVar, IntVar, Scale, PhotoImage, messagebox, Toplevel, ttk
from .controlador import Controlador

def enviar_servo1():
    grados = servo1.get()
    estado = controlador.control_servo1(grados)
    if estado == "EL VALOR DEL SERVO DEBE ESTAR EN 0 A 180" or estado == "EL VALOR DEBE SER NUMERICO":
        messagebox.showerror("Error", estado)
    elif estado == "NO SE HA CAMBIADO LA POSICIÓN DEL SERVO":
        messagebox.showinfo("Información", estado)
    else:
        estado_servo1.set(estado)
        controlador.posicion_actual_servo1 = int(grados)

def enviar_servo2():
    grados = str(servo2.get())
    estado = controlador.control_servo2(grados)

    if estado == "NO SE HA CAMBIADO LA POSICIÓN DEL SERVO2":
        messagebox.showinfo("Información", estado)
    else:
        estado_servo2.set(estado)

def abrir_ventana_con_imagen():
    ventana_imagen = Toplevel(miVentana)
    ventana_imagen.title("Registro del servo")

    # Treeview para mostrar los registros de los servos
    tree = ttk.Treeview(ventana_imagen)
    tree["columns"] = ("Servo", "Valor", "Fecha")

    tree.column("#0", width=0, stretch="no")
    tree.column("Fecha", anchor="center", width=120)
    tree.column("Valor", anchor="center", width=80)

    tree.heading("#0", text="", anchor="w")
    tree.heading("Servo", text="Servo")
    tree.heading("Valor", text="Valor")
    tree.heading("Fecha", text="Fecha")
    


    tree.pack()
    
    
    
# Crear la ventana principal
miVentana = Tk()
miVentana.title("Gustavo Alexander Medina Cifuentes")
miVentana.resizable(0, 0)
miVentana.geometry("350x350")

# Resto del código permanece igual

controlador = Controlador()
estado_servo1 = StringVar(value=controlador.estado_servo1)
estado_servo2 = StringVar(value=controlador.estado_servo2)
barra_estado = StringVar()
servo1 = StringVar()
servo2 = IntVar()
servo2.set(int(estado_servo2.get()))

frame1 = Frame(miVentana)
frame1.pack(fill='both', expand=True)

imagen_path = 'ejercicio3/notebook.png'
imagen = PhotoImage(file=imagen_path)

imagen = imagen.subsample(15, 15)

boton_imagen = Button(frame1, image=imagen, command=abrir_ventana_con_imagen)
boton_imagen.photo = imagen
boton_imagen.grid(row=0, column=2, sticky="e",  padx=5, pady=5)


Label(frame1, text="..:: control de 2 Servomotores ::..").grid(row=0, column=0, columnspan=2, padx=5, sticky="we")

Label(frame1, text="Servo 1").grid(row=1, column=0, padx=10, pady=5, sticky="we")
Label(frame1, text="Servo 2").grid(row=1, column=1, padx=5, pady=5, sticky="we")

Label(frame1, textvariable=estado_servo1, width=6, borderwidth=2, relief="groove", fg="green", bg="black", font=("Courier New", 15, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="wesn")

Label(frame1, textvariable=estado_servo2, width=6, borderwidth=2, relief="groove", fg="red", bg="black", font=("Courier New", 15, "bold")).grid(row=2, column=1, padx=5, pady=5, sticky="wesn")

Entry(frame1, textvariable=servo1, width=6, justify="center").grid(row=3, column=0, padx=10, pady=5, sticky="wesn")

Scale(frame1, variable=servo2, from_=0, to=180, orient="vertical", tickinterval=30, length=200).grid(row=1, column=3, rowspan=4, padx=5, pady=5)

Button(frame1, width=8, text="Enviar", command=enviar_servo1).grid(row=4, column=0, sticky="w", padx=10, pady=5)
Button(frame1, width=8, text="Enviar", command=enviar_servo2).grid(row=4, column=1, sticky="e", padx=5, pady=5)

Label(frame1, textvariable=barra_estado, width=20, bd=2, fg="red").grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky="we")

miVentana.mainloop()