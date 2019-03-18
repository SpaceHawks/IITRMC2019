from pathfinding import Pathfinding

pf = Pathfinding(0, 200)
pf.obstacle = [[300.0, 200.0, 15.0],
                [75.0, 150.0, 15.0]] # works with only 2 obstacles at any time
pf.pathFinder(0)
a= 0.0

if(a==None):
    print("fuck u")
