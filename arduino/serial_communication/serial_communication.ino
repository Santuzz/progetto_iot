//#define SEND_INTERVAL 5000 // every 5 seconds
unsigned long send_interval = 0;

const int road_a_redPin = 2;    // Connect the red LED to pin 2
const int road_a_yellowPin = 3; // Connect the yellow LED to pin 3
const int road_a_greenPin = 4;  // Connect the green LED to pin 4

const int road_b_redPin = 5;    // Connect the red LED to pin 2
const int road_b_yellowPin = 6; // Connect the yellow LED to pin 3
const int road_b_greenPin = 7;  // Connect the green LED to pin 4

unsigned long previousMillis = 0;
long intervalRed = 1000;    // Time for red (5 seconds)
long intervalGreen = 1000;  // Time for green (5 seconds)
const long intervalYellow = 500; // Time for yellow (1 second)

long road_intervalRed = 1000;
long road_intervalGreen = 1000;

int currentState = 0;

/* Serial Send variables */
unsigned long timestamp;

/* Serial Receive variables */
#define BUFFDIM 3 // header, plus_time, footer
long plus_time = 0;

unsigned char ucInBuffer[BUFFDIM];  // Buffer to memorize packet bytes 
size_t stBufferIndex;     // Index of the buffer

void setup()
{
  /* Serial Send setup */
  Serial.begin(9600);
  pinMode(road_a_redPin, OUTPUT);
  pinMode(road_a_yellowPin, OUTPUT);
  pinMode(road_a_greenPin, OUTPUT);
  pinMode(road_b_redPin, OUTPUT);
  pinMode(road_b_yellowPin, OUTPUT);
  pinMode(road_b_greenPin, OUTPUT);

  timestamp = 0;

  /* Serial Receive setup */
  for (stBufferIndex = 0; stBufferIndex < BUFFDIM; stBufferIndex++)
    ucInBuffer[stBufferIndex] = 0;

  stBufferIndex = 0;
}

void loop()
{
  
  // Aggiorno plus_time con il valore ricevuto sulla seriale
  int r = serialReceive(&plus_time);

  // if we recived a packet do something (turn on led for example)
  if (r == 1)
  {
    //Serial.write(plus_time);
    processPlusTime(plus_time, &road_intervalRed, &road_intervalGreen);
    //Serial.write("ok");
    Serial.write(plus_time);

  } 

  // Traffic light management based on the current state
    unsigned long currentMillis = millis();
    switch (currentState) {
        case 0: // Red road_a, Green road_b
            digitalWrite(road_a_redPin, HIGH);
            digitalWrite(road_a_yellowPin, LOW);
            digitalWrite(road_a_greenPin, LOW);

            digitalWrite(road_b_redPin, LOW);
            digitalWrite(road_b_yellowPin, LOW);
            digitalWrite(road_b_greenPin, HIGH);
            
            if (currentMillis - previousMillis >= road_intervalRed) {
                previousMillis = currentMillis;
                currentState = 1; // Move to red road_a, yellow road_b
            }
            break;

        case 1: // Red road_a, Yellow road_b
            digitalWrite(road_a_redPin, HIGH);
            digitalWrite(road_a_yellowPin, LOW);
            digitalWrite(road_a_greenPin, LOW);

            digitalWrite(road_b_redPin, LOW);
            digitalWrite(road_b_yellowPin, HIGH);
            digitalWrite(road_b_greenPin, LOW);

            if (currentMillis - previousMillis >= intervalYellow) {
                previousMillis = currentMillis;
                currentState = 2; // Move to green road_a, red road_b
            }
            break;

        case 2: // Green road_a, Red road_b
            digitalWrite(road_a_redPin, LOW);
            digitalWrite(road_a_yellowPin, LOW);
            digitalWrite(road_a_greenPin, HIGH);

            digitalWrite(road_b_redPin, HIGH);
            digitalWrite(road_b_yellowPin, LOW);
            digitalWrite(road_b_greenPin, LOW);

            if (currentMillis - previousMillis >= road_intervalGreen) {
                previousMillis = currentMillis;
                currentState = 3; // Move to yellow road_a, red road_b
            }
            break;
        
        case 3: // Yellow road_a, Red road_b
            digitalWrite(road_a_redPin, LOW);
            digitalWrite(road_a_yellowPin, HIGH);
            digitalWrite(road_a_greenPin, LOW);

            digitalWrite(road_b_redPin, HIGH);
            digitalWrite(road_b_yellowPin, LOW);
            digitalWrite(road_b_greenPin, LOW);

            if (currentMillis - previousMillis >= intervalYellow) {
                previousMillis = currentMillis;
                currentState = 0; // Move to red road_a, greed road_b
            }
            break;
    }
}

int serialReceive(long *plus_time)
{
  
  // If there are some data from the serial
  if (Serial.available() > 0)
  {
    unsigned char ucData;
    ucData = Serial.read(); // read a byte
    if (ucData == 0xFE) // EOF
    {
      // Append last byte
      ucInBuffer[stBufferIndex] = ucData;
      stBufferIndex++;
      //int r = useData(&plus_time);
      if(ucInBuffer[1] > 128){
        *plus_time= (256-ucInBuffer[1])*-1;
      }
      else
        *plus_time=ucInBuffer[1];

      // Clear buffer
      for (stBufferIndex = 0; stBufferIndex < BUFFDIM; stBufferIndex++)
        ucInBuffer[stBufferIndex] = 0;

      stBufferIndex = 0;
      //if (r == 1)
        return 1;
    }
    else
    {
      // Append
      ucInBuffer[stBufferIndex] = ucData;
      stBufferIndex++;
    }
  }
  return 0; 
}

int useData(long **plus_time)
{
  if (stBufferIndex < BUFFDIM)  // at least header, plus_time, footer
    return 0;

  if (ucInBuffer[0] != 0xFF)
    return 0;

  // getting value
  long ucVal = ucInBuffer[1];
   
  // use of value
  *(*plus_time) = ucVal;
  /*
    A cosa serve send_interval?
  */
  if (ucVal < 0){
    ucVal *= -1;
  }
  send_interval = ucVal;
  return 1;
}

void processPlusTime(int plus_time, long *road_intervalRed, long *road_intervalGreen) {
    /*
    if (plus_time > 0) {
        // The red interval for road_a and the green interval for road_b is the same
        // The green interval for road_a and the red interval for road_b is the same
        *road_intervalRed = intervalRed - ((plus_time * 1000)/2);
        *road_intervalGreen = intervalGreen + (plus_time * 1000); // Convert seconds to milliseconds and add to green interval
        
        // Ensure that the red interval is not less than 3000 milliseconds (3 second)
        if (*road_intervalRed < 3000) {
           *road_intervalRed = 3000;
        }
    } else if (plus_time < 0) {
        *road_intervalGreen = intervalGreen - ((-plus_time) * 1000); // Convert seconds to milliseconds and subtract from green interval
        *road_intervalRed = intervalRed + (((-plus_time) * 1000)/2);
        
        //Ensure that the green interval is not less than 3000 milliseconds (3 second)
        if (*road_intervalGreen < 3000) {
            *road_intervalGreen = 3000;
        }
    } else {
        *road_intervalGreen = intervalGreen;
        *road_intervalRed = intervalRed;
    }
    */
    if (plus_time == 0) {
        *road_intervalRed = intervalRed;
        *road_intervalGreen = intervalGreen; 
        
    } else if (plus_time > 0) {

      *road_intervalGreen = intervalGreen*(plus_time+1);
      *road_intervalRed = intervalRed;
      

    }else if (plus_time < 0) {
      *road_intervalRed = intervalRed*(-plus_time+1);
      *road_intervalGreen = intervalGreen;
    }
}