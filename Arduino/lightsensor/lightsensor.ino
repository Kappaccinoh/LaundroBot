// https://www.build-electronic-circuits.com/arduino-light-sensor/#:~:text=To%20connect%20a%20light%20sensor,photoresistors%2C%20photodiodes%2C%20and%20phototransistors.

void setup() {
  // Setup serial communication at baudrate 9600 for reading the light sensor
  Serial.begin(9600);
}

void loop() {
  // reads the input on analog pin A0
  int lightValue = analogRead(A0);

  // Print out the values to read in the Serial Monitor
  Serial.print("Analog reading (0-1023): ");
  Serial.print(lightValue);
  Serial.print("\n");
}