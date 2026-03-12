from . import Map_Instantiate as iMap, Map_Update as uMap
import random


def firstPlacement(instanceMap, fighter) -> None:
    rightEdgeEmpty = []

    if fighter.rank != "player":
        for row in range(4):
            if instanceMap[row][11] not in iMap.impermissible: rightEdgeEmpty += [row]

    available = False
    while not available:
        column, row = 0, random.randint(0, 3)
        if fighter.rank == "player": column = random.randint(0, 1)
        else: column = random.randint(5, 10)

        available = visitSpace(instanceMap, row, column, fighter, rightEdgeEmpty)

    fighter.position = [row, column]


def visitSpace(instanceMap, row, column, fighter, endTargets) -> bool:
    marker = uMap.setMarker(fighter, instanceMap[row][column])

    if "___" in instanceMap[row][column]:
        instanceMap[row][column] = marker

        if fighter.rank == "player":
            walkable = walk(instanceMap, row, 0, column + 1)[0]
            if not walkable: instanceMap[row][column] = iMap.emptySpace
            return walkable

        else:
            walkResult = walk(instanceMap, row, column, 12)
            walkable = walkResult[0]
            endRow = walkResult[1]

            if (not walkable) or (endRow not in endTargets):
                instanceMap[row][column] = iMap.emptySpace
                return False
            else: return True    
    else: return False


def placeObstruction(instanceMap, obstruction) -> bool:
    row, column = random.randint(0, 11), random.randint(0, 11)

    if instanceMap[row][column] == iMap.emptySpace:
        instanceMap[row][column] = obstruction
        walkable = walk(instanceMap, random.randint(0, 11), 0, 12)[0]
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
        elif type == "Mana": instanceMap[row][column] = iMap.manaWell
        elif type == "Mist": instanceMap[row][column] = iMap.mistSpace
        elif type == "Rime": instanceMap[row][column] = iMap.rimeSpace
        elif type == "Blessed": instanceMap[row][column] = iMap.sacredSpace
        elif type == "Smoke": instanceMap[row][column] = iMap.smokeSpace
        elif type == "Toxin": instanceMap[row][column] = iMap.toxinSpace
        return True
    else:
        return False

def placeTrap(instanceMap):
    row, column = random.randint(0, 11), random.randint(0, 11)

    if not any(char in instanceMap[row][column] for char in ["/", ".", "!", ")", "~"]):
        atmosphere = instanceMap[row][column][0]
        instanceMap[row][column] = atmosphere + "___]"
        return True
    else:
        return False


def walk(instanceMap, startingRow, staringColumn, columnLimit) -> bool:
    previousFreeRow, nextColumn = startingRow, staringColumn
    makingProgress, visited = True, []

    while makingProgress and (nextColumn < columnLimit):
        topLimit, bottomLimit = max(0, previousFreeRow - 1), min(11, previousFreeRow + 1)

        gotOne = False
        for row in range(topLimit, bottomLimit):
            while (nextColumn < columnLimit) and (instanceMap[row][nextColumn] not in iMap.impermissible):
                previousFreeRow = row
                nextColumn += 1
                gotOne = True
                visited = []

        if not gotOne:
            visited += [previousFreeRow]
            if (topLimit > 0) and (topLimit not in visited) and (instanceMap[topLimit][nextColumn - 1] not in iMap.impermissible):
                previousFreeRow -= 1
                gotOne = True
            elif (bottomLimit < 11) and (bottomLimit not in visited) and (instanceMap[bottomLimit][nextColumn - 1] not in iMap.impermissible):
                previousFreeRow += 1
                gotOne = True

        makingProgress = gotOne

    return [makingProgress, previousFreeRow]