import numpy as np

TARGET_STRIPE_WIDTH = 0
STRIPE_INTENS_THRESHOLD = 0

def locateRocks(irregularities):
	#Using the distances and angles marked as irregular in detectRocks(),
	# 	 this function will give an (x,y) coordinate to the rocks by
	# 	 referencing with the origin target
	return np.array([])

def locateRobot(backLidarData):
	#Using the distances, angles, and intensities from the back LIDAR 
	# 	detecting the target in order to give the robot a tuple of 
	#   (x,y) coordinate and radian orientation
	
	#find the target points
	targetPoints = [] 				#FIXME make this a numpy array
	lastCoord = None
	for coord in backLidarData:
		if lastCoord is None:
			lastCoord = coord
		else:
			if abs(coord[2] - lastCoord[2]) >  STRIPE_INTENS_THRESHOLD:
				#FIXME make this the average of the two angles and distances					
				targetPoints.append(coord)				
			lastCoord = coord

    #identify two useful points
	
    #do geometry
    
    #return (backLidarCoord, robotOrientation)

	return (0.0,0.0)

def inMiningZone(backLidarCoord, robotOrientation):
	#This function references with the origin target to see if the 
	# 	robot is in the mining zone or not,
	#	used in stopping a scan of the arena and grouping found 
	# 	data to begin the pathfinding phase
	
	position = True

	# some code

	return position

def locateFrontLidar(backLidar):
    pass