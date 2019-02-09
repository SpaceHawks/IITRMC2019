import xbox;
import comms;
import time;

# get the joystick speed from the xbox controller
def get_speed_turn(joy):
    x, y = joy.leftStick();
    print("x:%s, y:%s" % (x,y));
    speed = y * 100;
    turn = x * 100;
    return (speed, turn);

# send command to the robot
def send_drive_cmd(speed, turn):
    comms.send([1, 10, speed, turn]);

# xbox controller
joy = xbox.Joystick();


# main loop
while True:
    speed, turn = get_speed_turn(joy);
    send_drive_cmd(speed, turn);
    time.sleep(1 / 8); # 8fps
