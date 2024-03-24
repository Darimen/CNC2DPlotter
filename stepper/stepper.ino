#include <Stepper.h>
#include <Servo.h>
#include <math.h>

const int stepsPerRevolution = 2038;

String message, Gval, Xval, Yval, Zval, Ival, Jval, Rval;
int g, x = 0, y = 0, z = 0, i = 0, j = 0, r = 0;

Stepper step1 = Stepper(stepsPerRevolution, 3, 5, 4, 6);
Stepper step2 = Stepper(stepsPerRevolution, 7, 9, 8, 10);
const int CLOCKWISE = 1;
const int COUNTER_CLOCKWISE = -1;

Servo servo;

volatile int stop = 0;

int currentX = 0;
int currentY = 0;
int currentZ = 0;

void readFromSerial();                                         //Reads the input from Serial 9600 and then sends the input to the parse function
void parse(String message);                                    //attibues values to the variables of  g,x,y,z,i,j,r and then calls the funtions corresponding to the g value
void moveAll(int x, int y, int z);                             // moves the motors in  a liniar method
int sign(int nr);                                              //return 1 if positive, -1 if negative
void checkStop();                                              //checks if stop is 1
void moveg1(int x, int y, int z);                              //prints the values for x,y,z in serial and calls moveAll
void moveg2(int x, int y, int z, int i, int j, int r);         // moves the head in the necessary position and then calls moveCircular COUNTER_CLOCKWISE
void moveg3(int x, int y, int z, int i, int j, int r);         // moves the head in the necessary position and then calls moveCircular CLOCKWISE
void moveCircular(int I, int J, int R, int direction, int z);  //should move the head in a circular motion
void moveg28();                                                //moves the writing head home, calling moveAll(-dX, -dY, -currentZ)
void moveX(int ammount, int dir);                              //moves the writing head on horizontal
void moveY(int ammount, int dir);                              //moves the writing head on vertical
void movePen(int dir);                                         //lifts the writing head up or lets it down to write
void cancelCurrentMovement();                                  //an interrupt attached that if a button is pressed, sets the stop to 1

void setup() {

  pinMode(2, INPUT);
  //attachInterrupt(digitalPinToInterrupt(2), cancelCurrentMovement, CHANGE);
  servo.attach(11);
  servo.write(60);
  delay(1000);
  Serial.begin(9600);
  Serial.setTimeout(1000);
}

void loop() {
  if (Serial.available() > 0) {
    readFromSerial();
    Serial.print("OK");
  }
}



void readFromSerial() {
  message = Serial.readString();
  Serial.print("The message I got is:");
  Serial.println(message);
  parse(message);
  message = "";
}

void parse(String message) {

  Serial.println(" The parsing: ");

  if (message.charAt(0) == 'd') {
    demo2();
  }

  if (message.charAt(0) == 'G') {

    Gval = message.substring(message.indexOf("G") + 1, message.indexOf(" "));
    message = message.substring(message.indexOf(" ") + 1);

    g = Gval.toInt();
    Serial.print("The value of G: ");
    Serial.println(g);

    if (g == 0 || g == 1) {

      if (message.indexOf("X") >= 0) {
        Xval = message.substring(message.indexOf("X") + 1, message.indexOf(" "));
        x = Xval.toInt();
        message = message.substring(message.indexOf(" ") + 1);
      }
      if (message.indexOf("Y") >= 0) {
        Yval = message.substring(message.indexOf("Y") + 1, message.indexOf(" "));
        y = Yval.toInt();
        message = message.substring(message.indexOf(" ") + 1);
      }
      if (message.indexOf("Z") >= 0) {
        Zval = message.substring(message.indexOf("Z") + 1);
        z = Zval.toInt();
      }

      moveg1(x, y, z);

    } else if (g == 2 || g == 3) {

      if (message.indexOf("I") >= 0) {
        Ival = message.substring(message.indexOf("I") + 1, message.indexOf(" "));
        i = Ival.toInt();
        message = message.substring(message.indexOf(" ") + 1);
      }

      if (message.indexOf("J") >= 0) {
        Jval = message.substring(message.indexOf("J") + 1, message.indexOf(" "));
        j = Jval.toInt();
        message = message.substring(message.indexOf(" ") + 1);
      }

      if (message.indexOf("R") >= 0) {
        Rval = message.substring(message.indexOf("R") + 1);
        r = Rval.toInt();
        message = message.substring(message.indexOf(" ") + 1);
      }

      if (message.indexOf("X") >= 0) {
        Xval = message.substring(message.indexOf("X") + 1, message.indexOf(" "));
        x = Xval.toInt();
        message = message.substring(message.indexOf(" ") + 1);
      }
      if (message.indexOf("Y") >= 0) {
        Yval = message.substring(message.indexOf("Y") + 1, message.indexOf(" "));
        y = Yval.toInt();
        message = message.substring(message.indexOf(" ") + 1);
      }
      if (message.indexOf("Z") >= 0) {
        Zval = message.substring(message.indexOf("Z") + 1);
        z = Zval.toInt();
      }

      if (g == 2) {
        moveg2(x, y, z, i, j, r);
      } else {
        moveg3(x, y, z, i, j, r);
      }
    } else if (g == 28) {
      moveg28();
    } else {
      Serial.println("ERROR");
    }

    x = 0;
    y = 0;
    z = 0;
    i = 0;
    j = 0;
    r = 0;
    stop = 0;
  }
}

void demo2() {
  for (int i = 0; i < 3; i++) {
    moveAll(1000, -1000, 1);
    moveAll(1000, -1000, -1);
  }

  delay(1000);

  for (int i = 0; i < 3; i++) {
    moveAll(-1000, 1000, -1);
    moveAll(-1000, 1000, 1);
  }
}

void moveAll(int x, int y, int z) {
  int ratio = 0;
  int count = 0;
  if (stop) {
    x = 0;
    y = 0;
    z = 0;
  }
  currentZ += z;

  if (x * sign(x) > y * sign(y)) {
    ratio = x * sign(x) / y * sign(y);

    while (x != 0 || y != 0 || z != 0) {
      checkStop();
      if (x * sign(x) > 0) {
        moveX(1, sign(x));
        x = x - sign(x);
      }

      if (y * sign(y) > 0) {
        if (ratio == count) {
          moveY(1, sign(y));
          y = y - sign(y);
          count = 0;
        }
        count++;
      }
      if (z * sign(z) > 0) {
        movePen(z);
        z = 0;
      }
    }
  } else {
    ratio = y * sign(y) / x * sign(x);

    while (y != 0 || x != 0 || z != 0) {
      checkStop();
      if (y * sign(y) > 0) {
        moveY(1, sign(y));
        y = y - sign(y);
      }

      if (x * sign(x) > 0) {
        if (ratio == count) {
          moveX(1, sign(x));
          x = x - sign(x);
          count = 0;
        }
        count++;
      }
      if (z * sign(z) > 0) {
        movePen(z);
        z = 0;
      }
    }
  }
}

int sign(int nr) {
  if (nr < 0)
    return -1;
  return 1;
}

void checkStop() {
  if (stop) {
    x = 0;
    y = 0;
    z = 0;
  }
}

void moveCircular(int I, int J, int R, int direction, int z) {
  int centerX = currentX + I;
  int centerY = currentY + J;

  float startAngle = atan2(currentY - centerY, currentX - centerX);
  float endAngle = startAngle + direction * 2 * PI;

  for (int step = 0; step <= stepsPerRevolution; step++) {
    float angle = startAngle + direction * (2 * PI * step / stepsPerRevolution);

    if (direction == COUNTER_CLOCKWISE && angle < startAngle) {
      angle += 2 * PI;
    }

    int x = centerX + R * cos(angle);
    int y = centerY + R * sin(angle);
    moveAll(x, y, z);
    delay(100);
  }
}


void moveg1(int x, int y, int z) {
  Serial.print("the values for x");
  Serial.println(x);
  Serial.print("the values for y");
  Serial.println(y);
  Serial.print("the values for z");
  Serial.println(z);
  moveAll(x, y, z);
}

void moveg2(int x, int y, int z, int i, int j, int r) {
  Serial.print("the values for x");
  Serial.println(x);
  Serial.print("the values for y");
  Serial.println(y);
  Serial.print("the values for z");
  Serial.println(z);
  Serial.print("the values for i");
  Serial.println(i);
  Serial.print("the values for j");
  Serial.println(j);
  Serial.print("the values for r");
  Serial.println(r);
  moveAll(x, y, 0);
  moveCircular(i, j, r, 1, z);
}

void moveg3(int x, int y, int z, int i, int j, int r) {
  Serial.print("the values for x");
  Serial.println(x);
  Serial.print("the values for y");
  Serial.println(y);
  Serial.print("the values for z");
  Serial.println(z);
  Serial.print("the values for i");
  Serial.println(i);
  Serial.print("the values for j");
  Serial.println(j);
  Serial.print("the values for r");
  Serial.println(r);
  moveAll(x, y, 0);
  moveCircular(i, j, r, -1, z);
}

void moveg28() {
  Serial.println("Homing...");
  moveAll(-currentX, -currentY, -currentZ);
}

void moveX(int ammount, int dir) {
  currentX += ammount;
  step1.setSpeed(10);
  step1.step(ammount * dir);
}

//IF POSITIVE, THEN BACK
void moveY(int ammount, int dir) {
  currentY += ammount;
  step2.setSpeed(10);
  step2.step(ammount * dir);
}

void demo() {
  step1.setSpeed(10);
  step1.step(stepsPerRevolution);

  step1.setSpeed(10);
  step1.step(-stepsPerRevolution);

  step2.setSpeed(10);
  step2.step(stepsPerRevolution);

  step2.setSpeed(10);
  step2.step(-stepsPerRevolution);

  servo.write(90);
  delay(1000);
  servo.write(0);
  delay(1000);
}

void movePen(int dir) {
  if (dir > 0) {
    //down
    servo.write(90);
  } else if (dir == -100) {
    servo.write(0);
  } else {
    //up
    servo.write(60);
  }
}

void cancelCurrentMovement() {
  Serial.println("Stop changed!");
  stop = 1;
}