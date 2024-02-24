const int pinLed1 = 11;
const int pinLed2 = 12;
const int pinLed3 = 13;
int estadoLed1 = 0;
int estadoLed2 = 0;
int estadoLed3 = 0;
int separador, option, valorNum;
String op, cadena, valor;
void setup()
{
    Serial.begin(9600);
    pinMode(pinLed2, OUTPUT);
    pinMode(pinLed1, OUTPUT);
    pinMode(pinLed3, OUTPUT);
}

void loop()
{
    if (Serial.available() > 0)
    {
        cadena = Serial.readString();
        separador = cadena.indexOf(':');
        op = cadena.substring(0, separador);
        option = op.toInt();
        valor = cadena.substring(separador + 1);
        valorNum = valor.toInt();

        switch (option)
        {
        case 1:
            estadoLed1 = control_led(pinLed1, valorNum);
            Serial.println(estadoLed1);
            break;
        case 2:
            estadoLed2 = control_led(pinLed2, valorNum);
            Serial.println(estadoLed2);
            break;
        case 3:
            estadoLed3 = control_led(pinLed3, valorNum);
            Serial.println(estadoLed3);
            break;
        case 4:
            Serial.println(String(estadoLed1) + "," + String(estadoLed2) + "," + String(estadoLed3));
            break;
        }
    }
}

int control_led(int pinLed, int estado)
{
    int estadoLed = -1;
    if (estado == 0)
    {
        digitalWrite(pinLed, LOW);
        estadoLed = 0;
    }
    else if (estado == 1)
    {
        digitalWrite(pinLed, HIGH);
        estadoLed = 1;
    }
    return estadoLed;
}