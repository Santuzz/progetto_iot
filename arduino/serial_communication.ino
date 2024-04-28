const int redPin = 2;    // Connect the red LED to pin 2
const int yellowPin = 3; // Connect the yellow LED to pin 3
const int greenPin = 4;  // Connect the green LED to pin 4

unsigned long previousMillis = 0;
long intervalRed = 5000;    // Time for red (5 seconds)
long intervalGreen = 5000;  // Time for green (5 seconds)
const long intervalYellow = 1000; // Time for yellow (1 second)

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
    // Check if 1 second has elapsed since the last iteration
    if (millis() - lastMillis >= 1000) {
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
    }

    // Traffic light management based on the current state
    unsigned long currentMillis = millis();
    switch (currentState) {
        case 0: // Red
            digitalWrite(redPin, HIGH);
            digitalWrite(yellowPin, LOW);
            digitalWrite(greenPin, LOW);
            
            if (currentMillis - previousMillis >= intervalRed) {
                previousMillis = currentMillis;
                currentState = 2; // Move to yellow
            }
            break;

        case 1: // Green
            digitalWrite(redPin, LOW);
            digitalWrite(yellowPin, LOW);
            digitalWrite(greenPin, HIGH);

            if (currentMillis - previousMillis >= intervalGreen) {
                previousMillis = currentMillis;
                currentState = 0; // Move to red
            }
            break;

        case 2: // Yellow
            digitalWrite(redPin, LOW);
            digitalWrite(yellowPin, HIGH);
            digitalWrite(greenPin, LOW);

            if (currentMillis - previousMillis >= intervalYellow) {
                previousMillis = currentMillis;
                currentState = 1; // Move to green
            }
            break;
    }
}

void processPlusTime() {
    // Process the additional time received from serial
    // Update the green interval time based on the value of plus_time
    if (plus_time > 0) {
        intervalGreen += plus_time * 1000; // Convert seconds to milliseconds and add to green interval
    } else if (plus_time < 0) {
        intervalGreen -= (-plus_time) * 1000; // Convert seconds to milliseconds and subtract from green interval
        // Ensure that the green interval is not less than 1000 milliseconds (1 second)
        if (intervalGreen < 1000) {
            intervalGreen = 1000;
        }
    }
}