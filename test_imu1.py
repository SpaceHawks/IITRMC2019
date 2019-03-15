import imu

imu.InitMPU()
for i in range(2000):
    #imu.accel()
    imu.gyro()
