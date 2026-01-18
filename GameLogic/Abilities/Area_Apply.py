from Systems import PlayerSelect as Select
from Maps import Map_Instantiate as iMap, Map_Print as Print
import random


def selectSpace(fighter, enemies, boarders) -> int:
    emptySpace = "___"
    sightMap = fighter.sightMap
    leftEdge, rightEdge, topEdge, bottomEdge = boarders[0], boarders[1], boarders[2], boarders[3]

    if (leftEdge == rightEdge) and (topEdge == bottomEdge):
        return [leftEdge, topEdge]
    else:
        optionsMap = [[], [], [], [], [], [], [], [], [], [], [], []]
        for row in range(12):
            for column in range(12):
                optionsMap[row] += [sightMap[row][column]]
        
        counter, optionDict = 1, {}
        for column in range(leftEdge, rightEdge+1):
            for row in range(topEdge, bottomEdge+1):
                if (emptySpace in optionsMap[row][column]) and not ("?" == optionsMap[row][column][-1]):
                    optionDict[str(counter)] = [row, column]

                    atmosphere = sightMap[row][column][0]
                    elevation = sightMap[row][column][-1]
                    
                    dot = ""
                    if counter < 10: dot = "._"
                    else: dot = "."
                    
                    optionsMap[row][column] = atmosphere + str(counter) + dot + elevation
                    counter += 1

        choice = ""
        if fighter.rank == "player":
            Print.printOptionsMap(optionsMap, "Options Map")
            choice = Select.takeInput(1, counter)
        else:
            choice = random.randint(1, counter) #find highest concentration of enemies and get as central as possible.

        return optionDict[str(choice)]


def getAtmosphere(source, scale, dmgType) -> str:
    atmosphere, big, little, lingering = "_", "", "", ""

    if source == "Stone":
        if "Blessed" in dmgType: dmgType = "Holy"
        elif "Corpse" in dmgType: dmgType = "Rot"
        elif "Flame" in dmgType: dmgType = "Burn"
        elif "Ice" in dmgType: dmgType = "Freeze"
        elif "Fey" in dmgType: dmgType = "Dream"
        elif "Toxin" in dmgType: dmgType = "Venom"
    
    match dmgType:
        case "Burn": big, little, lingering = "B", "b", "#"
        case "Crush": big, little = "C", "c"
        case "Dream": big, little, lingering = "D", "d", "@"
        case "Freeze": big, little, lingering = "F", "f", "%"
        case "Holy": big, little, lingering = "H", "h", "+"
        case "Pierce": big, little = "P", "p"
        case "Rot": big, little, lingering = "R", "r", "}"
        case "Venom": big, little, lingering = "V", "v", "&"

    match scale:
        case 1: atmosphere = lingering
        case 2: atmosphere = little
        case 3: atmosphere = big

    return atmosphere


def spreadAtmosphere(atmosphere, dmgType, coverage, tossRow, tossColumn, battleMap) -> None:
    upRow, downRow = tossRow - 1, tossRow + 1
    leftColumn, rightColumn = tossColumn - 1, tossColumn + 1
    spaces = []

    for step in range(coverage + 1):
        spaces += addSpaces(tossRow, upRow, downRow, tossColumn, leftColumn, rightColumn)
        upRow -= 1
        downRow += 1
        leftColumn -= 1
        rightColumn += 1

    cloud, cloudSpaces = getAtmosphere("None", 1, dmgType), []
    if dmgType not in ["Crush", "Pierce"]:
        cloudSpaces += addSpaces(tossRow, upRow, downRow, tossColumn, leftColumn, rightColumn)
        
    for space in spaces: setAtmosphere(atmosphere, space[0], space[1], battleMap)
    for cloudSpace in cloudSpaces: setAtmosphere(cloud, cloudSpace[0], cloudSpace[1], battleMap)

def addSpaces(tossRow, upRow, downRow, tossColumn, leftColumn, rightColumn):
    newSpaces = []

    if upRow >= 0:
        newSpaces += [[upRow, tossColumn]]
        if leftColumn >= 0: newSpaces += [[upRow, leftColumn]]
        if rightColumn <= 11: newSpaces += [[upRow, rightColumn]]
    if downRow <= 11:
        newSpaces += [[downRow, tossColumn]]
        if leftColumn >= 0: newSpaces += [[downRow, leftColumn]]
        if rightColumn <= 11: newSpaces += [[downRow, rightColumn]]
        downRow += 1
    if leftColumn >= 0:
        newSpaces += [[tossRow, leftColumn]]
        leftColumn -= 1
    if rightColumn <= 11:
        newSpaces += [[tossRow, rightColumn]]
        rightColumn += 1

    return newSpaces

def setAtmosphere(atmosphere, row, column, battleMap):
    if not any(obstruction in battleMap[row][column] for obstruction in ["/", "("]):
        battleMap[row][column] = atmosphere + battleMap[row][column][1:]