#include "RMCKangaroo.hpp"
RMCKangaroo motorK(Serial3);

void setup() {
	Serial1.begin(9600);
	Serial.begin(9600);
	motorK.begin();
	Serial.println("Motor control started!");

}

void loop() {
	motorK.loop();
	serialEvent();

}

void serialEvent() {
	while (Serial1.available() > 4) {
		char message[5];
		Serial1.readBytes(message, 5);
		bool valid = verifyCheckSum(message, 5);
		while (!valid && Serial1.available())
		{
			for (int i = 4; i > 0; i--)
			{
				message[i] = message[i - 1];
			}
			message[0] = Serial1.read();
			valid = verifyCheckSum(message, 5);
			Serial.println("hieu");
		}
		if (valid)
		{
			char command = message[0];
			char device = message[1];
			char value1 = message[2];
			char value2 = message[3];
			//Serial.println("Passed checksum: " + String(command) + " " + String(device) + " " + String(value1) + " " + String(value2));
			switch (command)
			{
			case 0:
				switch (device)
				{
				case 1:
					KangarooError errorStatuses[8];
					motorK.getStatus(errorStatuses);
					for (int i = 0; i < 8; i++)
					{
						sendSystem(1, i + 1, errorStatuses[i]);
					}
					break;
				case 10:
					motorK.motors->setSpeedLimit(value1);
					break;
				default:
					break;
				}
				break;
			case 1:
				switch (device)
				{
				case 0:
					//Emergency Stop. Should stop all motors
					motorK.motors->drive(0, 0);
					break;
				case 1:
					break;
				case 2:
					break;
				case 3:
					break;
				case 4:
					break;
				case 5://linear actuator pair
					motorK.linearActuatorPair->setTargetPosAndSpeed(value1, value2);
					break;
				case 6://linear actuator pair
					motorK.linearActuatorPair->setTargetPosAndSpeed(value1, value2);
					break;
				case 7:// auger on/off reverse/forward
					motorK.slider->setTargetPosAndSpeed(value1, value2);
					break;
				case 8:// auger on/off reverse/forward
					motorK.auger->setDirection(value1, value2);
					break;
				case 9:// auger on/off reverse/forward
					motorK.conveyor->setTargetSpeed(value2);
					break;
				case 10:
					motorK.motors->drive((signed char)value1, (signed char)value2);
					break;
				case 11:
					motorK.motors->tankDrive((signed char)value1, (signed char)value2);
					break;
				case 12:
					motorK.motors->shutDown();
					break;
				case 17: //new
					if (value1 == 0)
					{
						motorK.slider->setSpeed(100);
						motorK.slider->setTargetPosDirect(SLIDER_INITIAL_POS);
					}
					else if (value1 == 1)
					{
						motorK.slider->home().wait();
					}
					break;
				default:
					Serial.println("unhanddle command: " + String(command) + " " + String(device) + " " + String(value1) + " " + String(value2));
					break;
				}
				break;
			case 3:
				switch (device)
				{
				case 0:
					break;
				case 1:
					break;
				case 2:
					break;
				case 3:
					break;
				case 4:
					break;
				case 5:
				{
					char leftPos = (char)motorK.linearActuatorPair->channel[0]->getCurrentVal();
					char rightPos = (char)motorK.linearActuatorPair->channel[1]->getCurrentVal();
					sendData(5, leftPos, rightPos);
					break;
				}
				case 6:
				{
					char leftPos = (char)motorK.linearActuatorPair->channel[0]->getCurrentVal();
					char rightPos = (char)motorK.linearActuatorPair->channel[1]->getCurrentVal();
					sendData(6, leftPos, rightPos);
					break;
				}
				case 10:
				{
					char *speeds = motorK.motors->currentSpeeds;
					speeds[FRONT_LEFT] = -speeds[FRONT_LEFT];
					speeds[FRONT_RIGHT] = -speeds[FRONT_RIGHT];
					sendData(10, speeds[FRONT_LEFT], speeds[FRONT_RIGHT]);
					sendData(20, speeds[REAR_LEFT], speeds[REAR_RIGHT]);
					break;
				}
				default:
					break;
				}
				break;
			}
		}
		else {// com failed, stop all actuators
			motorK.motors->drive(0, 0); //should be all motors
		}
	}
}
