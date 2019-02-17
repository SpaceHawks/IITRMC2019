#include "RMCKangaroo.hpp"

extern bool stopAll;

/*! Constructor */
LinearActuator::LinearActuator(KangarooSerial& K, char name) :KangarooChannel(K, name)
{
}

/*!
Initiates the Kangaroo. Gets min and max positions for Linear Actuator.
*/
void LinearActuator::begin() {
  commandTimeout(500);
  errorStatus = start();
  if (errorStatus == KANGAROO_NO_ERROR)
  {
    getExtremes();
  }
}
/*!
Extends Linear Actuator to target position with set speed while in range.
Powers down when completed.
*/
void LinearActuator::loop()
{
  if (errorStatus == KANGAROO_NO_ERROR)
  {
    if (targetVal >= min && targetVal <= max && (targetVal != lastVal || speed != lastSpeed)) {
      done = false;
      p(targetVal, speed);
      lastVal = targetVal;
      lastSpeed = speed;
    }
    status = getP();
    errorStatus = status.error();
    if (status.done()) {
      powerDown();
      done = true;
    }
  }
}
/*!
Computes min and max values for position of Linear Actuator.
Sets default max Speed.
*/
void LinearActuator::getExtremes()
{
  long absMin = getMin().value();
  long absMax = getMax().value();
  long safeBound = (absMax - absMin)*0.02;
  min = (absMin + safeBound);
  max = absMax - safeBound;
  maxSpeed = 208;
  //maxSpeed = 0.5 * (absMax - absMin);
  Serial.println("max speed is: " + String(maxSpeed));
}
/*!
Sets target position for Linear Actuator between 0 and 100.
*/
void LinearActuator::setTargetPosDirect(long pos)
{
  if (targetVal >= min && targetVal <= max) {
    targetVal = pos;
  }
}
/*!
Sets target position and speed for Linear Actuator.
*/
void LinearActuator::setTargetPosAndSpeed(long pos, long newSpeed) { //val = 0% to 100%
  setTargetPos(pos);
  setSpeed(newSpeed);
}
/*!
Sets target position for Linear Actuator scaled between min and max.
*/
void LinearActuator::setTargetPos(long pos) {
  if (pos >= 0 && pos <= 100) {
    targetVal = map(pos, 0, 100, min, max);
  }
}
/*!
Sets speed for Linear Actuator scaled between 0 and max speed.
*/
void LinearActuator::setSpeed(long newSpeed) {
  if (newSpeed >= 0 && newSpeed <= 100) {
    speed = map(newSpeed, 0, 100, 0, maxSpeed);
  }
}
/*!
Gets current position of Linear Actuator.
*/
long LinearActuator::getCurrentVal()
{
  return status.value();
}
void LinearActuator::stop()
{
  setTargetPos(status.value());
  setSpeed(speed);
}
/*!
Constructor
Instantiates PID control object. Sets default values and range.
Instaites objects to control Linear Actuators individually.
*/
LinearActuatorPair::LinearActuatorPair(KangarooSerial & K, char name)
{
  syncPID = new PID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
  Setpoint = 0;
  syncPID->SetMode(AUTOMATIC);
  syncPID->SetOutputLimits(-5, 5);
  channel[0] = new LinearActuator(K, name);
  channel[1] = new LinearActuator(K, name + 1);
}
/*!
\
*/
long * LinearActuatorPair::getCurrentVal()
{
  return nullptr;
}
long LinearActuatorPair::getPos()
{
  return map(channel[0]->status.value(), channel[0]->min, channel[0]->max, 0, 100);
}
/*!
\
*/
void LinearActuatorPair::setSpeed(long newSpeed)
{// set speed in the range if 0 - 100
  if (newSpeed != lastSpeed && newSpeed >= 0 && newSpeed <= 100)
  {
    channel[0]->setSpeed(newSpeed);
    channel[1]->setSpeed(newSpeed);
    lastSpeed = newSpeed; //fix this
    speed = newSpeed;
  }
}
/*!
Sets target value for position of Linear Actuator.
*/
void LinearActuatorPair::setTargetPos(long pos)
{
  targetVal = pos;
}
void LinearActuatorPair::setTargetPosAndSpeed(long pos, long speed)
{
  setTargetPos(pos);
  setSpeed(speed);
}

/*!
Computes gap between Linear Actuators and fixes it if greater than tolerance.
Moves Linear Actuator Pair to target value controlled by PID.
Executes loops of all channels.
*/
void LinearActuatorPair::loop()
{
  long tempTargetVal = targetVal;
  if (channel[0]->done && channel[1]->done)
  {
    channel[0]->setTargetPos(tempTargetVal);
    channel[1]->setTargetPos(tempTargetVal);
  }
  else
  {
    long la1 = channel[0]->status.value();
    long la2 = channel[1]->status.value();
    Input = la2 - la1;
    long gap = Input;
    syncPID->Compute();
    //Serial.println(String(targetVal)+"     "+String(Output));
    long scaledLa1 = map(la1, channel[0]->min, channel[0]->max, 0, 100);
    long scaledLa2 = map(la2, channel[0]->min, channel[0]->max, 0, 100);
    if ((tempTargetVal - scaledLa1) > 1)
    {
      channel[1]->setSpeed(speed + Output);
    }
    else if ((tempTargetVal - scaledLa1) < -1)
    {
      channel[1]->setSpeed(speed - Output);
    }
    //Serial.println(gap);
    if (abs(gap) > 25) {
      if (!isSyncing) {
        isSyncing = true;

        channel[0]->setTargetPosDirect(la1);
        channel[1]->setTargetPosDirect(la1);
      }
    }
    else {
      if (isSyncing && abs(gap) < 15)
      {
        isSyncing = false;
      }
      channel[0]->setTargetPos(tempTargetVal);
      channel[1]->setTargetPos(tempTargetVal);
    }
  }
  channel[0]->loop();
  channel[1]->loop();
  currentPos[0] = channel[0]->getCurrentVal();
  currentPos[1] = channel[1]->getCurrentVal();

}
/*!
Executes begin methods of all channels.
Sets speed of Linear Actuator.
*/
void LinearActuatorPair::begin()
{
  channel[0]->begin();
  channel[1]->begin();
  setSpeed(100);
}
void LinearActuatorPair::getStatus(KangarooError *output, int startIndex)
{
  for (int i = 0; i < 2; i++)
  {
    channel[i]->getStatus(output, startIndex + i);
  }
}

void LinearActuatorPair::stop()
{
  setTargetPos(currentPos[0]);
  setSpeed(speed);
}

Motor::Motor(KangarooSerial& K, char name) :KangarooChannel(K, name)
{
}
void Motor::begin()
{
  commandTimeout(500);
  errorStatus = start();
  //KangarooError error = start();
  //Serial.println(error);
}
void Motor::setTargetPos(long pos)
{
  mode = 1;
  targetPos = pos;
}
void Motor::loop()
{
  if (errorStatus == KANGAROO_NO_ERROR)
  {
    long tempSpeed = speed;
    //Serial.println("tempSpeed "+String(tempSpeed));
    //Serial.println("lastSpeed " + String(lastSpeed));
    //Serial.println("speedLimit " + String(speedLimit));
    if (tempSpeed != lastSpeed && tempSpeed >= -speedLimit && tempSpeed <= speedLimit)
    {
      s(tempSpeed);
      lastSpeed = tempSpeed;

    }
    status = getS();
    errorStatus = status.error();
  }
}
void Motor::setTargetSpeed(long speed) {
  if (speed >= -100 && speed <= 100) {
    this->speed = map(speed, -100, 100, -speedLimit, speedLimit);
  }
}
long Motor::getCurrentSpeed()
{
  return map(status.value(), -WHEEL_MOTOR_MECHANICAL_SPEED_LIMIT, WHEEL_MOTOR_MECHANICAL_SPEED_LIMIT, -100, 100);
}
void Motor::setSpeedLimit(long newSpeed) //speed is percentage
{
  if (newSpeed > 0 && newSpeed <= 100) {
    speedLimit = map(newSpeed, 0, 100, 0, WHEEL_MOTOR_MECHANICAL_SPEED_LIMIT);
  }
}
void Motor::move(long angle, long speed)
{
  long val = angle / 360 * 2040;
  pi(val, speed).wait();
  //done = true;
}
void Motor::stop() {

  this->speed = 0;

}

Motors::Motors(KangarooSerial & K, char name)
{
  channel[0] = new Motor(K, name);
  channel[1] = new Motor(K, name + 1);
  channel[2] = new Motor(K, name + 2);
  channel[3] = new Motor(K, name + 3);
  setSpeedLimit(25);
}

void Motors::setSpeedLimit(int newSpeed) { // speed is percent
  if (newSpeed > 0 && newSpeed <= 100)
  {
    for (int i = 0; i < 4; i++) {
      channel[i]->setSpeedLimit(newSpeed);
    }
  }
}

void Motors::loop()
{
  for (int i = 0; i < 4; i++) {
    channel[i]->mode = mode;
  }
  if (mode == 1 && alreadySetTargetPos == false) {
    if (angle <= 180 && angle >= -180) {
      long leftPos;
      long rightPos;
      if (angle < 0)
      {
        leftPos = -angle;
        rightPos = angle;
      }
      else if (angle > 0)
      {
        leftPos = angle;
        rightPos = -angle;
      }
      else {
        leftPos = targetPos;
        rightPos = targetPos;
      }
      channel[FRONT_LEFT]->setTargetPos(-leftPos);
      channel[FRONT_RIGHT]->setTargetPos(-rightPos);
      channel[REAR_LEFT]->setTargetPos(leftPos);
      channel[REAR_RIGHT]->setTargetPos(rightPos);
      alreadySetTargetPos = true; //fix this
    }
  }
  //
  channel[FRONT_LEFT]->setTargetSpeed(-leftSpeed);
  channel[FRONT_RIGHT]->setTargetSpeed(-rightSpeed);
  channel[REAR_LEFT]->setTargetSpeed(leftSpeed);
  channel[REAR_RIGHT]->setTargetSpeed(rightSpeed);
  for (int i = 0; i < 4; i++)
  {
    if (channel[i]->done == true)
    {
      channel[i]->done == false;
      channel[i]->setTargetSpeed(0);
    }
    channel[i]->loop();
    currentSpeeds[i] = channel[i]->getCurrentSpeed();
  }
}
void Motors::begin()
{
  for (int i = 0; i < 4; i++) {
    channel[i]->begin();
  }
}

void Motors::drive(long drive, long turn)
{
  if (drive >= -100 && drive <= 100 && turn >= -100 && turn <= 100) {
    //do left and right speed calciulation here
    leftSpeed = drive;
    rightSpeed = drive;
    if (turn == -100) {
      leftSpeed = -drive;
    }
    else if (turn < 0 && turn >-100) {
      leftSpeed = drive * (1 + (float)turn / 100);
    }
    else if (turn < 100 && turn > 0) {
      rightSpeed = drive * (1 - (float)turn / 100);
    }
    else if (turn == 100) {
      rightSpeed = -drive;
    }
  }
}

/*!
Powers down all wheel motors.
*/
void Motors::shutDown()
{
  for (int i = 0; i < 4; i++) {
    channel[i]->powerDown();
  }
}

void Motors::tankDrive(long leftSpeed, long rightSpeed)
{
  if (leftSpeed >= -100 && leftSpeed <= 100 && rightSpeed >= -100 && rightSpeed <= 100) {
    this->leftSpeed = leftSpeed;
    this->rightSpeed = rightSpeed;
  }
}

void Motors::clearAngle()
{
  angle = 0;
}
void Motors::setPos(long pos)
{
  mode = 1;
  targetPos = pos * 2040;
  alreadySetTargetPos == false;
}
void Motors::getStatus(KangarooError *output, int startIndex)
{
  for (int i = 0; i < 4; i++)
  {
    channel[i]->getStatus(output, startIndex + i);
  }
}
void Motors::setAngle(long angle)
{
  if (angle >= -180 && angle <= 180)
  {
    mode = 1;
    this->angle = angle * 2040;
    alreadySetTargetPos == false;
  }
}

void Motors::moveStraight(boolean signal)
{
  if (signal = true)
    setPos(30);
  else
    setPos(-30);
}

void Motors::rotate(boolean signal)
{
  if (signal = true)
    setAngle(5);
  else
    setAngle(-5);

}

void Motors::moveSlant(boolean signal1, boolean signal2)
{
  moveStraight(signal1);
  rotate(signal2);
}

void Motors::moveTo(double x1, double y1, double x2, double y2)
{
  double y = y2 - y1;
  double x = x2 - x1;
  double angle = atan(y / x);
  double r = sqrt((x*x) + (y*y));
  setAngle(180 - angle); // 180 should be replaced with actual orientation
  setPos(r);
}

void Motors::stop()
{
  this->leftSpeed = 0;
  this->rightSpeed = 0;
}
Auger::Auger(int enablePin, int reversePin)
{
  attach(enablePin, reversePin);
}

void Auger::changeControlPins(int enablePin, int reversePin)
{
  release();
  attach(enablePin, reversePin);
}

void Auger::attach(int enablePin, int reversePin)// only accept degital pins 2-13
{
  if (enablePin >= 2 && enablePin <= 13 && reversePin >= 2 && reversePin <= 13 && enablePin != reversePin)
  {
    this->enablePin = enablePin;
    this->reversePin = reversePin;
    pinMode(enablePin, OUTPUT);
    pinMode(reversePin, OUTPUT);
  }
}

void Auger::release()
{
  pinMode(enablePin, INPUT);
  pinMode(reversePin, INPUT);
}

void Auger::forward()
{
  digitalWrite(enablePin, HIGH);
  digitalWrite(reversePin, LOW);
}

void Auger::reverse()
{
  digitalWrite(enablePin, HIGH);
  digitalWrite(reversePin, HIGH);
}

void Auger::setDirection(int enable, int direction)
{
  if (enable == 1)
  {
    if (direction == 1) //reverse
    {
      reverse();
    }
    else if (direction == 0) //reverse
    {
      forward();
    }
  }
  else if (enable == 0) {
    stop();
  }
}

void Auger::stop()
{
  digitalWrite(enablePin, LOW);
  digitalWrite(reversePin, LOW);
}

/*!
Constructor. Initilizes Arduino pins connected to the Kangaroo.
\param potPin the Arduino analog pin number. Default is 0.
*/
RMCKangaroo::RMCKangaroo(USARTClass &serial)
{
  SerialPort = &serial;
  K = new KangarooSerial(*SerialPort);
  motors = new Motors(*K, '1');
  linearActuatorPair = new LinearActuatorPair(*K, '1');
  auger = new Auger(2, 3);
  slider = new Slider(*K, '7');
  conveyor = new Conveyor(*K, '8');
}
/*!
Executes the loop of the right Linear Actuator
*/
void RMCKangaroo::loop()
{
  motors->loop();
  linearActuatorPair->loop();
  slider->loop();
  conveyor->loop();
}
/*!
Initiates Serial Communication.
Executes begin methods of all Linear Actuators and Motors.
*/
void RMCKangaroo::begin() {
  SerialPort->begin(9600);
  stopAll = false; // global
  motors->begin();
  /*linearActuatorPair->begin();
  slider->begin();
  conveyor->begin();*/
}

void RMCKangaroo::getStatus(KangarooError *errorStatuses)
{
  linearActuatorPair->getStatus(errorStatuses, 0);
  motors->getStatus(errorStatuses, 2);
  slider->getStatus(errorStatuses, 6);
  conveyor->getStatus(errorStatuses, 7);

  for (int i = 0; i < 8; i++)
  {
    Serial.print(errorStatuses[i]);
    if (errorStatuses[i] == KANGAROO_NO_ERROR)
      Serial.print("No_error ");
    else if (errorStatuses[i] == KANGAROO_NOT_STARTED)
      Serial.print("Not_Started ");
    else if (errorStatuses[i] == KANGAROO_NOT_HOMED)
      Serial.print("Not_homed ");
    else if (errorStatuses[i] == KANGAROO_CONTROL_ERROR)
      Serial.print("Control_error ");
    else if (errorStatuses[i] == KANGAROO_WRONG_MODE)
      Serial.print("Wrong_mode ");
    else if (errorStatuses[i] == KANGAROO_SERIAL_TIMEOUT)
      Serial.print("Serial_timeout ");
    else if (errorStatuses[i] == KANGAROO_TIMED_OUT)
      Serial.print("Command_timeout ");
    Serial.print(" ");
  }
  Serial.println();
}

void RMCKangaroo::stop() {
  motors->stop();
  linearActuatorPair->stop();
  slider->stop();
  auger->stop();
  conveyor->stop();
}

Slider::Slider(KangarooSerial & K, char name) : LinearActuator(K, name)
  { maxSpeed = 208; }
Conveyor::Conveyor(KangarooSerial & K, char name) : Motor(K, name)
  { setSpeedLimit(100); }

void Conveyor::setSpeedLimit(long newSpeed)
{
  if (newSpeed > 0 && newSpeed <= 100)
    speedLimit = map(newSpeed, 0, 100, 0, CONVEYOR_MOTOR_MECHANICAL_SPEED_LIMIT);
}

void Actuator::getStatus(KangarooError * output, int startIndex)
  { output[startIndex] = errorStatus; }
