// -------------------------------------------
//
//  Poject: Lab1_task1
//  Group: 35
//  Students: Niels van Griethuijsen & Fabiënne Voorhorst
//  Date: 6/2/2025
//  ------------------------------------------


// put your setup code here
void setup() {

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // initialize serial port and wait for port to open:
  Serial.begin(9600);

  // wait for serial port to connect. Needed for native USB port only
  while (!Serial) {} 
  
  // init digital IO pins
  digitalWrite(LED_BUILTIN, LOW); 
}


// put your main code here
void loop() {
  String command = Serial.readStringUntil('\n');
  if(command == "on") {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("LED on");
  }
  else if (command == "off") {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("LED off");
  }
}
