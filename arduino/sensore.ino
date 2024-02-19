
unsigned long timestamp;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  timestamp = millis();
  
}

void loop() {
  int dato1;
  //int dato2;
  if (millis() - timestamp > 1000){
    dato1 = analogRead(0);
    //dato2 = analogRead(1);
    // pacchetto dati
    // FF  2  dato1 dato2 FE
    Serial.write(0xFF);
    Serial.write(1);
    
    Serial.write(map(dato1,0,1023,0,253));
    //Serial.write(map(dato2,0,1023,0,253));

    Serial.write(0xFE);
    
    timestamp = millis();
  }
  
}
