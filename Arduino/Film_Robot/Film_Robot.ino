

//~~~~~~~~~~~~~~~~~~~~~~DC MOTORS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~//
#define L_PWM_1 5
#define R_PWM_1 6
#define L_EN_1 7
#define R_EN_1 8

#define L_PWM_2 3
#define R_PWM_2 11
#define L_EN_2 12
#define R_EN_2 13

//~~~~~~~~~~~~~~~~~~~~~~SERVOS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~//
#include <Servo.h>
#define pitchPin 9
#define yawPin 10
Servo pitch;  // create servo object to control a servo
Servo yaw;
int pos_yaw = 65;    // variable to store the yaw servo position
int pos_pitch = 100;    // variable to store the pitch servo position
float joystick_thresh = 0.05;

//~~~~~~~~~~~~~~~~~~~~~~CONTROL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~//
long servoTime = 0;
long servoTime_prev = 0;

String data;
float rightStickHorizontal;
float rightStickVertical;
int servoSpeed = 1;
float motor1;
float motor2;
float motor1_command;
float motor2_command;

void setup() {

  pinMode(L_PWM_1, OUTPUT);
  pinMode(R_PWM_1, OUTPUT);
  pinMode(L_EN_1, OUTPUT);
  pinMode(R_EN_1, OUTPUT);
  digitalWrite(L_EN_1, HIGH);
  digitalWrite(R_EN_1, HIGH);


  pinMode(L_PWM_2, OUTPUT);
  pinMode(R_PWM_2, OUTPUT);
  pinMode(L_EN_2, OUTPUT);
  pinMode(R_EN_2, OUTPUT);
  digitalWrite(L_EN_2, HIGH);
  digitalWrite(R_EN_2, HIGH);
  delay(500);

  Serial.begin(9600);
  Serial.setTimeout(10);

  pitch.attach(pitchPin);
  yaw.attach(yawPin);
}
void loop() {
  
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('~');
    //Serial.print("From Arduino: ");

    int numData = countCharacter(data, ',') + 1;
    int lastCommaIndex = 0;
    float dataValues[numData];
    for (int i = 0; i < numData; i++) {
      int commaIndex = data.indexOf(',', lastCommaIndex);
      dataValues[i] = data.substring(lastCommaIndex, commaIndex).toFloat();
      lastCommaIndex = commaIndex + 1;
    }
    
    motor1 = dataValues[0];
    motor2 = dataValues[1];
    rightStickHorizontal = dataValues[2];
    rightStickVertical = dataValues[3];

    /*
      //Printing Back to RPi
      Serial.print(String(motorLeft));
      Serial.print("  ");
      Serial.print(String(motorRight));
      Serial.print("  ");
      Serial.print(String(rightStickHorizontal));
      Serial.print("  ");
      Serial.println(String(rightStickVertical));
    */
  }
  
  //UPDATE MOTORS
  if (abs(motor1)<joystick_thresh){
      motor1=0;
    }
  if (abs(motor2)<joystick_thresh){
    motor2=0;
  }
  
  if (motor1 >= 0) {
    analogWrite(L_PWM_2, abs(motor1) * 250);
    analogWrite(R_PWM_2, 0);
  }
  else {
    analogWrite(R_PWM_2, abs(motor1) * 250);
    analogWrite(L_PWM_2, 0);
  }

  if (motor2 >= 0) {
    analogWrite(R_PWM_1, abs(motor2) * 250);
    analogWrite(L_PWM_1, 0);
  }
  else {
    analogWrite(L_PWM_1, abs(motor2) * 250);
    analogWrite(R_PWM_1, 0);
  }
  
  servoTime = millis();
  if (servoTime - servoTime_prev > 50) {
    //UPDATE SERVOS
    if (abs(rightStickHorizontal)<joystick_thresh){
      rightStickHorizontal=0;
    }
    if (abs(rightStickVertical)<joystick_thresh){
      rightStickVertical=0;
    }
    pos_yaw = pos_yaw - 2*servoSpeed * rightStickHorizontal;
    if (pos_yaw>180){
      pos_yaw = 180;
    }
    else if (pos_yaw<0){
      pos_yaw = 0;
    }
    yaw.write(pos_yaw);
    //Serial.println(String(pos_yaw));
    pos_pitch = pos_pitch + servoSpeed * rightStickVertical;
    if (pos_pitch>120){
      pos_pitch = 120;
    }
    else if (pos_pitch<85){
      pos_pitch = 85;
    }
    pitch.write(pos_pitch);
    //Serial.println(String(pos_pitch));
    servoTime_prev = servoTime;
  }

}

int countCharacter(const String &inputString, char targetChar) {
  int count = 0;
  // Iterate through each character in the string
  for (int i = 0; i < inputString.length(); i++) {
    // Check if the current character is the target character
    if (inputString[i] == targetChar) {
      count++;
    }
  }
  return count;
}
