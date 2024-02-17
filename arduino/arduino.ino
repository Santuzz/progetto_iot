//traffic light base

const int redPin = 2;    // Collega il LED rosso al pin 2
const int yellowPin = 3; // Collega il LED giallo al pin 3
const int greenPin = 4;  // Collega il LED verde al pin 4

unsigned long previousMillis = 0;
const long intervalRed = 5000;   // Tempo per il rosso (5 secondi)
const long intervalGreen = 5000; // Tempo per il verde (5 secondi)
const long intervalYellow = 1000; // Tempo per il giallo (1 secondo)

int currentState = 0; // 0 = rosso, 1 = verde, 2 = giallo

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();

  switch (currentState) {
    case 0: // Verde
      digitalWrite(redPin, LOW);
      digitalWrite(yellowPin, LOW);
      digitalWrite(greenPin, HIGH);

      if (currentMillis - previousMillis >= intervalRed) {
        previousMillis = currentMillis;
        currentState = 2; // Passa al giallo
      }
      break;

    case 1: // rosso
      digitalWrite(redPin, HIGH);
      digitalWrite(yellowPin, LOW);
      digitalWrite(greenPin, LOW);

      if (currentMillis - previousMillis >= intervalGreen) {
        previousMillis = currentMillis;
        currentState = 0; // Passa al verde
      }
      break;

    case 2: // Giallo
      digitalWrite(redPin, LOW);
      digitalWrite(yellowPin, HIGH);
      digitalWrite(greenPin, LOW);

      if (currentMillis - previousMillis >= intervalYellow) {
        previousMillis = currentMillis;
        currentState = 1; // Passa al rosso
      }
      break;
  }
}
