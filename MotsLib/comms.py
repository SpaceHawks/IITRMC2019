import serial

ser = serial.Serial("/dev/ttyS1", 9600);

def send(data):

	# append checksum to end of data
	data.append((-getSum(data)) % 256);

	# convert data to ints
	data = list(map(int, data));

	# verify all elems are one byte
	data = checkData(data);

	#
	data = bytearray(data)
	ser.write(data)

# value needed to make total to zero with overflow
def getSum(data):
	sum = 0;
	for i in data:
		sum += i;
	return sum;

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
