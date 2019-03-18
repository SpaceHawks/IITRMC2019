from pathfinding import Pathfinding

pf = Pathfinding(0, 200)
pf.obstacle = [[300.0, 200.0, 15.0],
                [200.0, 50.0, 15.0]] # works with only 2 obstacles at any time
pf.pathFinder(2)
