from . import Map_Instantiate as iMap, Map
import random


def firstPlacement(instanceMap, fighter, mapHeight) -> None:
    rightEdgeEmpty = []

    if fighter.rank != "player":
        for row in range(mapHeight):
            if instanceMap[row][11] not in iMap.wall + iMap.pit: rightEdgeEmpty += [row]

    available = False
    while not available:
        column, row = 0, random.randint(0, mapHeight - 1)
        if fighter.rank == "player": column = random.randint(0, 1)
        else: column = random.randint(4, 10)

        available = visitSpace(instanceMap, row, column, fighter, mapHeight, rightEdgeEmpty)

    fighter.position = [row, column]


def visitSpace(instanceMap, row, column, fighter, mapHeight, endTargets) -> bool:
    marker = Map.setMarker(fighter, instanceMap[row][column])

    if instanceMap[row][column] in [iMap.emptySpace, iMap.smokeSpace, iMap.fogSpace, iMap.mistSpace]:
        instanceMap[row][column] = marker

        if fighter.rank == "player":
            walkable = walk(instanceMap, row, mapHeight, 0, column + 1)[0]
            if not walkable: instanceMap[row][column] = iMap.emptySpace
            return walkable

        else:
            walkResult = walk(instanceMap, row, mapHeight, column, 12)
            walkable = walkResult[0]
            endRow = walkResult[1]

            if (not walkable) or (endRow not in endTargets):
                instanceMap[row][column] = iMap.emptySpace
                return False
            else: return True    
    else: return False


def placeObstruction(instanceMap, obstruction, mapHeight) -> bool:
    row, column = random.randint(0, mapHeight), random.randint(0, 11)

    if instanceMap[row][column] == iMap.emptySpace:
        instanceMap[row][column] = obstruction
        walkable = walk(instanceMap, random.randint(0, mapHeight), mapHeight, 0, 12)[0]
        if not walkable: instanceMap[row][column] = iMap.emptySpace
        return walkable
    else:
        return False

def placeFog(instanceMap, type, mapHeight) -> bool:
    row, column = random.randint(0, mapHeight), random.randint(0, 11)

    if instanceMap[row][column] == iMap.emptySpace:
        if type == "Death": instanceMap[row][column] = iMap.deathSpace
        elif type == "Dazzle": instanceMap[row][column] = iMap.dazzleSpace
        elif type == "Fog": instanceMap[row][column] = iMap.fogSpace
        elif type == "Mana": instanceMap[row][column] = iMap.manaWell
        elif type == "Mist": instanceMap[row][column] = iMap.mistSpace
        elif type == "Rime": instanceMap[row][column] = iMap.rimeSpace
        elif type == "Blessed": instanceMap[row][column] = iMap.sacredSpace
        elif type == "Smoke": instanceMap[row][column] = iMap.smokeSpace
        elif type == "Toxic": instanceMap[row][column] = iMap.toxicSpace
        return True
    else:
        return False

def placeTrap(instanceMap, mapHeight):
    row, column = random.randint(0, mapHeight), random.randint(0, 11)

    if not any(char in instanceMap[row][column] for char in ["/", ".", "!", ")"]):
        atmosphere = instanceMap[row][column][0]
        instanceMap[row][column] = atmosphere + "___]"
        return True
    else:
        return False


def walk(instanceMap, startingRow, rowLimit, staringColumn, columnLimit) -> bool:
    previousFreeRow, nextColumn = startingRow, staringColumn
    makingProgress, visited = True, []

    while makingProgress and (nextColumn < columnLimit):
        topLimit, bottomLimit = max(0, previousFreeRow - 1), min(rowLimit, previousFreeRow + 1)

        gotOne = False
        for row in range(topLimit, bottomLimit):
            while (nextColumn < columnLimit) and (instanceMap[row][nextColumn] not in iMap.wall + iMap.pit):
                previousFreeRow = row
                nextColumn += 1
                gotOne = True
                visited = []

        if not gotOne:
            visited += [previousFreeRow]
            if (topLimit > 0) and (topLimit not in visited) and (instanceMap[topLimit][nextColumn - 1] not in iMap.wall + iMap.pit):
                previousFreeRow -= 1
                gotOne = True
            elif (bottomLimit < rowLimit) and (bottomLimit not in visited) and (instanceMap[bottomLimit][nextColumn - 1] not in iMap.wall + iMap.pit):
                previousFreeRow += 1
                gotOne = True

        makingProgress = gotOne

    return [makingProgress, previousFreeRow]