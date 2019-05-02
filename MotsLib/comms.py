import serial;
import time;
ser = serial.Serial("/dev/ttyS1", 9600);

def send(data):
	# append checksum to end of data
	data.append((-sum(data)) % 256);

	# convert data to ints
	data = list(map(int, data));

	# verify all elems are one byte
	data = checkData(data);
	data = bytearray(data);
	ser.write(data);
	time.sleep(1 / 32);

# verify all elems are one byte
def checkData(data):
	for i in range(len(data)):
		data[i] = data[i] % 256;
	return data;


# returns recieved data, otherwise returns None
def receive():
    if serial.in_waiting < 5:
        return None;
    data = serial.read(5);
    return data;


import RPi.GPIO as GPIO;

# reset arduino
def reset_arduino():
	GPIO.setmode(GPIO.BCM);
	GPIO.setwarnings(False);
	GPIO.setup(18, GPIO.OUT);
	time.sleep(5);
	GPIO.output(18, GPIO.LOW);
	time.sleep(.2);
	GPIO.output(18, GPIO.HIGH);

reset_arduino();
