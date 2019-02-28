import xbox;
import comms;
import time;
import signal;
import sys;
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!');
    comms.send([1, 10, 0, 0]);
    sys.exit(0);

signal.signal(signal.SIGINT, signal_handler);
#signal.pause();


# get the joystick speed from the xbox controller
def get_speed_turn(joy):
    x, y = joy.leftStick();
    print("x:%s, y:%s" % (x,y));
    speed = y * 100;
    turn = x * 100;
    return (speed, turn);

# send command to the robot
def send_drive_cmd(speed, turn):
    V = (100 - abs(turn)) * (speed / 100) + speed;
    W = (100 - abs(speed)) * (turn / 100) + turn;
    
    comms.send([1, 11, (V+W)/2, (V-W)/2]);

# xbox controller
joy = xbox.Joystick();


# main loop
while True:
    speed, turn = get_speed_turn(joy);
    send_drive_cmd(speed, turn);
    time.sleep(1 / 8); # 8fps