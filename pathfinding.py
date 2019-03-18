#Move 3 steps aheah (40cm each)
import matplotlib.pyplot as plt
import math

class Pathfinding:
    
    isForward = True
    r = 50.0 # radius of robot
    rX = 100.0 # x-coordinate of robot
    rY = 450.0 # y-coordinate of robot

    obstacles = [[0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],] # holds upto 5 obstacles

    numPivots = 0 # num of relevant obstacles
    pivots = [[400.0, 320.0, 15.0],
              [180.0, 200.0, 15.0]] # works with only 2 obstacles at any time

    dir = 1     #where the robot face
    dest = 1    #direction of destination (bin/mining)

    xA = 0.0
    yA = 0.0
    xB = 0.0
    yB = 0.0
    x1 = 0.0
    y1 = 0.0
    x2 = 0.0
    y2 = 0.0
    x3 = 0.0
    y3 = 0.0

    def moveTo(x,y): # move robot to given (x,y) coordinates
        pass # need to implement using motor class

    def moveStraight(): # moves robot forward/backward 10 cm
        if (isForward == True):
            dest = 1
        else:
            dest = -1
        moveTo(rX+dest*10,rY)

    def pathA(num): # if numPivots == 1
        global xA
        global yA
        global x1
        global y1
        global x2
        global y2
        global x3
        global y3
        if(isForward == True):
            dest = 1
        else:
            dest = -1
        if(num == 1):
            xA = pivots[0][0]
            yA= pivots[0][1]
            if(yA > 0.0):
                dir = -1
            else:
                dir = 1
        if(num == 2):
            if((pivots[0][1]+pivots[1][1])/2 > 0):
                dir = -1
            else:
                dir = 1
            if(dir == 1):
                if(pivots[0][1] > pivots[1][1]):
                    xA = pivots[0][0]
                    yA= pivots[0][1]
                    xB = pivots[1][0]
                    yB= pivots[1][1]
                else:
                    xA = pivots[1][0]
                    yA= pivots[1][1]
                    xB = pivots[0][0]
                    yB= pivots[0][1]
            else:
                if(pivots[0][1] > pivots[1][1]):
                    xA = pivots[1][0]
                    yA= pivots[1][1]
                    xB = pivots[0][0]
                    yB= pivots[0][1]
                else:
                    xA = pivots[0][0]
                    yA= pivots[0][1]
                    xB = pivots[1][0]
                    yB= pivots[1][1]
        x3 = xA
        y3 = yA + dir*(r+40)
        x2 = xA - dest*(r+40)*2/3
        y2 = y3
        x1 = xA - dest * (r + 40)
        y1 = y3 - dir*(r+ 40)/3
        if(dest*x1 > dest*rX):
            moveTo(x1,y1)
        if (dest * x2 > dest * rX):
            moveTo(x2, y2)
        if (dest * x3 > dest * rX):
            moveTo(x3, y3)

    def pathB(): # if numPivots == 2
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
        xA = pivots[0][0]
        yA = pivots[0][1]
        xB = pivots[1][0]
        yB = pivots[1][1]
        width = math.sqrt(math.pow(xB-xA,2)+math.pow(yB-yA,2)) - pivots[0][2] - pivots[1][2]
        x1 = (xA + xB) / 2
        y1 = (yA + yB) / 2
        if (isForward == True):
            dest = 1
        else:
            dest = -1
        if(width > 2*r):
            if(math.fabs(yA-yB) < 2*r):
                if(dest*(xA-xB) < 0.0):
                    xA = pivots[1][0]
                    yA = pivots[1][1]
                    xB = pivots[0][0]
                    yB = pivots[0][1]
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
                y3 = yA + dir*(r+40)
            else:
                x2 = x1
                y2 = y1
                x1 = x2 - dest*20
                y3 = y2
                x3 = x2 + dest*20
            if(dest*x1 > dest*rX):
                moveTo(x1,y1)
            if (dest * x2 > dest * rX):
                moveTo(x2, y2)
            if (dest * x3 > dest * rX):
                moveTo(x3, y3)
        else:
            pathA(2) # treat the two obstacles as a single big one

    def draw(rX,rY,xA,yA,xB,yB,x1,y1,x2,y2,x3,y3): # plot to test cases
        plt.plot([rX, x1, x2, x3], [rY, y1,y2,y3])
        plt.plot([xA-10.6, xA-10.6, xA+10.6, xA+10.6, xA-10.6 ], [yA-10.6, yA+10.6, yA+10.6, yA-10.6, yA-10.6])
        plt.plot([xB-10.6, xB-10.6, xB+10.6, xB+10.6, xB-10.6 ], [yB-10.6, yB+10.6, yB+10.6, yB-10.6, yB-10.6])
        plt.plot([rX-40, rX-40, rX+40, rX+40, rX-40 ], [rY-40, rY+40, rY+40, rY-40, rY-40])
        plt.plot([x1-40, x1-40, x1+40, x1+40, x1-40 ], [y1-40, y1+40, y1+40, y1-40, y1-40])
        plt.plot([x2-40, x2-40, x2+40, x2+40, x2-40 ], [y2-40, y2+40, y2+40, y2-40, y2-40])
        plt.plot([x3-40, x3-40, x3+40, x3+40, x3-40 ], [y3-40, y3+40, y3+40, y3-40, y3-40])
        plt.show()

    def pathFinder(): # Returns path of 3 points to move to
        if(numPivots == 0):
            moveStraight()
        if(numPivots == 1):
            pathA(1)
        if(numPivots == 2):
            pathB()
        else:# eliminate unnecessary pivots
           pass # need to implement
        draw(rX,rY,pivots[0][0],pivots[0][1],pivots[1][0],pivots[1][1],x1,y1,x2,y2,x3,y3)

def main():
    global numPivots
    numPivots = 1
    pathFinder()


if __name__ == "__main__":
    main()
