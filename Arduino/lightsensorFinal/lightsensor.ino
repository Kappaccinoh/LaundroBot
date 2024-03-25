#include <WiFi.h> //Wifi library
#include <HTTPClient.h> // library used for HTTP requests
#include "esp_wpa2.h" //wpa2 library for connections to Enterprise networks
#include <ArduinoJson.h> // Library to convert strings to json objects in arduino

#define EAP_IDENTITY "e...." //if connecting from another corporation, use identity@organisation.domain in Eduroam 
#define EAP_USERNAME "e...." //oftentimes just a repeat of the identity
#define EAP_PASSWORD "" //your Eduroam password

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

const char* ssid = "NUS_STU"; // Eduroam SSID
const char* host = "www.google.com"; //external server domain for HTTP connection after authentification
#define ENDPOINT "https://free-api-ryfe.onrender.com/seventeenWashers/update"
int counter = 0;

void setup() {
  pinMode(2, OUTPUT);

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
    sensorValue0 = analogRead(analogInPin0);
    sensorValue1 = analogRead(analogInPin1);
    sensorValue2 = analogRead(analogInPin2);
    sensorValue3 = analogRead(analogInPin3);
    sensorValue4 = analogRead(analogInPin4);

    int sensorValues[5] = {sensorValue0, sensorValue1, sensorValue2, sensorValue3, sensorValue4};
    int sensorThresholds[5] = {3800, 3650, 2800, 3650, 3650};
    // print the results to the Serial Monitor:
    
    bool inUse[] = {false, false, false, false, false};

    for (int i = 0; i < 5; i++) {
      if (sensorValues[i] > sensorThresholds[i]) {
        digitalWrite(2, 1);
      } else {
        inUse[i] = true;
        digitalWrite(2, 0);
      }
    }

    for (int i = 0; i < 5; i++) {
      Serial.print("sensor " + String(i) + "output value: ");
      Serial.print(sensorValues[i]);
      Serial.print(" inUse="+String(inUse[i]));
      Serial.print("\n");
    }

    // wait 2 milliseconds before the next loop for the analog-to-digital
    // converter to settle after the last reading:
    delay(2);

    // Your Domain name with URL path or IP address with path
    http.begin(ENDPOINT);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = -1000000;

    String payload = httpGET("https://free-api-ryfe.onrender.com/seventeenwashers");
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);

    // Extract washer data
    JsonObject washer1 = doc[0];
    JsonObject washer2 = doc[1];
    JsonObject washer3 = doc[2];
    JsonObject washer4 = doc[3];
    JsonObject washer5 = doc[4];

    if (inUse[0]) { //washer1["timeLeftUserInput"].as<int>() == 0 && inUse[0]) {
      httpResponseCode = http.PUT("{\"api_key\":\"https://free-api-ryfe.onrender.com\", \"name\": \"Washer " + String(1) + "\", \"timeLeftUserInput\": 25}");
      Serial.print("sensor 1 sent");
    }
    if (inUse[1]) { //washer2["timeLeftUserInput"].as<int>() == 0 && inUse[1]) {
      httpResponseCode = http.PUT("{\"api_key\":\"https://free-api-ryfe.onrender.com\", \"name\": \"Washer " + String(2) + "\", \"timeLeftUserInput\": 25}");
      Serial.print("sensor 2 sent");
    }
    if (inUse[2]) { //washer3["timeLeftUserInput"].as<int>() == 0 && inUse[2]) {
      httpResponseCode = http.PUT("{\"api_key\":\"https://free-api-ryfe.onrender.com\", \"name\": \"Washer " + String(3) + "\", \"timeLeftUserInput\": 25}");
      Serial.print("sensor 3 sent");
    }
    if (inUse[3]) { //washer4["timeLeftUserInput"].as<int>()== 0 && inUse[3]) {
      httpResponseCode = http.PUT("{\"api_key\":\"https://free-api-ryfe.onrender.com\", \"name\": \"Washer " + String(4) + "\", \"timeLeftUserInput\": 25}");
      Serial.print("sensor 4 sent");
    }
    if (inUse[4]) { //washer5["timeLeftUserInput"].as<int>() == 0 && inUse[4]) {
      httpResponseCode = http.PUT("{\"api_key\":\"https://free-api-ryfe.onrender.com\", \"name\": \"Washer " + String(5) + "\", \"timeLeftUserInput\": 25}");
      Serial.print("sensor 5 sent");
    }
    http.end();
    Serial.println();
  } else{
      Serial.println("Connection unsucessful");
  } 
}

String httpGET(char *endpoint){
  HTTPClient http;
  String payload = "";
  // Your Domain name with URL path or IP address with path
  http.begin(endpoint);
  // Send HTTP GET request
  int httpResponseCode = http.GET();
  
  if (httpResponseCode>0) {
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();
  return payload;
}
