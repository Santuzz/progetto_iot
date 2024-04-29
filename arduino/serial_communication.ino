const int redPin = 2;    // Connect the red LED to pin 2
const int yellowPin = 3; // Connect the yellow LED to pin 3
const int greenPin = 4;  // Connect the green LED to pin 4

unsigned long previousMillis = 0;
long intervalRed = 8000;    // Time for red (5 seconds)
long intervalGreen = 8000;  // Time for green (5 seconds)
const long intervalYellow = 3000; // Time for yellow (1 second)

long intervalRed_new = 0;
long intervalGreen_new = 0;

int currentState = 0; // 0 = red, 1 = green, 2 = yellow

const int baudRate = 9600; // Adjust baud rate if needed
const byte START_BYTE = 0xFF;
const byte END_BYTE = 0xFE;

unsigned long lastMillis = 0;  // Millisecond counter for timing
long plus_time = 0;           // Variable to store the time to be added to green interval

void setup() {
    pinMode(redPin, OUTPUT);
    pinMode(yellowPin, OUTPUT);
    pinMode(greenPin, OUTPUT);

    Serial.begin(baudRate);
}

void loop() {
    intervalRed_new = 0;
    intervalGreen_new = 0;

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
        case 0: // Red
            digitalWrite(redPin, HIGH);
            digitalWrite(yellowPin, LOW);
            digitalWrite(greenPin, LOW);
            
            if (currentMillis - previousMillis >= intervalRed_new) {
                previousMillis = currentMillis;
                currentState = 1; // Move to green
            }
            break;

        case 1: // Green
            digitalWrite(redPin, LOW);
            digitalWrite(yellowPin, LOW);
            digitalWrite(greenPin, HIGH);

            if (currentMillis - previousMillis >= intervalGreen_new) {
                previousMillis = currentMillis;
                currentState = 2; // Move to yellow
            }
            break;

        case 2: // Yellow
            digitalWrite(redPin, LOW);
            digitalWrite(yellowPin, HIGH);
            digitalWrite(greenPin, LOW);

            if (currentMillis - previousMillis >= intervalYellow) {
                previousMillis = currentMillis;
                currentState = 0; // Move to red
            }
            break;
    }
}

void processPlusTime() {
    // Process the additional time received from serial
    // Update the green interval time based on the value of plus_time
    if (plus_time > 0) {
        intervalRed_new = intervalRed - ((plus_time * 1000)/2);
        intervalGreen_new = intervalGreen + (plus_time * 1000); // Convert seconds to milliseconds and add to green interval
        // Ensure that the red interval is not less than 3000 milliseconds (3 second)
        if (intervalRed_new < 3000) {
            intervalRed_new = 3000;
        }
    } else if (plus_time < 0) {
        intervalGreen_new = intervalGreen - ((-plus_time) * 1000); // Convert seconds to milliseconds and subtract from green interval
        intervalRed_new = intervalRed + ((plus_time * 1000)/2);
        // Ensure that the green interval is not less than 3000 milliseconds (3 second)
        if (intervalGreen_new < 3000) {
            intervalGreen_new = 3000;
        }
    } else {
        intervalGreen_new = intervalGreen;
        intervalRed_new = intervalRed;
    }
}