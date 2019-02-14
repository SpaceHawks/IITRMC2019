# This code will be purposed with grouping (x,y) coordinates
#	based on distance and angles that are found

import math
import numpy as np

GROUPING_THRESHOLD = 0
	
def point_dist(pointA, pointB):
	return (((pointA[0] - pointB[0]) ** 2) + ((pointA[1] - pointB[1]) ** 2))**(1/2)

def groupRocks(rockCoords):
	#Using all of the (x,y) coordinates generated from the locateRocks()
	# 	function, rocks will be assigned fewer data points to store and 
	# 	use less data while pathfinding using the 
	# 	location of rocks (coord of center and radius)
	
	dummyValue = [[[0,0],0],[[1,1],1]]

	return np.array(dummyValue)