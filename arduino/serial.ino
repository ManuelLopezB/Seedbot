// Motor A
int ENA = 8;
int IN1 = 9;
int IN2 = 10;

// Motor B
int ENB = 13;
int IN3 = 11;
int IN4 = 12;

void setup()
{
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  Serial.begin(115200);
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB
  }
  pinMode(LED_BUILTIN, OUTPUT);
}

void izquierda()
{
  // Direccion motor A
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 100); // Velocidad motor A
}

void derecha()
{
  // Direccion motor B
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 100); // Velocidad motor B
}

void parar()
{
  // Direccion motor A
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0); // Velocidad motor A
  // Direccion motor B
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0); // Velocidad motor A
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
      parar();
      break;
    case '1':
      //        digitalWrite(LED_BUILTIN, HIGH);
      izquierda();
      break;
    case '2':
      digitalWrite(LED_BUILTIN, HIGH);
      derecha();
      break;
    }
  }
}