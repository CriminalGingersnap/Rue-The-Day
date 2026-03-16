from . import Map_Instantiate as iMap
from Abilities import Area_Apply as Area
import random

up, down = "↑", "↓"
doubleUp, doubleDown = "⇑", "⇓"
middle = "|"


def setElevation(battleMap, environment, slope):
    match slope:
        case "right": slopeLeftRight(battleMap, "right")
        case "left": slopeLeftRight(battleMap, "left")
        case "lr": slopeLeftRight(battleMap, "sides")
        case "up": slopeDownUp(battleMap, "up")
        case "down": slopeDownUp(battleMap, "down")
        case "ud": slopeDownUp(battleMap, "sides")
        case "craters": bumps(battleMap, "down")
        case "hills": bumps(battleMap, "up")

    adjustObstructionHeight(battleMap)
    adjustEnvironment(battleMap, environment)


def bumps(battleMap, lean):
    bumps = random.randint(3, 7)
    maxElevation, minElevation = "", ""
    match lean:
        case "up": maxElevation, minElevation = doubleUp, up
        case "down": maxElevation, minElevation = doubleDown, down

    for bump in range(bumps):
        row, column = random.randint(0, 11), random.randint(0, 11)
        battleMap[row][column] = battleMap[row][column][:-1] + maxElevation

        spreadMax = random.randint(0, 1)
        spreadMin = 2- spreadMax

        upRow, downRow = row - 1, row + 1
        leftColumn, rightColumn = column - 1, column + 1
        maxSpaces, minSpaces = [], []

        for step in range(spreadMax):
            maxSpaces += Area.addSpaces(row, upRow, downRow, column, leftColumn, rightColumn)
            upRow -= 1
            downRow += 1
            leftColumn -= 1
            rightColumn += 1

        for step in range(spreadMin):
            minSpaces += Area.addSpaces(row, upRow, downRow, column, leftColumn, rightColumn)
            if (upRow + 1) < row:
                if (0 <= leftColumn < rightColumn <= 11) and (0 <= upRow < downRow <= 11):
                    minSpaces += [[upRow, rightColumn-1], [upRow, leftColumn+1]]
                    minSpaces += [[downRow-1, rightColumn], [upRow+1, rightColumn]]
                    minSpaces += [[downRow, rightColumn-1], [downRow, leftColumn+1]]
                    minSpaces += [[downRow-1, leftColumn], [upRow+1, leftColumn]]
            upRow -= 1
            downRow += 1
            leftColumn -= 1
            rightColumn += 1
            
        for maxSpace in maxSpaces: battleMap[maxSpace[0]][maxSpace[1]] = battleMap[maxSpace[0]][maxSpace[1]][:-1] + maxElevation
        for minSpace in minSpaces:
            if maxElevation not in battleMap[minSpace[0]][minSpace[1]]: battleMap[minSpace[0]][minSpace[1]] = battleMap[minSpace[0]][minSpace[1]][:-1] + minElevation


def resetLtRtElv(lean):
    if lean == "right":
        randomLeft = random.choice([doubleUp, up, middle])
        randomRight = random.choice([doubleDown, down, middle])
        randomMiddle = random.choice([randomRight, randomLeft, middle])
    elif lean == "left":
        randomLeft = random.choice([doubleDown, down, middle])
        randomRight = random.choice([doubleUp, up, middle])
        randomMiddle = random.choice([randomRight, randomLeft, middle])
    else:
        randomMiddle = random.choice([doubleUp, up, middle])
        randomLeft = random.choice([randomMiddle, doubleDown, down, middle])
        randomRight = random.choice([randomMiddle, doubleDown, down, middle])
    
    return [randomLeft, randomMiddle, randomRight]

def slopeLeftRight(battleMap, lean):
    elv = resetLtRtElv(lean)
    randomLeft, randomMiddle, randomRight = elv[0], elv[1], elv[2]
    firstEndRow, thirdStartRow = random.randint(3, 6), random.randint(6, 9)

    for row in range(12):
        if row in [firstEndRow, thirdStartRow]:
            elv = resetLtRtElv(lean)
            randomLeft, randomMiddle, randomRight = elv[0], elv[1], elv[2]

        firstEndCol = random.randint(2, 5)
        thirdStartCol = random.randint(7, 10)

        for column in range(0, firstEndCol):
            battleMap[row][column] = battleMap[row][column][:-1] + randomLeft
        for column in range(firstEndCol, thirdStartCol):
            battleMap[row][column] = battleMap[row][column][:-1] + randomMiddle
        for column in range(thirdStartCol, 12):
            battleMap[row][column] = battleMap[row][column][:-1] + randomRight
        
    for column in range(12):
        for row in range(11):
            selfElevation = battleMap[row][column][-1]
            downElevation = battleMap[row+1][column][-1]

            if selfElevation != downElevation:
                if random.choice([True, False]):
                    battleMap[row][column] = battleMap[row][column][:-1] + downElevation
                else:
                    battleMap[row+1][column] = battleMap[row+1][column][:-1] + selfElevation


def resetUpDnElv(lean):
    if lean == "up":
        randomTop = random.choice([doubleDown, down, middle])
        randomBottom = random.choice([doubleUp, up, middle])
        randomMiddle = random.choice([randomTop, randomBottom, middle])
    elif lean == "down":
        randomTop = random.choice([doubleUp, up, middle])
        randomBottom = random.choice([doubleDown, down, middle])
        randomMiddle = random.choice([randomTop, randomBottom, middle])
    else:
        randomMiddle = random.choice([doubleUp, up, middle])
        randomTop = random.choice([randomMiddle, doubleDown, down, middle])
        randomBottom = random.choice([randomMiddle, doubleDown, down, middle])

    return [randomTop, randomMiddle, randomBottom]

def slopeDownUp(battleMap, lean):
    elv = resetUpDnElv(lean)
    randomTop, randomMiddle, randomBottom = elv[0], elv[1], elv[2]
    firstEndCol, thirdStartCol = random.randint(3, 6), random.randint(6, 9)

    for column in range(12):
        if column in [firstEndCol, thirdStartCol]:
            elv = resetUpDnElv(lean)
            randomTop, randomMiddle, randomBottom = elv[0], elv[1], elv[2]
        
        firstEndRow = random.randint(2, 5)
        thirdStartRow = random.randint(7, 10)

        for row in range(0, firstEndRow):
            battleMap[row][column] = battleMap[row][column][:-1] + randomTop
        for row in range(firstEndRow, thirdStartRow):
            battleMap[row][column] = battleMap[row][column][:-1] + randomMiddle
        for row in range(thirdStartRow, 6):
            battleMap[row][column] = battleMap[row][column][:-1] + randomBottom

    for column in range(11):
        for row in range(12):
            selfElevation = battleMap[row][column][-1]
            rightElevation = battleMap[row][column+1][-1]

            if selfElevation != rightElevation:
                if random.choice([True, False]):
                    battleMap[row][column] = battleMap[row][column][:-1] + rightElevation
                else:
                    battleMap[row][column+1] = battleMap[row][column+1][:-1] + selfElevation


def adjustObstructionHeight(battleMap):
    for row in range(12):
        for column in range(12):
            if "/" in battleMap[row][column]:
                elevation = battleMap[row][column][-1]
                if elevation == doubleDown: elevation = random.choice([doubleDown, down, middle, up, doubleUp])
                elif elevation == down: elevation = random.choice([down, middle, up, doubleUp])
                elif elevation == middle: elevation = random.choice([middle, up, doubleUp])
                elif elevation == up: elevation = random.choice([up, doubleUp])
                battleMap[row][column] = battleMap[row][column][:-1] + elevation
            elif ")" in battleMap[row][column]:
                battleMap[row][column] = battleMap[row][column][:-1] + doubleDown


def adjustEnvironment(battleMap, environment):
    match environment:
        case "Clubs":
            for row in range(12):
                for column in range(12):
                    flood(battleMap, row, column, 2)

        case "Hearts":
            for row in range(12):
                for column in range(12):
                    if "/" not in battleMap[row][column]:
                        flood(battleMap, row, column, 1)
                        if down in battleMap[row][column]:
                            battleMap[row][column] = "=" + battleMap[row][column][1:]
                        if middle in battleMap[row][column]:
                            battleMap[row][column] = "-" + battleMap[row][column][1:]
                    
        case "Diamonds":
            for row in range(12):
                for column in range(12):
                    if any(downer in battleMap[row][column] for downer in [doubleDown, down]):
                            battleMap[row][column] = "=" + battleMap[row][column][1:]
                    if any(upper in battleMap[row][column] for upper in [middle, up]):
                        battleMap[row][column] = "-" + battleMap[row][column][1:]
                    

def flood(battleMap, row, column, severity):
    elevation = doubleDown
    if severity == 2: elevation = down

    if any(downer in battleMap[row][column] for downer in [doubleDown, down]):
        if "." in battleMap[row][column]:
            battleMap[row][column] = battleMap[row][column][:-1] + middle
        elif doubleDown in battleMap[row][column]: 
            battleMap[row][column] = iMap.pool[:-1] + elevation

        elif ("/" not in battleMap[row][column]) and (severity == 2) and (down in battleMap[row][column]):
            battleMap[row][column] = iMap.pool[:-1] + elevation