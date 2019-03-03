#Program takes sample data from LIDAR and puts it in a .csv file 
# 	for angles, dists and intens

from hokuyolx import HokuyoLX
import numpy as np

lidar = HokuyoLX()

_, data = lidar.get_filtered_intens()

data=data.tolist()

fileName = input("Enter a file name: ")

with open(str(fileName) + ".csv", 'w') as pw:
	for i in range(len(data)):
		pw.write(str(data[i][0]) + "," + str(data[i][1]) + "," + str(data[i][2]))
		if i != len(data)-1:
			pw.write("\n")
	pw.close()
lidar.close()

#commment