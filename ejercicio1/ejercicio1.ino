#define LED 13
int valor = 0;
bool estado = 0;
void setup()
{
    //
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    //
        if(Serial.available()>0){
        valor = Serial.read();
        
        if(valor == 'e' && estado == 0){
            digitalWrite(LED, HIGH);
            estado = 1;
            Serial.println(estado);
        }
        else if(valor == 'a' && estado == 1){
            digitalWrite(LED, LOW);
            estado = 0;
            Serial.println(estado);
        }
        else if(valor == 'E'){
            Serial.println(estado);
        }
        else{
            Serial.println(3);
        }
    }
}
