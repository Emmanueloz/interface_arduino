#include <Ticker.h>
const long A = 1000;  // Resistencia en oscuridad de K
const int B = 15;       // Resistencia ala luz (10 Lux) en K
const long Rc = 10;     // Resistencia calibración en K
const int pinLDR = A1;  // Pin del LDR 
const int pinLM35 = A0; // Pin de LM35 temp 
int Volt, lumAct = 0,lumNuevo;
float tempAct = 0.0, tempNuevo;
int separador, posNueva, option;
String op, cadena, grados;

void leerTemp();
void leerLumin();

Ticker tareaTemp(leerTemp,1000);
Ticker tareaLumin(leerLumin,1500);

void setup (){
    Serial.begin(9600);
    tareaTemp.start();
    tareaLumin.start();
}

void loop(){
  tareaTemp.update();
  tareaLumin.update();

  if(Serial.available()){
      controlPeticiones(Serial.readString());
  }
}

void controlPeticiones(String cadena){
    separador= cadena.indexOf(':');//posicion de ':'
    op = cadena.substring(0,separador);//extrae de 0 hasta :
    option = op.toInt();
    grados = cadena.substring(separador+1);//extrae el resto  de la cadena
    posNueva = grados.toInt();//grados a entero

    switch (option){
      case 1:
          Serial.println(String(lumAct)+","+String(tempAct));
          break;
        //agregar aqui otras opciones para control de actuadores..         
    }
    cadena = ""; // Se corrigió para borrar el contenido de la cadena
}

void leerTemp(){
    tempNuevo = analogRead(pinLM35);
    tempNuevo = (tempNuevo * 500.0)/1024.0;
    if(tempNuevo != tempAct){
      tempAct = tempNuevo;
      Serial.println("3:"+ String(tempAct));
    }
}

void leerLumin(){
    Volt = analogRead(pinLDR);//nivel de voltaje leido
    lumNuevo = ((long)(1024-Volt) *A*10)/((long)B*Rc*Volt); //usar si LDR entre GND Y A0
    //lumenes = ((long)Volt*A*10)/((long)B*Rc*(1024-Volt)); //usar si LDR entre A0 y Vcc
    if(lumNuevo != lumAct){
        lumAct = lumNuevo;
        Serial.println("2:"+ String(lumAct));
    }
}


