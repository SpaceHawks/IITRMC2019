#pragma once
#include <Kangaroo.h>
#include "PID_v1.hpp"


#define DEFAULT_NUMBER_OF_CHANNEL 10
#define FRONT_RIGHT 0 //channel 3
#define FRONT_LEFT 1 //channel 4
#define REAR_LEFT 3 //channel 5
#define REAR_RIGHT 2 //channel 6
#define WHEEL_MOTOR_MECHANICAL_SPEED_LIMIT 20000
#define SLIDER_MOTOR_MECHANICAL_SPEED_LIMIT 20000

/*!
\class Actuator
\brief This parent class ensures Linear Actuator and motor class inherits the general functions.
*/
class Actuator {
public:
  void begin();
  void loop();
  void setTargetVal(long val);
  void setTargetVal(long val1, long val2); //For controlling 2 Kangaroo Channels
  long *getCurrentVal();
  KangarooError errorStatus;
  void getStatus(KangarooError * output, int startIndex);

};

/*!
\class LinearActuator
\Inherits KangarooChannel and Actuator
\brief This class controls a single Linear Actuator
*/
class LinearActuator : public KangarooChannel, public Actuator {
public:
  LinearActuator(KangarooSerial& K, char name);
  long min;
  long max;
  long maxSpeed;
  long speed;
  long lastSpeed;
  long targetVal;
  long lastVal;
  long getCurrentVal();
  void stop();
  bool done = false;
  //  void setSpeed(long speed);
  void getExtremes();
  void setTargetPosDirect(long pos);
  void setTargetPosAndSpeed(long pos, long newSpeed);
  void setSpeed(long newSpeed);
  void setTargetPos(long pos);
  void loop();
  KangarooStatus status;
  void begin();
};

/*!
\class LinearActuatorPair
\brief This class controls two Linear Actuator synchronously.
*/
class LinearActuatorPair {
public:
  LinearActuatorPair(KangarooSerial& K, char name);
  LinearActuator* channel[2];
  long targetVal;
  long lastVal;
  long lastSpeed;
  bool isSyncing;
  long *getCurrentVal();
  long getPos();
  //void setTargetVal(long pos, long newSpeed);
  void setSpeed(long newSpeed);
  void setTargetPos(long pos);
  void setTargetPosAndSpeed(long pos, long speed);
  void loop();
  void begin();
  long speed;
  char currentPos[3];
  //Define Variables we'll be connecting to
  double Setpoint, Input, Output;
  void getStatus(KangarooError *output, int i);

  void stop();

  //Specify the links and initial tuning parameters
  double Kp = 0.4, Ki = 0, Kd = 0;
  PID* syncPID;
};

class Motor : public KangarooChannel, public Actuator {
public:
  Motor(KangarooSerial& K, char name);
  bool done = false;
  long speedLimit;
  long mechanicalSpeedLimit = WHEEL_MOTOR_MECHANICAL_SPEED_LIMIT;
  long lastSpeed = 1;
  long speed = 0;
  int mode; //0 - speed , 1 - position
  long targetPos;
  long getCurrentSpeed();
  void move(long angle, long speed);
  void stop();
  void setSpeedLimit(long newSpeed);
  //void moveAtSpeed(long val, long newSpeed);
  void setTargetVal(long val);
  void loop();
  void setTargetSpeed(long val);
  //void setTargetVal(long val, long distance);
  KangarooStatus status;
  void begin();
  void setTargetPos(long pos);
};

class Motors {
public:
  //long drive = 101;
  long leftSpeed = 0;
  long rightSpeed = 0;
  //long turn = 101;
  long angle = 0;
  long targetPos = 0;
  bool alreadySetTargetPos = true;
  int mode = 0;
  Motor *channel[4];
  Motors(KangarooSerial & K, char name);
  void setSpeedLimit(int newSpeed);
  void drive(long drive, long turn);
  void shutDown();
  //void setTurn(long turn);
  void tankDrive(long leftSpeed, long rightSpeed);
  void setAngle(long angle);
  void moveStraight(boolean signal);
  void rotate(boolean signal);
  void moveSlant(boolean signal1, boolean signal2);
  void moveTo(double x1, double y1, double x2, double y2);
  void stop();
  void clearAngle();
  void loop();
  void begin();
  void setPos(long pos);
  //Define Variables we'll be connecting to
  double Setpoint, Input, Output;
  char currentSpeeds[5];
  void getStatus(KangarooError *output, int startIndex);

  //Specify the links and initial tuning parameters
  double Kp = 0, Ki = 0, Kd = 0;
  PID* syncPID;
};


class Auger {
public:
  Auger(int enablePin, int reversePin);
  int enablePin;
  int reversePin;
  void changeControlPins(int enablePin, int reversePin);
  void attach(int enablePin, int reversePin);
  void release();
  void forward();
  void reverse();
  void setDirection(int enable, int direction);
  void stop();
  char currentPos;
};

class Slider : public Motor {
public:
  Slider(KangarooSerial& K, char name);
  void setSpeed(int8_t speed);
};

class Conveyor {
public:
  int8_t pin;
  bool state;
  Conveyor(const int8_t pin)
    { pinMode(pin, OUTPUT); }
  void set(const bool on)
    { state = on; }
  void stop()
    { this->set(false); }
  void loop()
    { digitalWrite(pin, state); }
};


/*!
\class RMCKangaroo1
\brief This the main class for Kangaroo X2 Motion Controller
*/
class RMCKangaroo
{    
public:
  int channelIndex[DEFAULT_NUMBER_OF_CHANNEL];
  Motors* channel[DEFAULT_NUMBER_OF_CHANNEL];
  USARTClass* SerialPort;
  KangarooSerial* K;
  String channelList;
  String channelType;
  Motors* motors;
  LinearActuatorPair* linearActuatorPair;
  Auger* auger;
  Slider* slider;
  Conveyor* conveyor;
  RMCKangaroo(USARTClass &serialPorta);
  void loop();
  void begin();
  void getStatus(KangarooError *errorStatuses);
  void stop();
  KangarooStatus status[DEFAULT_NUMBER_OF_CHANNEL];
};
