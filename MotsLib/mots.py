
import comms;

# instruction set defined here: https://docs.google.com/document/d/1cUTG8RFGPtx6UG5p6J76NQImksJC-LNIKzTHBX8p66E/edit?usp=sharing

# robot is 4wd
class Drivetrain():
    def __init__(self):
        pass;

    # wheel num goes from 0-3
    # 1 0
    # 3 2
    @staticmethod
    def driveWheel(wheelNum, speed):
        comms.send([1, 1 + wheelNum, speed, speed]);

    # both range from negative to positive 100%
    @staticmethod
    def drive(speed, turn): # Arduino code for command apparently doesn't work
        comms.send([1, 10, speed, turn]);

    # left and right are on range of +/- 100%
    @staticmethod
    def tank_drive(left, right):
        comms.send([1, 11, left, right]);

    ### this should be async!! (lag = bad)
    # wheel num goes from 0-3
    # 1 0
    # 3 2
    @staticmethod
    def get_mot_speed(wheelNum):
        comms.send([3, 1 + wheelNum, 0, 0]);
        return comms.receive();

    @staticmethod
    def get_speed():
        comms.send([3, 10, 0, 0]);


# mining subsystem, auger, linear actuators, conveyor, etc.
class Auger():
    @staticmethod
    def set_actuator(pos, speed):
        comms.send([1, 5, pos, speed]);

    @staticmethod
    def set_slider(pos, speed):
        comms.send([1, 7, pos, speed]);

    @staticmethod
    def set_conveyor(speed):
        comms.send([1, 9, speed, speed]);

    # accepts 3 states
    # 0 : off, 1 : forwards, -1 : backwards
    @staticmethod
    def set_drill(state, direction=None):
        if direction:
            comms.send([1, 8, state, direction]);
        else:
            comms.send([1, 8, 1 if state else 0, state < 0]);

# global controls for the system

# power-cycle the Arduino
def reset_arduino():
    comms.send([0, 11, 0, 0]);

# stop all actuators
def stop_all():
    comms.send([1, 0, 0, 0]);

# emergency stop
def estop():
    comms.send([1, 13, 0, 0]);
