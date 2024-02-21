from tkinter import Tk, Frame, Button, Label, StringVar

miVentana = Tk()
miVentana.title("Roberto Carlos")
miVentana.resizable(0,0)
miVentana.geometry("300x150")

frame1 = Frame(miVentana)
frame1.pack(fill='both', expand=True)

lbl_titulo = Label(frame1, text="..:: Control de led::..")
lbl_titulo.grid(row=0, column=1, padx=5, pady=5)

btn_ON = Button(frame1, width=10, text="Encender")
btn_ON.config(fg="blue")
btn_ON.grid(row=1, column=0, sticky="w", padx=5, pady=5)

btn_OFF = Button(frame1, width=10, text="Apagar")
btn_OFF.config(fg="red")
btn_OFF.grid(row=1, column=2, padx=5, pady=5)

lbl_estado = Label(frame1)
lbl_estado.config(fg="red", font=("Courier New", 14, "bold"))
lbl_estado.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

lbl_barraEstado = Label(frame1)
lbl_barraEstado.config(fg="red", font=(8))
lbl_barraEstado.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

miVentana.mainloop()
