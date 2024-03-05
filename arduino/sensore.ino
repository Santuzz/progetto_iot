
//TODO: controllare se funziona 
const int baudRate = 9600; // Adjust baud rate if needed
const byte START_BYTE = 0xFF;
const byte END_BYTE = 0xFE;

unsigned long lastMillis = 0;  // Millisecond counter for timing
byte dataByte;                 // Variable to store the data byte

void setup() {
  Serial.begin(baudRate);
}

void loop() {
  if (millis() - lastMillis >= 1000) { // Check for 1 second interval
    lastMillis = millis();

    if (Serial.available() >= 3) { // Check if at least 3 bytes are available
      if (Serial.read() == START_BYTE) { // Read and check the first byte
        dataByte = Serial.read();        // Read the data byte
        if (Serial.read() == END_BYTE) {  // Read and check the end byte
          // Process the dataByte here (e.g., print it)
          Serial.print("Received data: ");
          Serial.println(dataByte);
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
}

