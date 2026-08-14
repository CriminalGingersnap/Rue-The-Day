from . import Map_Instantiate as iMap, Map_Update as uMap
import random


def firstPlacement(instanceMap, rowCount, fighter) -> None:
    available = False
    
    while not available:
        column, row = 0, random.randint(0, (rowCount - 1))
        if fighter.props["rank"] == "player": column = random.randint(0, 1)
        else: column = random.randint(3, 10)

        available = visitSpace(instanceMap, rowCount, row, column, fighter)

    fighter.pos = [row, column, 0]


def visitSpace(instanceMap, rowCount, row, column, fighter) -> bool:
    walkable = False

    if "___" in instanceMap[row][column]:
        instanceMap[row][column] = uMap.setMarker(fighter, instanceMap[row][column])

        if fighter.props["rank"] == "player": walkable = walk(instanceMap, rowCount, row, 0, column + 1)
        else: walkable = walk(instanceMap, rowCount, row, column, 11)

        if not walkable: instanceMap[row][column] = iMap.emptySpace

    return walkable


def walk(instanceMap, rowCount, startingRow, startingColumn, rightStop) -> bool:
    nextColumn, downStop, makingProgress = startingColumn + 1, rowCount - 1, True
    upRow, downRow = max(0, startingRow - 1), min(downStop, startingRow + 1)

    while (nextColumn < rightStop) and makingProgress:
        makingProgress = False

        for row in range(upRow, downRow):
            if instanceMap[row][nextColumn] not in iMap.impermissible:
                upRow, downRow = max(0, row - 1), min(downStop, row + 1)
                nextColumn += 1
                makingProgress = True
                break
        
        if not makingProgress:
            for row in range(0, upRow):
                upRow, downRow = max(0, upRow - 1), max(1, downRow - 1)
                if instanceMap[upRow][nextColumn] not in iMap.impermissible:
                    nextColumn += 1
                    makingProgress = True
                    break

        if not makingProgress:
            for row in range(downRow, downStop):
                upRow, downRow = min(downStop -1, upRow + 1), min(downStop, downRow + 1)
                if instanceMap[downRow][nextColumn] not in iMap.impermissible:
                    nextColumn += 1
                    makingProgress = True
                    break

    return makingProgress


def placeObstruction(instanceMap, obsSpace, obsRange, mapHeight) -> None:
    spaceOptions, colStart, colStop = [], random.randint(0, 4), random.randint(8, 12)
    for row in range(mapHeight):
        for column in range(colStart, colStop):
            if instanceMap[row][column] == iMap.emptySpace: spaceOptions += [[row, column]]

    while (len(spaceOptions) > 0) and (obsRange > 0):
        randSpace = random.choice(spaceOptions)
        randRow, randColumn = randSpace[0], randSpace[1]
        instanceMap[randRow][randColumn] = obsSpace
        
        walkable = walk(instanceMap, mapHeight, randRow, max(0, randColumn - 1), 11)
        if not walkable: instanceMap[randRow][randColumn] = iMap.emptySpace

        spaceOptions.remove(randSpace)
        obsRange -= 1


def placeTrap(instanceMap, trapRange, mapHeight) -> None:
    spaceOptions = []
    for row in range(mapHeight):
        for column in range(12):
            if not any(char in instanceMap[row][column] for char in ["/", ".", ")", "~"] + iMap.intStrings):
                spaceOptions += [[row, column]]

    while (len(spaceOptions) > 0) and (trapRange > 0):
        randSpace = random.choice(spaceOptions)
        randRow, randColumn = randSpace[0], randSpace[1]
        instanceMap[randRow][randColumn] = instanceMap[randRow][randColumn][0] + "___]"

        spaceOptions.remove(randSpace)
        trapRange -= 1


def placeFog(instanceMap, atmo, atmoRange, mapHeight) -> None:
    atmo, spaceOptions = "_", []

    for row in range(mapHeight):
        for column in range(12):
            if instanceMap[row][column][0] == "_": spaceOptions += [[row, column]]

    while (len(spaceOptions) > 0) and (atmoRange > 0):
        randSpace = random.choice(spaceOptions)
        randRow, randColumn = randSpace[0], randSpace[1]
        instanceMap[randRow][randColumn] = atmo + instanceMap[randRow][randColumn][1:]

        spaceOptions.remove(randSpace)
        atmoRange -= 1