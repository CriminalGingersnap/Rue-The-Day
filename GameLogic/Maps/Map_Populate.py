from . import Map_Instantiate as iMap, Map_Update as uMap
import random


def firstPlacement(instanceMap, rowCount, fighter) -> None:
    available = False
    
    while not available:
        column, row = 0, random.randint(0, (rowCount - 1))
        if fighter.props["rank"] == "player": column = random.randint(0, 1)
        else: column = random.randint(3, 10)

        available = visitSpace(instanceMap, rowCount, row, column, fighter)

    fighter.pos = [row, column]


def visitSpace(instanceMap, rowCount, row, column, fighter) -> bool:
    walkable = False

    if "___" in instanceMap[row][column]:
        instanceMap[row][column] = uMap.setMarker(fighter, instanceMap[row][column])

        if fighter.props["rank"] == "player": walkable = walk(instanceMap, rowCount, row, 0, column + 1)
        else: walkable = walk(instanceMap, rowCount, row, column, 11)

        if not walkable: instanceMap[row][column] = iMap.emptySpace

    return walkable


def walk(instanceMap, rowCount, startingRow, startingColumn, rightStop):
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


def placeObstruction(instanceMap, obstruction, multiplier) -> bool:
    rowCount = 4 * multiplier
    row, column = random.randint(0, (rowCount - 1)), random.randint(0, 11)

    if instanceMap[row][column] == iMap.emptySpace:
        instanceMap[row][column] = obstruction
        walkable = walk(instanceMap, rowCount, row, max(0, column - 1), 11)
        if not walkable: instanceMap[row][column] = iMap.emptySpace
        return walkable
    else:
        return False

def placeFog(instanceMap, type) -> bool:
    row, column = random.randint(0, 11), random.randint(0, 11)

    if instanceMap[row][column] == iMap.emptySpace:
        if type == "Death": instanceMap[row][column] = iMap.deathSpace
        elif type == "Dazzle": instanceMap[row][column] = iMap.dazzleSpace
        elif type == "Fog": instanceMap[row][column] = iMap.fogSpace
        elif type == "Mist": instanceMap[row][column] = iMap.mistSpace
        elif type == "Noxious": instanceMap[row][column] = iMap.noxiousSpace
        elif type == "Rime": instanceMap[row][column] = iMap.rimeSpace
        elif type == "Sacred": instanceMap[row][column] = iMap.sacredSpace
        elif type == "Smoke": instanceMap[row][column] = iMap.smokeSpace
        return True
    else:
        return False

def placeTrap(instanceMap):
    row, column = random.randint(0, 11), random.randint(0, 11)

    if not any(char in instanceMap[row][column] for char in ["/", ".", ")", "~"] + iMap.intStrings):
        atmosphere = instanceMap[row][column][0]
        instanceMap[row][column] = atmosphere + "___]"
        return True
    else:
        return False