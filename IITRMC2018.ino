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
	
					
motorK.motors->setSpeedLimit(value1);
					
				switch (device)
				{
				case 0:
					//Emergency Stop. Should stop all motors
					motorK.motors->drive(0, 0);
				
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
			
			
		else {// com failed, stop all actuators
			motorK.motors->drive(0, 0); //should be all motors
		}
	}
}
