from pathfinding import Pathfinding

pf = Pathfinding(0, 200)    #starting coordinate of robot
pf.obstacle = [[300.0, 200.0, 15.0],
                [75.0, 150.0, 15.0]] # coordinate of next 2 obstacles, can be 0
pf.pathFinder(0)        #arugment = number of obstacle
