void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
  pinMode(LED_BUILTIN, OUTPUT);
}


void loop()
{
  char c;
  if (Serial.available() > 0)
  {
    c = Serial.read();
    switch (c)
    {
      case '0':
        digitalWrite(LED_BUILTIN, LOW);
        break;
      case '1':
        digitalWrite(LED_BUILTIN, HIGH);
        break;
    }
  }
}
