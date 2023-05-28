#include "secrets.h"
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "EmonLib.h"   //https://github.com/openenergymonitor/EmonLib
#include "WiFi.h"
#include <Wire.h>
#include <SPI.h>
 
#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"

EnergyMonitor emon_main;
EnergyMonitor emon_dev1;
EnergyMonitor emon_dev2;

#define vCalibration 106.8
#define currCalibration 0.52

float voltage_main=0,current_main=0,power_main=0;
float voltage_dev1=0,current_dev1=0,power_dev1=0;
float voltage_dev2=0,current_dev2=0,power_dev2=0;

int main_voltage_pin = 35;
int main_current_pin = 34;
int main_relay_pin = 32;

int dev1_voltage_pin = 35;
int dev1_current_pin = 34;
int dev1_relay_pin = 32;

int dev2_voltage_pin = 35;
int dev2_current_pin = 34;
int dev2_relay_pin = 32;

 
WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);

void messageHandler(char* topic, byte* payload, unsigned int length)
{
  Serial.print("incoming: ");
  Serial.println(topic);
 
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  const char* message = doc["message"];

  if(strcmp(message,"mainon") == 0)
  {
    digitalWrite(main_relay_pin,false);
  }
  else if(strcmp(message,"mainoff") == 0)
  {
    digitalWrite(main_relay_pin,true);
  }
  else if(strcmp(message,"dev1on") == 0)
  {
    digitalWrite(dev1_relay_pin,false);
  }
  else if(strcmp(message,"dev1off") == 0)
  {
    digitalWrite(dev1_relay_pin,true);
  }
  else if(strcmp(message,"dev2on") == 0)
  {
    digitalWrite(dev2_relay_pin,false);
  }
  else if(strcmp(message,"dev2off") == 0)
  {
    digitalWrite(dev2_relay_pin,true);
  }
  
  Serial.println(message);
}
 
void connectAWS()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 
  Serial.println("Connecting to Wi-Fi");
 
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
 
  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
 
  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.setServer(AWS_IOT_ENDPOINT, 8883);
 
  // Create a message handler
  client.setCallback(messageHandler);
 
  Serial.println("Connecting to AWS IOT");
 
  while (!client.connect(THINGNAME))
  {
    Serial.print(".");
    delay(100);
  }
 
  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }
 
  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
 
  Serial.println("AWS IoT Connected!");
}
 
void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["voltage_main"] = voltage_main;
  doc["current_main"] = current_main;
  doc["power_main"] = power_main;

  doc["voltage_dev1"] = voltage_dev1;
  doc["current_dev1"] = current_dev1;
  doc["power_dev1"] = power_dev1;

  doc["voltage_dev2"] = voltage_dev2;
  doc["current_dev2"] = current_dev2;
  doc["power_dev2"] = power_dev2;
  
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client
 
  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}
 
void setup()
{
  Serial.begin(115200);
  pinMode(main_relay_pin, OUTPUT);
  digitalWrite(main_relay_pin,LOW);

  pinMode(dev1_relay_pin, OUTPUT);
  digitalWrite(dev1_relay_pin,LOW);

  pinMode(dev2_relay_pin, OUTPUT);
  digitalWrite(dev2_relay_pin,LOW);
  
  emon_main.voltage(main_voltage_pin, vCalibration, 1.7); // Voltage: input pin, calibration, phase_shift
  emon_main.current(main_current_pin, currCalibration); // Current: input pin, calibration.

  emon_dev1.voltage(dev1_voltage_pin, vCalibration, 1.7); // Voltage: input pin, calibration, phase_shift
  emon_dev1.current(dev1_current_pin, currCalibration); // Current: input pin, calibration.

  emon_dev2.voltage(dev2_voltage_pin, vCalibration, 1.7); // Voltage: input pin, calibration, phase_shift
  emon_dev2.current(dev2_current_pin, currCalibration); // Current: input pin, calibration.
  
  connectAWS();
}
 
void loop()
{
  emon_main.calcVI(20, 2000);
  voltage_main = emon_main.Vrms;
  current_main = emon_main.Irms;
  power_main = emon_main.apparentPower;

  emon_dev1.calcVI(20, 2000);
  voltage_dev1 = emon_dev1.Vrms;
  current_dev1 = emon_dev1.Irms;
  power_dev1 = emon_dev1.apparentPower;

  emon_dev2.calcVI(20, 2000);
  voltage_dev2 = emon_dev2.Vrms;
  current_dev2 = emon_dev2.Irms;
  power_dev2 = emon_dev2.apparentPower;
 
    Serial.print("Vrms: ");
    Serial.print(emon_main.Vrms, 2);
    Serial.print("V");
    Serial.print("\tIrms: ");
    Serial.print(emon_main.Irms, 4);
    Serial.print("A");
    Serial.print("\tPower: ");
    Serial.print(emon_main.apparentPower, 4);
    Serial.print("W");
    Serial.println();
 
  publishMessage();
  client.loop();
  delay(5000);
}
