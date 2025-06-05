// -------------------------------------------
//
//  Poject: Lab1_task1
//  Group: 35
//  Students: Niels van Griethuijsen & Fabiënne Voorhorst
//  Date: 6/2/2025
//  ------------------------------------------
#include <Arduino_LSM6DS3.h>
#include <string.h>

#define IMU IMU_LSM6DS3

// put your setup code here
void setup() {

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // initialize serial port and wait for port to open:
  Serial.begin(9600);
  // delay(2000); //om verbinding te kunnen maken

  // wait for serial port to connect. Needed for native USB port only
  while (!Serial) {} 
  
  // init digital IO pins
  digitalWrite(LED_BUILTIN, LOW); 

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    exit(1); //stop hier
  }

  // Serial.print("Accelerometer sample rate = ");
  // Serial.print(IMU.accelerationSampleRate());
  // Serial.println(" Hz");
  // Serial.println();
  // Serial.println("Acceleration in g's");
  // Serial.println("X\tY\tZ");
}


// put your main code here
void loop() {

  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    String data = String(x) + "," + String(y) + "," + String(z);
    Serial.println(data);
  }
  delay(10);
}
