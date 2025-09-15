#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "Ruinquister";
const char* password = "00000000";

// Flask server (change IP to your PC's IP where Flask runs)
String serverName = "http://192.168.137.170:5000/add-data";

// Sensor 1 pins
const int trigPin1 = 4;
const int echoPin1 = 2;

// Sensor 2 pins
const int trigPin2 = 14;
const int echoPin2 = 26;

void setup() {
  Serial.begin(115200);

  // Set pin modes
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);

  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
}

float readDistance(int trigPin, int echoPin) {
  // Clear the trigger
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Send trigger pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure echo time
  long duration = pulseIn(echoPin, HIGH);

  // Convert to distance in cm
  return duration * 0.034 / 2;
}

void loop() {
  float distance1 = readDistance(trigPin1, echoPin1);
  float distance2 = readDistance(trigPin2, echoPin2);

  Serial.print("Sensor 1: ");
  Serial.print(distance1);
  Serial.println(" cm");

  Serial.print("Sensor 2: ");
  Serial.print(distance2);
  Serial.println(" cm");

  // Send to Flask every 5s
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // JSON payload
    String json = "{\"sensor1\": " + String(distance1) +
                  ", \"sensor2\": " + String(distance2) + "}";

    int httpResponseCode = http.POST(json);

    if (httpResponseCode > 0) {
      Serial.print("POST Response: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected!");
  }

  delay(5000); // 5 seconds interval
}
