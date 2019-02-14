from hokuyolx import HokuyoLX
import Detect
import Locate
import Grouping

#This is a template for the completed work of the LIDAR team on 
# 	mapping out the arena's obstacles

TARGET_STRIPE_WIDTH = 0
STRIPE_INTENS_THRESHOLD = 0
DETECTION_THRESHOLD = 0
CHOICE_TO_LOCATE_THRESHOLD = 0
GROUPING_THRESHOLD = 0


def firstRun():
	#This code should run simultaneous with the initial movement of 
	# 	the robot. This is the first phase of the 
	# 	robot's traversal of the arena. While moving forward 
	# 	nonspecifically, this code is designed to repeatedly 
	# 	scan the arena for irregular points in each slice (points 
	# 	that could be rocks), locate, and save these 
	# 	points all while directing the robot onto a safe path 
	# 	until the mining zone is reached. After the mining 
	# 	zone is reached, this algorithm should provide all data 
	# 	needed for the robot to decide it's own safe path 
	# 	back and forth safely in the arena

	backLIDAR = HokuyoLX()		#hook up to specifically front LIDAR
	frontLIDAR = HokuyoLX()		#hook up to specifically back LIDAR
	
	#IMPORTANT --- think about when to start the front lidar, not 
	# 	before we know where we are or else we start reading a wall 
	# 	and find a really, really big rock
	
	rockCoords = [] 		#FIXME --- Make this a numpy array --- FIXME

	backLidarCoord, robotOrientation = locateRobot(backData)		#find location and orientation for inMiningZone()
	
	while not inMiningZone(backLidarCoord):
		timestampF, frontData = frontLIDAR.get_filtered_dist()
		timestampB, backData = backLIDAR.get_filtered_intens()
		backLidarCoord, robotOrientation = locateRobot(backData)
		irregularities = detectRocks(frontLidar)
		if len(irregularities) > CHOICE_TO_LOCATE_THRESHOLD:
			rockCoords = locateRocks(rockCoords)
	
	rockZones = groupRocks(rockCoords)

	#now we can switch to an automation driving algorithm, so call 
	# 	that function here
	
	
def inMiningZone(backLidarCoord):
	#This function references with the origin target to see if the 
	# 	robot is in the mining zone or not,
	#	used in stopping a scan of the arena and grouping found 
	# 	data to begin the pathfinding phase
	
	position = True

	# some code

	return position

'''	
def detectRocks(frontLIDAR):
	#Using a threshold TBD, this function will save the angles 
	# 	and distances from the first LIDAR 
	#	that are tagged as irregular in shape (items that are 
	# 	rocks compared to reasonable bumps in
	# 	gravel)

	

#This function will use arguments consisting of the numpy array of points
#   from the back LIDAR to find the points where reflectivity varies the
#   most. Using these points, angles and distances will be used to locate the 
#   coordinate of the BACK LIDAR SENSOR as well as the orientation of the 
#   robot. Both values will be returned in a tuple
def locateRobot(backLidarData):
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

def locateRocks(rockCoords):
	#Using the distances and angles marked as irregular in detectRocks(),
	# 	 this function will give an (x,y) coordinate to the rocks by
	# 	 referencing with the origin target
	pass
	
def groupRocks(rockCoords):
	#Using all of the (x,y) coordinates generated from the locateRocks()
	# 	function, rocks will be assigned fewer data points to store and 
	# 	use less data while pathfinding using the 
	# 	location of rocks (coord of center and radius)
	
	dummyValue = [[[0,0],0][[1,1],1]]

	return array(dummyValue)
'''