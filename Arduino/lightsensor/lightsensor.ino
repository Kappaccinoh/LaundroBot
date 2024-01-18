#include <WiFi.h> //Wifi library
#include <HTTPClient.h>
#include "esp_wpa2.h" //wpa2 library for connections to Enterprise networks

#define EAP_IDENTITY "" //if connecting from another corporation, use identity@organisation.domain in Eduroam 
#define EAP_USERNAME "" //oftentimes just a repeat of the identity
#define EAP_PASSWORD "" //your Eduroam password
/*
  Analog input, analog output, serial output

  Reads an analog input pin, maps the result to a range from 0 to 255 and uses
  the result to set the pulse width modulation (PWM) of an output pin.
  Also prints the results to the Serial Monitor.

  The circuit:
  - potentiometer connected to analog pin 0.
    Center pin of the potentiometer goes to the analog pin.
    side pins of the potentiometer go to +5V and ground
  - LED connected from digital pin 9 to ground through 220 ohm resistor

  created 29 Dec. 2008
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogInOutSerial
*/

// These constants won't change. They're used to give names to the pins used:
const int analogInPin = 34;  // Analog input pin that the potentiometer is attached to
const int fakeGND = 39;

//const int analogOutPin = 39;  // Analog output pin that the LED is attached to

int sensorValue = 0;  // value read from the pot
int outputValue = 0;  // value output to the PWM (analog out)

const char* ssid = "NUS_STU"; // Eduroam SSID
const char* host = "www.google.com"; //external server domain for HTTP connection after authentification
#define ENDPOINT "https://free-api-ryfe.onrender.com/seventeenWashers/update"
int counter = 0;

// NOTE: For some systems, various certification keys are required to connect to the wifi system.
//       Usually you are provided these by the IT department of your organization when certs are required
//       and you can't connect with just an identity and password.
//       Most eduroam setups we have seen do not require this level of authentication, but you should contact
//       your IT department to verify.
//       You should uncomment these and populate with the contents of the files if this is required for your scenario (See Example 2 and Example 3 below).
//const char *ca_pem = "insert your CA cert from your .pem file here";
//const char *client_cert = "insert your client cert from your .crt file here";
//const char *client_key = "insert your client key from your .key file here";

void setup() {
  pinMode(2, OUTPUT);
  
  pinMode(fakeGND, OUTPUT);
  digitalWrite(fakeGND, 0);

  Serial.begin(115200);
  delay(10);
  Serial.println();
  Serial.print("Connecting to network: ");
  Serial.println(ssid);
  WiFi.disconnect(true);  //disconnect form wifi to set new wifi connection
  WiFi.mode(WIFI_STA); //init wifi mode
  
  // Example1 (most common): a cert-file-free eduroam with PEAP (or TTLS)
  WiFi.begin(ssid, WPA2_AUTH_PEAP, EAP_IDENTITY, EAP_USERNAME, EAP_PASSWORD);

  // Example 2: a cert-file WPA2 Enterprise with PEAP
  //WiFi.begin(ssid, WPA2_AUTH_PEAP, EAP_IDENTITY, EAP_USERNAME, EAP_PASSWORD, ca_pem, client_cert, client_key);
  
  // Example 3: TLS with cert-files and no password
  //WiFi.begin(ssid, WPA2_AUTH_TLS, EAP_IDENTITY, NULL, NULL, ca_pem, client_cert, client_key);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    counter++;
    if(counter>=60){ //after 30 seconds timeout - reset board
      ESP.restart();
    }
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address set: "); 
  Serial.println(WiFi.localIP()); //print LAN IP
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) { //if we are connected to Eduroam network
    counter = 0; //reset counter
    Serial.println("Wifi is still connected with IP: "); 
    Serial.println(WiFi.localIP());   //inform user about his IP address
  } else if (WiFi.status() != WL_CONNECTED) { //if we lost connection, retry
    WiFi.begin(ssid);      
  }
  while (WiFi.status() != WL_CONNECTED) { //during lost connection, print dots
    delay(500);
    Serial.print(".");
    counter++;
    if(counter>=60){ //30 seconds timeout - reset board
    ESP.restart();
    }
  }

  Serial.print("Connecting to website: ");
  Serial.println(host);
  WiFiClient client;
  HTTPClient http;

  // syntax - client.connect(ip/URL, port)
  if (client.connect(host, 80)) {
    Serial.println("Connected");
    // read the analog in value:
    sensorValue = analogRead(analogInPin);
    // map it to the range of the analog out:
    outputValue = map(sensorValue, 0, 1023, 0, 255);
    // change the analog out value:
    //analogWrite(analogOutPin, outputValue);
    // print the results to the Serial Monitor:
    Serial.print("sensor = ");
    Serial.print(sensorValue);
    Serial.print("\t output = ");
    Serial.println(outputValue);

    bool inUse = false;

    if (sensorValue > 3500) {
      digitalWrite(2, 1);
    } else {
      inUse = true;
      digitalWrite(2, 0);
    }

    // wait 2 milliseconds before the next loop for the analog-to-digital
    // converter to settle after the last reading:
    delay(2);

    // Your Domain name with URL path or IP address with path
    http.begin(ENDPOINT);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = -1000000;
    if (inUse) {
      httpResponseCode = http.PUT("{\"api_key\":\"https://free-api-ryfe.onrender.com\", \"name\": \"Washer 5\", \"timeLeftUserInput\": 45}");

    } else {
      httpResponseCode = http.PUT("{\"api_key\":\"https://free-api-ryfe.onrender.com\", \"name\": \"Washer 5\", \"timeLeftUserInput\": 0}");
    };
    Serial.print("HTTP Response: ");
    Serial.println(httpResponseCode);
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
    }
    http.end();

    httpGET("https://free-api-ryfe.onrender.com/washers");
    Serial.println();
  } else{
      Serial.println("Connection unsucessful");
  } 
}

void httpGET(char *endpoint){
  HTTPClient http;
  // Your Domain name with URL path or IP address with path
  http.begin(endpoint);
  // Send HTTP GET request
  int httpResponseCode = http.GET();
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String payload = http.getString();
    Serial.println(payload);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();
}