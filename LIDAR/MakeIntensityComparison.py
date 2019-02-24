#This module is used for the comparing of two test CSV files, grouped by
#   their angles and compared by intensities

def generateIntensityComparison():
    firstFile, secondFile = "", ""
    firstList, secondList = [], []
    
    firstFile = input("Enter first file name with extension: ")
    secondFile = input("Enter second file name with extension: ")

    with open(firstFile, 'r') as in1:
        for line in in1:
            elements = line.split(",")
            firstList.append([float(elements[0]), float(elements[2])])
            in1.close() 

    with open(secondFile, 'r') as in2:
        for line in in2:
            elements = line.split(",")
            secondList.append(float(elements[2]))
            in2.close()

    newFile = input("Enter a new file name: ")
    newFileLines = []

    if(len(firstList)>len(secondList)):
        with open(newFile, 'w') as out:
            for i in range(len(firstList)):
                newFileLines.append(str(firstList[i][0] + "," + firstList[i][1] + "," + secondList[i]))
            out.writelines(newFileLines)
            out.close()