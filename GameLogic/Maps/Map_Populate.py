from . import Map_Instantiate as iMap, Map_Update as uMap
import random


def firstPlacement(instanceMap, rowCount, fighter) -> None:
    available = False
    while not available:
        column, row = 0, random.randint(0, (rowCount - 1))
        if fighter.props["rank"] == "player": column = random.randint(0, 1)
        else: column = random.randint(5, 10)

        available = visitSpace(instanceMap, rowCount, row, column, fighter)

    fighter.position = [row, column]


def visitSpace(instanceMap, rowCount, row, column, fighter) -> bool:
    marker = uMap.setMarker(fighter, instanceMap[row][column])

    if "___" in instanceMap[row][column]:
        instanceMap[row][column] = marker

        if fighter.props["rank"] == "player":
            walkable = walk(instanceMap, rowCount, row, 0, column + 1)
        else: walkable = walk(instanceMap, rowCount, row, column, 12)

    if not walkable: instanceMap[row][column] = iMap.emptySpace
    return walkable


def walk(instanceMap, rowCount, startingRow, startingColumn, rightStop):
    currentColumn, makingProgress = startingColumn + 1, True
    upRow, downRow = max(0, startingRow - 1), min(11, startingRow + 1)

    while (currentColumn < rightStop) and makingProgress:
        for row in range(upRow, downRow):
            if instanceMap[row][currentColumn] not in iMap.impermissible:
                upRow, downRow = max(0, startingRow - 1), min(11, startingRow + 1)
                currentColumn += 1
                makingProgress = True
                break
            else: makingProgress = False
        
        if not makingProgress:
            for row in range(0, upRow):
                if instanceMap[upRow][currentColumn] not in iMap.impermissible:
                    upRow -= 1
                    downRow += 1
                    makingProgress = True
                    break

        if not makingProgress:
            for row in range(downRow, rowCount):
                if instanceMap[row][currentColumn] not in iMap.impermissible:
                    upRow += 1
                    downRow -= 1
                    makingProgress = True
                    break

    return makingProgress


def placeObstruction(instanceMap, obstruction) -> bool:
    row, column = random.randint(0, 11), random.randint(0, 11)

    if instanceMap[row][column] == iMap.emptySpace:
        instanceMap[row][column] = obstruction
        walkable = walk(instanceMap, 12, row, max(0, column - 1), 12)
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

    if not any(char in instanceMap[row][column] for char in ["/", ".", ")", "~"] + iMap.intStrings):
        atmosphere = instanceMap[row][column][0]
        instanceMap[row][column] = atmosphere + "___]"
        return True
    else:
        return False