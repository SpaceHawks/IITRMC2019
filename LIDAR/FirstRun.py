#This module details the algorithm by which the robot will traverse the arena with no environmental
#	information, collected data as it adjusts its path to safely make its way across the arena into
# 	the mining zone of the arena. We will use separate modules for the implementation of obstacle 
# 	detection, location, and grouping.

from hokuyolx import HokuyoLX					
from Detect import detectRocks					
from Locate import locateRocks, locateRobot, inMiningZone		
from Grouping import groupRocks					
import numpy as np

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
	
	
