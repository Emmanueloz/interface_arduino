# include <Servo.h>

int pinServo1 = 5, pinServo2 = 3, posActServo1 = 0, posActServo2 = 0;
int separador, posNueva, option;
Servo servo1, servo2;
String op, cadena, grados;

void setup(){
  Serial.begin(9600);
  servo1.attach(pinServo1);
  servo1.write(0);
  servo2.attach(pinServo2);
  servo2.write(0);
  }

void loop(){
  if (Serial.available()> 0){
    cadena = Serial.readString();
    separador = cadena.indexOf(':');
    op = cadena.substring(0,separador);
    option = op.toInt();
    grados = cadena.substring(separador+1);
    posNueva = grados.toInt();

    switch (option){
      case 1:
        moverServo(1,posNueva);
        Serial.print(posActServo1);
        break;
      case 2:
        moverServo(2, posNueva);
        Serial.print(posActServo2);
        break;
      case 3:
        Serial.println(String(posActServo1)+","+String(posActServo2));
      }
      cadena = "\0";
    }
  }
void moverServo(int numServo, int posicion){
  if (numServo == 1){
    if (posicion != posActServo1){
      posActServo1 = posicion;
      servo1.write(posicion);
      }
    }
  else if (numServo == 2){
    if (posicion != posActServo2){
      posActServo2 = posicion;
      servo2.write(posicion);
      }
   } 
  }