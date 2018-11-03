bool stopAll = false;

#include "RMCKangaroo.hpp"
RMCKangaroo k(Serial2);


/*

  [
    Command: uint8_t
    Device: uint8_t
    Val1: int8_t
    Val2: int8_t
    Checksum: uint8_t
  ]

*/

void setup() {
  Serial.begin(9600);
  k.begin();
  k.motors->drive(10, 100);
}


void loop() {
    acceptCommands();

}


// if valid comand returns zero
// if not, redurns whats needed to make it a valid command
bool checkSum(const char msg[], const uint8_t len) {

    // total parts
    char sum = 0;
    for (uint8_t i = 0; i < len; i++)
        sum += msg[i];

    // if not zero its not valid
    if (sum != 0) {
        Serial.print("invalid msg totaled to ");
        Serial.println(sum);
    }

    return sum;
}



// send data to computer
void sendData(char* data, const unsigned size) {
    data[size] = checkSum(data, size); // last gets replaced
    Serial.write(data, size + 1);
}

// send a single data pair
void sendValues(const char device, const char index, const char value) {
    char data[] = { 3, device, index, value, 0 }; // last value gets replaced
    sendData(data, 4);
}

// send mulitple values in a series
void sendMulti(const char device, const char v1, const char v2) {
    char data[] = { 0, device, v1, v2, 0 }; // last gets replaced
    sendData(data, 4);
}




void acceptCommands() {
    while (Serial1.available() > 4) {

        // read msg from serial
        // should have 5 vals: cmd, device, v1, v2, checksum
        char msg[5];
        Serial.readBytes(msg, 5);

        // checksum should make msg total to zero otherwise its invalid
        bool valid = checkSum(msg, 5);
        while (!valid && Serial1.available()) {

            // last checksum invalid so lets get a new char to see
            for (uint8_t i = 4; i > 0; i--)
                msg[i] = msg[i - 1];
            msg[0] = Serial1.read();
            valid = checkSum(msg, 5);
        }

        if (!valid) {
            Serial.println("com failed");
            k.motors->drive(0, 0);
            return;
        }

        char cmd = msg[0], device = msg[1],
             arg1 = msg[2], arg2 = msg[3];

        switch(cmd) {
            case 0: cmdConfig(device, arg1, arg2);  break;
            case 1: cmdDrive(device, arg1, arg2);   break;
            case 2: cmdAuto(device, arg1, arg2);    break;
            case 3: cmdSensorData(device, arg1, arg2); break;
            default:
                Serial.println("invalid command received (passed checksum)");
                break;
        }
    }
}


// cmd0: system configurations (non-driving operations)
void cmdConfig(char device, char v1, char v2) {

    switch (device) {
    case 0: // tcp connection status --> e-stop (1=pressed 0=released)
        /*
        arg1:
            0: sender connecteds
            1: sender disconnected
            2: redeiver connected
            3: receiger disconnected
        arg2: ip address of remote device
        */
        break;
    case 1: // Kangaroo error status


        break;
    case 2: // set remaining time in competition
        break;
    case 3: // motor arduino system operation
        break;
    case 4: // sensor arduino system operation
        break;
    case 5: // ctlr connected?
        break;
    case 6: // set autonomous mode
        break;
    case 10: // set speed limit for wheels
        break;
    case 11: // reset arduino
        break;
    case 12: // setup
        break;
    case 13: // start
        break;
    default:
        Serial.println("command 0: invalid device");
        break;
    }
}

// cmd 1
void cmdDrive(char device, char v1, char v2) {
    switch (device) {
    case 0: // stop all
        k.motors->drive(0, 0);
        stopAll = true;
        break;
    case 1: case 2: case 3: case 4: // control specific wheel
        k.motors->channel[device - 1]->setTargetSpeed((signed char) v1);
        break;

    case 5: case 6: // linear actuator (pos, speed)
        k.linearActuatorPair->setTargetPosAndSpeed(v1, v2);
        break;

    case 7: // auger slider
        k.slider->setTargetPosAndSpeed(v1, v2);
        break;

    case 8: // auger drill motor
        k.auger->setDirection(v1, v2);
        break;

    case 9: // dumping conveyor
        k.conveyor->setTargetSpeed(v1); // was v2, changed to v1 bc it makes more sense
        break;

    case 10: // drive magnitude + direction
        k.motors->drive((signed char) v1, (signed char) v2);
        break;

    case 11: // tank drive (L, R)
        k.motors->tankDrive((signed char) v1, (signed char) v2);
        break;

    case 12: // shut down
        k.motors->shutDown();
        break;
    case 13: // e-stop
        k.motors->shutDown();
        stopAll = true;
        break;

    case 15: // stop tilter
        break;

    case 17: // stop slider
        if (v1 == 1) {
            k.slider->home().wait();
        } else if (v2 == 0) {
            k.slider->setSpeed(100);
            k.slider->home(); //.wait();// was: setTargetPosDirect(SLIDER_INITIAL_POS);
        }
        break;

    default:
        Serial.println("Cmd 1: invalid device");
        break;
    }
}

// cmd2: autonomous operations
// should be controlled by tinkerboard/pi so that robot can
// utilize sensors data
void cmdAuto(char device, char v1, char v2) {
    switch (device) {
        case 0: // stop auto
            break;
        case 1:
            // automatically dig and dump onto robot's bin once
            break;
        case 2:
            // automatic dump on robot's bin once
            break;
        case 3:
            // navigating to arena's bin
            break;
        case 4:
            // navigating to mining area
            break;
        case 5:
            // dump everything into arean's bin
            break;
        case 6:
            // dump everything into arena's bin
            break;
        default:
            Serial.println("cmd2: invalid operation");
    }
}

// cmd3
void cmdSensorData(char device, char v1, char v2) {
    switch (device) {
        case 0: // stopall
            stopAll = true; // might be too strong :/
            break;
        case 1: // get speed of wheel1
            sendValues(device, (signed char) k.motors->channel[0]->getCurrentSpeed(), 0);
            break;
        case 2: // get speed of wheel2
            sendValues(device, (signed char) k.motors->channel[1]->getCurrentSpeed(), 0);
            break;
        case 3: // get speed of wheel3
            sendValues(device, (signed char) k.motors->channel[2]->getCurrentSpeed(), 0);
            break;
        case 4: // get speed of wheel4
            sendValues(device, (signed char) k.motors->channel[3]->getCurrentSpeed(), 0);
            break;
        case 5: case 6: { // linear actuator pair (pos, speed)
            const char leftPos = (char) k.linearActuatorPair->channel[0]->getCurrentVal();
            const char rightPos = (char) k.linearActuatorPair->channel[1]->getCurrentVal();
            sendValues(device, leftPos, rightPos);
            break;
        }
        case 7: // auger slider
            break;
        case 8: // drill motor
            break;
        case 9: // dumping conveyor
            break;
        case 10: { // get Speed (4 wheels)
            const char* speeds = k.motors->currentSpeeds;
            sendValues(device, -speeds[FRONT_LEFT], -speeds[FRONT_RIGHT]); // device 10
            sendValues(device + 10, -speeds[REAR_LEFT], -speeds[REAR_LEFT]); // device 20
            break;
        }
        case 11: // tank drive (we don't need this)
            // then why is it here?
            break;
        default:
            Serial.println("Cmd 3: invalid device");
    }
}
