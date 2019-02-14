#This module details the algorithm by which the robot will traverse the arena with no environmental
#	information, collected data as it adjusts its path to safely make its way across the arena into
# 	the mining zone of the arena. We will use separate modules for the implementation of obstacle 
# 	detection, location, and grouping.

from hokuyolx import HokuyoLX	#library for interfacing with the Hokuyo LIDAR sensor
from Detect import detectRocks	#module for detecting obstacles
from Locate import locateRocks	#module for locating obstacle coords
from Grouping import groupRocks	#module for grouping coordinates into macro obstacles
import numpy as np

TARGET_STRIPE_WIDTH = 0			#the width of each stripe on the target
STRIPE_INTENS_THRESHOLD = 0		#the diffrence in intensity to signify a stripe change
CHOICE_TO_LOCATE_THRESHOLD = 0	#the threshold for deciding if enough points were detected to run location

def firstRun():
	#Algorithm conducting the first traversal across the arena from a designated starting
	#	point. Will crawl forward, looking for obstacles in its path, adjusting path as needed,
	# 	and recording data - slice by slice - relevant to locating obstacles and storing their
	# 	data for the pathfinding phase that will follow this algorithm

	backLIDAR = HokuyoLX()		#hook up to specifically front LIDAR
	frontLIDAR = HokuyoLX()		#hook up to specifically back LIDAR
	
	#FIXME Dev Note --- think about when to start the front lidar, not 
	# 	before we know where we are or else we start reading a wall 
	# 	and find a really, really big rock
	
	rockCoords = [] 		#FIXME --- Make this a numpy array --- FIXME

	initTimestampB, initBackData = backLIDAR.get_filtered_intens()

	backLidarCoord, robotOrientation = locateRobot(initBackData)		
	
	while not inMiningZone(backLidarCoord, robotOrientation):
		timestampF, frontData = frontLIDAR.get_filtered_dist()
		timestampB, backData = backLIDAR.get_filtered_intens()
		backLidarCoord, robotOrientation = locateRobot(backData)
		irregularities = detectRocks(frontData)
		if len(irregularities) > CHOICE_TO_LOCATE_THRESHOLD:
			rockCoords = locateRocks(irregularities)
	
	obstacles = groupRocks(rockCoords)

	#now we can switch to an automation driving algorithm, so call 
	# 	that function here
	
	
def inMiningZone(backLidarCoord, robotOrientation):
	#This function references with the origin target to see if the 
	# 	robot is in the mining zone or not,
	#	used in stopping a scan of the arena and grouping found 
	# 	data to begin the pathfinding phase
	
	position = True

	# some code

	return position

def locateRobot(backLidarData):
	#This function will use arguments consisting of the numpy array of points
	#   from the back LIDAR to find the points where reflectivity varies the
	#   most. Using these points, angles and distances will be used to locate the 
	#   coordinate of the BACK LIDAR SENSOR as well as the orientation of the 
	#   robot. Both values will be returned in a tuple

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

def locateFrontLidar(backLidar):
    pass