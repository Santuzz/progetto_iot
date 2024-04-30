const int road_a_redPin = 2;    // Connect the red LED to pin 2
const int road_a_yellowPin = 3; // Connect the yellow LED to pin 3
const int road_a_greenPin = 4;  // Connect the green LED to pin 4

const int road_b_redPin = 5;    // Connect the red LED to pin 2
const int road_b_yellowPin = 6; // Connect the yellow LED to pin 3
const int road_b_greenPin = 7;  // Connect the green LED to pin 4

unsigned long previousMillis = 0;
long intervalRed = 5000;    // Time for red (5 seconds)
long intervalGreen = 5000;  // Time for green (5 seconds)
const long intervalYellow = 1000; // Time for yellow (1 second)

long road_intervalRed = 0;
long road_intervalGreen = 0;

int currentState = 0;

const int baudRate = 9600; // Adjust baud rate if needed
const byte START_BYTE = 0xFF;
const byte END_BYTE = 0xFE;

unsigned long lastMillis = 0;  // Millisecond counter for timing
long plus_time = 0;           // Variable to store the time to be added to green interval

void setup() {
    pinMode(road_a_redPin, OUTPUT);
    pinMode(road_a_yellowPin, OUTPUT);
    pinMode(road_a_greenPin, OUTPUT);
    pinMode(road_b_redPin, OUTPUT);
    pinMode(road_b_yellowPin, OUTPUT);
    pinMode(road_b_greenPin, OUTPUT);

    Serial.begin(baudRate);
}

void loop() {
    road_intervalRed = 0;
    road_intervalGreen = 0;

    // Check if 1 second has elapsed since the last iteration
    /*if (millis() - lastMillis >= 1000) {
        lastMillis = millis();

        // Check if there are data available on the serial port
        if (Serial.available() >= 3) {
            if (Serial.read() == START_BYTE) { // Read and check the first byte
                plus_time = Serial.parseInt(); // Read the additional time from serial
                if (Serial.read() == END_BYTE) { // Read and check the end byte
                    // Process the additional time
                    processPlusTime();
                } else {
                    // Handle case where end byte is missing
                    Serial.println("Error: Missing end byte");
                }
            } else {
                // Handle case where start byte is missing
                Serial.println("Error: Missing start byte");
                // Clear the serial buffer to prevent overflow
                Serial.read(10); // Read and discard up to 10 bytes
            }
        }
    }*/

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

void processPlusTime() {
    // Process the additional time received from serial
    // Update the green interval time based on the value of plus_time
    if (plus_time > 0) {
        // The red interval for road_a and the green interval for road_b is the same
        // The green interval for road_a and the red interval for road_b is the same
        road_intervalRed = intervalRed - ((plus_time * 1000)/2);
        road_intervalGreen = intervalGreen + (plus_time * 1000); // Convert seconds to milliseconds and add to green interval
        
        // Ensure that the red interval is not less than 3000 milliseconds (3 second)
        if (road_intervalRed < 3000) {
           road_intervalRed = 3000;
        }
    } else if (plus_time < 0) {
        road_intervalGreen = intervalGreen - ((-plus_time) * 1000); // Convert seconds to milliseconds and subtract from green interval
        road_intervalRed = intervalRed + (((-plus_time) * 1000)/2);
        
        // Ensure that the green interval is not less than 3000 milliseconds (3 second)
        if (road_intervalGreen < 3000) {
            road_intervalGreen = 3000;
        }
    } else {
        road_intervalGreen = intervalGreen;
        road_intervalRed = intervalRed;
    }
}