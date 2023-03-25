import re

# IF HAVE EXTRA TIME, MAKE MAIN FUNCTION READ COMMANDLINE ARGUMENT FOR THE INPUT FILE NAME & FEED IT to format_input function (either read commandline arg or if none given, use "input.txt")

# convert into nested dictionary
# ex: {"A": {"Treasures": ["Gold"], "Next": ["Start", "B", "D"]}, "B": {"Treasures": ["Ruby"], "Next": ["A", "D", "E"]}}

# function to clean input
def format_input(fileName):
    file = open(fileName, "r")
    inputText = file.read()
    
    inputLines = inputText.split("\n")
    
    mazeGeneralInfo = inputLines[0:3]
    mazeEncodingInfo = inputLines[3:]

    mazeGeneralInfo = [line.strip() for line in mazeGeneralInfo]
    nodesList = mazeGeneralInfo[0].split()
    treasuresList = mazeGeneralInfo[1].split()
    maxStepsAllowed = int(mazeGeneralInfo[2])

    mazeEncodingInfo = [line.strip() for line in mazeEncodingInfo]
    formattedMazeEncodingInfo = []
    for nodeInfo in mazeEncodingInfo:
        nodeInfo = nodeInfo.split("TREASURES")
        nodeInfo = [line.strip() for line in nodeInfo]
        nodeInfo[1] = nodeInfo[1].split("NEXT")
        nodeInfo[1] = [line.strip() for line in nodeInfo[1]]
        nodeInfo[1][0] = nodeInfo[1][0].split()
        nodeInfo[1][1] = nodeInfo[1][1].split()
        formattedMazeEncodingInfo.append(nodeInfo)

    mazeEncodingInfoDict = {}
    for nodeInfo in formattedMazeEncodingInfo:
        node, treasuresAndNext = nodeInfo[0], nodeInfo[1]
        treasures = treasuresAndNext[0]
        next = treasuresAndNext[1]
        mazeEncodingInfoDict[node] = {"Treasures": treasures, "Next": next}
    
    return [nodesList, treasuresList, maxStepsAllowed, mazeEncodingInfoDict]


def frontend_main():
    formattedInput = format_input("input.txt")
    nodesList = formattedInput[0]
    treasuresList = formattedInput[1]
    maxStepsAllowed = formattedInput[2]
    mazeEncodingInfoDict = formattedInput[3]

    print("nodesList:", nodesList)
    print("treasuresList:", treasuresList)
    print("maxStepsAllowed:", maxStepsAllowed)
    print("mazeEncodingInfoDict:", mazeEncodingInfoDict)

    propAtomMapping = {}
    propAtomNumber = 1
    for time in range(maxStepsAllowed + 1):
        for node in nodesList:
            nodePropAtom = "At(%s,%s)" % (node, time)
            print("propAtom:", nodePropAtom)
            propAtomMapping[nodePropAtom] = propAtomNumber
            propAtomNumber += 1
        for treasure in treasuresList:
            treasurePropAtom = "Has(%s,%s)" % (treasure, time)
            print("propAtom:", treasurePropAtom)
            propAtomMapping[treasurePropAtom] = propAtomNumber
            propAtomNumber += 1
    print("propAtomMapping:", propAtomMapping)

    # create & open new file to serve as input for dpll program
    f = open("dpll_input.txt", "w")

    # category 1
    f.write("CATEGORYYYYYYY 1")
    for time in range(maxStepsAllowed + 1):
        for nodeIndex in range(len(nodesList)):
            if nodeIndex < len(nodesList) - 1:
                for secondNodeIndex in range(nodeIndex + 1, len(nodesList)):
                    firstPropAtom = "At(%s,%s)" %(nodesList[nodeIndex], time)
                    secondPropAtom = "At(%s,%s)" %(nodesList[secondNodeIndex], time)
                    f.write("%s %s\n" % (-1*propAtomMapping[firstPropAtom], -1*propAtomMapping[secondPropAtom]))
    
    # category 2
    f.write("CATEGORYYYYYYY 2\n")
    # do i have to account for the fact that t should be < maxStepsAllowed so that t + 1 <= maxStepsAllowed??
    for node in nodesList:
        for time in range(maxStepsAllowed):
            currentNodePropAtom = "At(%s,%s)" % (node, time)
            f.write("%s" % (-1*propAtomMapping[currentNodePropAtom]))

            for neighborNode in mazeEncodingInfoDict[node]["Next"]:
                neighborPropAtom = "At(%s,%s)" % (neighborNode, time + 1)
                f.write(" %s" % propAtomMapping[neighborPropAtom])
                #f.write(" %s" % neighborPropAtom)
            f.write("\n")


    # category 3


    # category 4


    # category 5


    # category 6
    f.write("CATEGORYYYYYYY 6")
    propAtom = "At(START,0)"
    f.write(str(propAtomMapping[propAtom]))

    # category 7


    # category 8
    
    f.close()

frontend_main()