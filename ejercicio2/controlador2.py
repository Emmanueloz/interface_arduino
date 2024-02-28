import serial, time

arduino = serial.Serial('COM2',9600, timeout=1)
time.sleep(2)
print(arduino)
arduino.write("4:0".encode())
time.sleep(0.1)
datos = arduino.readline().decode('utf-8')
print(datos)
if datos:
    print("Datos recibidos...")
    estados = eval(datos)
    if estados[0] == 0:
        estadoLed1.set("Led 1 Apagado")
    if estados[0] == 1:
        estadoLed1.set("Led 1 Encendido")
        led1.set(1)
    if estados[1] == 0:
        estadoLed2.set("Led 2 Apagado")
    if estados[1] == 1:
        estadoLed2.set("Led 2 Encendido")
        led3.set(1)
    if estados[2] == 0:
        estadoLed3.set("Led 3 Apagado")
    if estados[2] == 1:
        estadoLed3.set("Led 3 Encendido")
        led3.set(1)
else:
    print("No se recibieron datos...")
    barraEstado.set("ERROR alconectar con arduino")



def encenderLed(nLed):
    arduino.write(f"{str(nLed)}:1".encode())
    time.sleep(0.1)
    valor = int(arduino.readline().decode("utf-8"))
    print(valor)
    return valor

def apagarLed(nLed):
    arduino.write(f"{str(nLed)}:0".encode())
    time.sleep(0.1)
    valor = int(arduino.readline().decode("utf-8"))
    print(valor)
    return valor