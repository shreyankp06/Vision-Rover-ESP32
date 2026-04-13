// Motor A (Left)
#define ENA 3
#define IN1 5
#define IN2 6

// Motor B (Right)
#define ENB 11
#define IN3 9
#define IN4 10

int speedLeft = 180;
int speedRight = 180;

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  digitalWrite(ENA, HIGH);
  digitalWrite(ENB, HIGH);
}

void loop() {

  if (Serial.available()) {

    char cmd = Serial.read();

    // 🔥 ignore newline characters (VERY IMPORTANT)
    if (cmd == '\n' || cmd == '\r') return;

    cmd = toupper(cmd);

    if (cmd == 'F') forward();
    else if (cmd == 'L') left();
    else if (cmd == 'R') right();
    else if (cmd == 'S') stopMotors();
  }
}

// FORWARD
void forward() {
  analogWrite(IN1, speedLeft);
  analogWrite(IN2, 0);

  analogWrite(IN3, speedRight);
  analogWrite(IN4, 0);
}

// LEFT
void left() {
  analogWrite(IN1, 80);
  analogWrite(IN2, 0);

  analogWrite(IN3, speedRight);
  analogWrite(IN4, 0);
}

// RIGHT
void right() {
  analogWrite(IN1, speedLeft);
  analogWrite(IN2, 0);

  analogWrite(IN3, 80);
  analogWrite(IN4, 0);
}

// STOP
void stopMotors() {
  analogWrite(IN1, 0);
  analogWrite(IN2, 0);
  analogWrite(IN3, 0);
  analogWrite(IN4, 0);
}
