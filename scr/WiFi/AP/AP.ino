#include <WiFi.h>

// Define the SSID and password for the Access Point
const char* ssid = "ESP32-Access-Point";
const char* password = "123456789";

void setup() {
  Serial.begin(115200);
  // Start the Wi-Fi Access Point
  WiFi.softAP(ssid, password);

  // Print the IP address of the Access Point
  Serial.println("Access Point started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());
}

int prevClientCount = 0;

void loop() {
  int clientCount = WiFi.softAPgetStationNum();
  if (clientCount > prevClientCount) {
    Serial.println("New device connected!");
    Serial.print("Total connected devices: ");
    Serial.println(clientCount);
  }
  prevClientCount = clientCount;
  delay(1000); // Add a delay to avoid overwhelming the serial output
}