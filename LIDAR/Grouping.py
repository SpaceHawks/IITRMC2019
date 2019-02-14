# This code will be purposed with grouping (x,y) coordinates
#	based on distance and angles that are found

import math
import numpy as np

KEEP_GROUPING_THRESHOLD = 0		#the number of stray points not grouped allowed to end grouping algorithm
DISTANCE_THRESHOLD = 0			#threshold of distance that decides whether or not two points are in the same group
MARK = 2						#index of rockCoords that holds the marker
	
def dist(pointA, pointB):
	return (((pointA[0] - pointB[0]) ** 2) + ((pointA[1] - pointB[1]) ** 2))**(1/2)

def groupRocks(rockCoords):
	# based on the rockCoords (x,y) for all points identified by location
	#	groupRocks will group them into groups represented by ordered pair
	# 	for a circle center and a scalar for radius, cutting down on data and
	# 	simplifying obstacle representation
	
	countedCoords = 0		#keeps tracked of how many coords have been grouped
	obstacles = []			#stores the groupings
	pivot = 0				#the point of focus to populate each group
	idx = 0					#tracks the index of the current group of focus
	i = 0					#counter to find the next pivot

	while(abs(len(rockCoords)-countedCoords) > KEEP_GROUPING_THRESHOLD):
		idx = len(obstacles)
		obstacles.append([])
		while(rockCoords[i][MARK] != 0):
			i += 1
		
		pivot = i

		for coord in rockCoords:
			if dist(coord, rockCoords[pivot]) < DISTANCE_THRESHOLD:
				coord[MARK] += 1
				countedCoords += 1
				obstacles[idx].append(coord)
	
	#dummyValue = [[[0,0],0],[[1,1],1]]
	#return np.array(dummyValue)
	
	return np.array(obstacles)