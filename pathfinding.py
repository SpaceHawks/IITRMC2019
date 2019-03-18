#Move 3 steps aheah (40cm each)
import matplotlib.pyplot as plt
import math

class Pathfinding:
    def __init__(self, rx ,ry):
        print("init")

        self.isForward = True
        self.r = 50.0 # radius of robot
        self.rX = rx # x-coordinate of robot
        self.rY = ry # y-coordinate of robot

        self.numObstacle = 0 # num of relevant obstacles
        self.obstacle = [[0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0]] # works with only 2 obstacles at any time

        dir = 1     #Direction faced by the robot
        dest = 1    #Direction of destination (-1 = bin, 1 = mining area)

        xA = yA = 0.0
        xB = 0.0
        yB = 0.0
        x1 = 0.0
        y1 = 0.0
        x2 = 0.0
        y2 = 0.0
        x3 = 0.0
        y3 = 0.0

    def pathFinder(self, numObs): # Returns path of 3 points to move to
        print("start")
        numObstacle = numObs
        if(numObstacle == 0):
            moveStraight()
        if(numObstacle == 1):
            self.pathA(1)
        if(numObstacle == 2):
            self.pathB()
        else:# eliminate unnecessary obstacle
           pass # need to implement
        self.draw(self.rX, self.rY, self.obstacle[0][0], self.obstacle[0][1], self.obstacle[1][0], self.obstacle[1][1],x1,y1,x2,y2,x3,y3)

    def moveTo(self, x, y): # move robot to given (x,y) coordinates
        pass # need to implement using motor class

    def moveStraight(self): # moves robot forward/backward 10 cm
        if (isForward == True):
            dest = 1
        else:
            dest = -1
        moveTo(rX+dest*10,rY)

    def pathA(self, num): # if numObstacle == 1
        global xA
        global yA
        global x1
        global y1
        global x2
        global y2
        global x3
        global y3
        if(self.isForward == True):
            dest = 1
        else:
            dest = -1
        if(num == 1):
            xA = self.obstacle[0][0]
            yA = self.obstacle[0][1]
            if(yA > 0.0):
                dir = -1
            else:
                dir = 1
        if(num == 2):
            if((self.obstacle[0][1]+self.obstacle[1][1])/2 > 0):
                dir = -1
            else:
                dir = 1
            if(dir == 1):
                if(self.obstacle[0][1] > self.obstacle[1][1]):
                    xA = self.obstacle[0][0]
                    yA = self.obstacle[0][1]
                    xB = self.obstacle[1][0]
                    yB = self.obstacle[1][1]
                else:
                    xA = self.obstacle[1][0]
                    yA = self.obstacle[1][1]
                    xB = self.obstacle[0][0]
                    yB = self.obstacle[0][1]
            else:
                if(self.obstacle[0][1] > self.obstacle[1][1]):
                    xA = obstacle[1][0]
                    yA = obstacle[1][1]
                    xB = obstacle[0][0]
                    yB = obstacle[0][1]
                else:
                    xA = self.obstacle[0][0]
                    yA = self.obstacle[0][1]
                    xB = self.obstacle[1][0]
                    yB = self.obstacle[1][1]
        x3 = xA
        y3 = yA + dir*(self.r+40)
        x2 = xA - dest*(self.r+40)*2/3
        y2 = y3
        x1 = xA - dest * (self.r + 40)
        y1 = y3 - dir*(self.r+ 40)/3
        if(dest*x1 > dest*self.rX):
            self.moveTo(x1,y1)
        if (dest * x2 > dest * self.rX):
            self.moveTo(x2, y2)
        if (dest * x3 > dest * self.rX):
            self.moveTo(x3, y3)

    def pathB(self): # if numObstacle == 2
        global xA
        global yA
        global xB
        global yB
        global x1
        global y1
        global x2
        global y2
        global x3
        global y3
        xA = self.obstacle[0][0]
        yA = self.obstacle[0][1]
        xB = self.obstacle[1][0]
        yB = self.obstacle[1][1]
        width = math.sqrt(math.pow(xB-xA,2)+math.pow(yB-yA,2)) - self.obstacle[0][2] - self.obstacle[1][2]
        x1 = (xA + xB) / 2
        y1 = (yA + yB) / 2
        if (self.isForward == True):
            dest = 1
        else:
            dest = -1
        if(width > 2*self.r):
            if(math.fabs(yA-yB) < 2*self.r):
                if(dest*(xA-xB) < 0.0):
                    xA = self.obstacle[1][0]
                    yA = self.obstacle[1][1]
                    xB = self.obstacle[0][0]
                    yB = self.obstacle[0][1]
                if((yA-yB) > 0.0):
                    dir = -1
                else:
                    dir = 1
                x2 = x1
                y2 = y1
                if(dest == dir):
                    x1 = x2 - dest*30
                    y1 = y2 - dest*30
                else:
                    x1 = x2 + dir*30
                    y1 = y2 + dest*30
                x3 = xA
                y3 = yA + dir*(self.r+40)
            else:
                x2 = x1
                y2 = y1
                x1 = x2 - dest*20
                y3 = y2
                x3 = x2 + dest*20
            if(dest*x1 > dest*self.rX):
                self.moveTo(x1,y1)
            if (dest * x2 > dest * self.rX):
                self.moveTo(x2, y2)
            if (dest * x3 > dest * self.rX):
                self.moveTo(x3, y3)
        else:
            self.pathA(2) # treat the two obstacles as a single big one

    def draw(self, rX,rY,xA,yA,xB,yB,x1,y1,x2,y2,x3,y3): # plot to test cases
        plt.plot([rX, x1, x2, x3], [rY, y1,y2,y3])
        plt.plot([xA-10.6, xA-10.6, xA+10.6, xA+10.6, xA-10.6 ], [yA-10.6, yA+10.6, yA+10.6, yA-10.6, yA-10.6])
        plt.plot([xB-10.6, xB-10.6, xB+10.6, xB+10.6, xB-10.6 ], [yB-10.6, yB+10.6, yB+10.6, yB-10.6, yB-10.6])
        plt.plot([rX-40, rX-40, rX+40, rX+40, rX-40 ], [rY-40, rY+40, rY+40, rY-40, rY-40])
        plt.plot([x1-40, x1-40, x1+40, x1+40, x1-40 ], [y1-40, y1+40, y1+40, y1-40, y1-40])
        plt.plot([x2-40, x2-40, x2+40, x2+40, x2-40 ], [y2-40, y2+40, y2+40, y2-40, y2-40])
        plt.plot([x3-40, x3-40, x3+40, x3+40, x3-40 ], [y3-40, y3+40, y3+40, y3-40, y3-40])
        plt.show()
