const int analogInPin0 = 36;  // Analog input pin that the potentiometer is attached to - Sensor 1
const int analogInPin1 = 39; // Sensor 2
const int analogInPin2 = 34; // Sensor 3
const int analogInPin3 = 35; // Sensor 4
const int analogInPin4 = 32; // Sensor 5

int sensorValue0 = 0;  // Washer 1 3.4k - 4k
int sensorValue1 = 0;  // Washer 2 2.1k - 3k
int sensorValue2 = 0;  // Washer 3 1.8k - 4k
int sensorValue3 = 0;  // Washer 4 3.2k - 4k 
int sensorValue4 = 0;  // Washer 5 1.7k - 4k

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Read sensor values
  sensorValue0 = analogRead(analogInPin0);
  sensorValue1 = analogRead(analogInPin1);
  sensorValue2 = analogRead(analogInPin2);
  sensorValue3 = analogRead(analogInPin3);
  sensorValue4 = analogRead(analogInPin4);

  // Print sensor values
  Serial.print("Sensor 1 output value: ");
  Serial.println(sensorValue0);
  Serial.print("Sensor 2 output value: ");
  Serial.println(sensorValue1);
  Serial.print("Sensor 3 output value: ");
  Serial.println(sensorValue2);
  Serial.print("Sensor 4 output value: ");
  Serial.println(sensorValue3);
  Serial.print("Sensor 5 output value: ");
  Serial.println(sensorValue4);

  // Delay before reading sensors again
  delay(1000); // Adjust delay time as needed
}
