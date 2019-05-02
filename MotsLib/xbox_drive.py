import xbox;
import comms;
import time;
import signal;
import sys;
import mots;

comms.reset_arduino();

# make it so that when user ends manual control the robot is first told to stop moving
def signal_handler(sig, frame):
    print("Stopped program");
    comms.send([1, 10, 0, 0]);
    sys.exit(0);

signal.signal(signal.SIGINT, signal_handler);


# get the joystick speed from the xbox controller
def get_speed_turn(joy):
    x, y = joy.leftStick();
    print("x:%s, y:%s" % (x,y));
    speed = y * 100;
    turn = x * 100;
    return (speed, turn);

# send command to the robot
def send_drive_cmd(speed, turn):
	# convert speed + turn to l & r motor speeds
	v = (100 - abs(turn)) * (speed / 100) + speed;
	w = (100 - abs(speed)) * (turn / 100) + turn;
	l = (v + w) / 2;
	r = (v - w) / 2;
	# send tank drive command
	mots.tank_drive(l, r);

# read buttons from xbox-controller
def control_auger(joy):

    # TODO: prevent retriggering
    # toggle buttons to control the auger
    if not control_auger.t_d_status and joy.A():
        control_auger.d_status = not control_auger.d_status;
        control_auger.t_d_status = True;
    elif control_auger.t_d_status and not joy.A():
        control_auger.t_d_status = False;

    if not control_auger.t_d_dir and joy.A():
        control_auger.d_dir = not control_auger.d_dir;
        control_auger.t_d_dir = True;
    elif control_auger.t_d_dir and not joy.A():
        control_auger.t_d_dir = False;

    mots.Auger.set_drill(control_auger.d_status, control_auger.d_dir);

    if joy.X():
        mots.Auger.set_slider(100,100);
    elif joy.Y():
        mots.Auger.set_slider(100, 100);

    if joy.leftBumper():
        mots.Auger.set_actuator(0, 100);
    elif joy.rightBumper():
        mots.Auger.set_actuator(75, 100);
    else:
        mots.Auger.set_actuator(0, 0);

    mots.Auger.set_conveyor(100 * (joy.rightTrigger() - joy.leftTrigger()));

control_auger.d_status = False;
control_auger.d_dir = False;
control_auger.t_d_status = False;
control_auger.t_d_dir = False;

# xbox controller
joy = xbox.Joystick();


# main loop
while True:
    speed, turn = get_speed_turn(joy);
    send_drive_cmd(speed, turn);
    control_auger(joy);

    #time.sleep(1 / 8); # 8 fps
