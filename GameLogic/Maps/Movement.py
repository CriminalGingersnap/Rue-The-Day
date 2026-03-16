from Systems import PlayerSelect as Select
from . import Map_Update as uMap, MovementOptions, Map_Print as Print
import random


def moveFighter(fighter, battleMap, target, closeRanks) -> None:
    movementMap = MovementOptions.setMoveOptions(fighter, target, battleMap)
    moveOptions = prepareOptions(movementMap)
    spaceOptions, firstSpace, lastSpace = moveOptions[0], moveOptions[1], moveOptions[2]
    stationary, moveChoice = False, None

    if fighter.rank == "player": moveChoice = movePlayer(movementMap, lastSpace)
    else: moveChoice = moveNPC(fighter, target, spaceOptions, firstSpace, lastSpace, closeRanks)

    if int(moveChoice) != 1:
        if fighter.rank != "player": Select.waitPrint(fighter.name + " moves.")

        row = spaceOptions[moveChoice][0]
        column = spaceOptions[moveChoice][1]
        stepCount = spaceOptions[moveChoice][2]
        uMap.updatePlacement(battleMap, fighter.sightMap, row, column, fighter)
        
        fighter.atrb["cur_sp"] -= stepCount
        if stepCount > fighter.atrb["base_sp"] // 2: fighter.cndt["running"] = True
    
    else: stationary = True
    return stationary


def getTargetDistance(fighter, target):
    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    targetRow, targetColumn = target.position[0], target.position[1]
    rowDiff, columnDiff = abs(fighterRow - targetRow), abs(fighterColumn - targetColumn)
    return max(rowDiff, columnDiff)

def getSpaceDistance(row1, row2, column1, column2) -> int:
    rowDiff, columnDiff = abs(row1 - row2), abs(column1 - column2)
    return max(rowDiff, columnDiff)


def moveNPC(fighter, target, spaceOptions, firstSpace, lastSpace, closeRanks) -> str:
    targetDistance = getTargetDistance(fighter, target)
    reach = fighter.equipment["weapon"]["reach"]

    closestIndex = 1
    leastToTarget = leastFromFighter = targetDistance
    highestEffective = desiredDistance = 0
    rankedOptions, rankedIndices = {}, {}

    for spaceNumber in range(firstSpace, lastSpace):
        row, column = spaceOptions[str(spaceNumber)][0], spaceOptions[str(spaceNumber)][1]
        spaceToTarget = getSpaceDistance(target.position[0], row, target.position[1], column)

        if spaceToTarget in rankedOptions: rankedOptions[spaceToTarget] += [[row, column, spaceNumber]]
        else: rankedOptions[spaceToTarget] = [[row, column, spaceNumber]]

        if spaceToTarget < leastToTarget: leastToTarget = spaceToTarget
        if (spaceToTarget > highestEffective) and (spaceToTarget <= reach): highestEffective = spaceToTarget

    if closeRanks or (highestEffective == 0): desiredDistance = leastToTarget
    else: desiredDistance = highestEffective

    for square in rankedOptions[desiredDistance]:
        row, column = square[0], square[1]
        spaceToFighter = getSpaceDistance(fighter.position[0], row, fighter.position[1], column)

        if spaceToFighter < leastFromFighter:
            leastFromFighter = spaceToFighter
            rankedIndices[spaceToFighter] = [square[2]]
        elif spaceToFighter == leastFromFighter:
            if spaceToFighter not in rankedIndices: rankedIndices[spaceToFighter] = [square[2]]
            else: rankedIndices[spaceToFighter] += [square[2]]

    closestIndex = random.choice(rankedIndices[leastFromFighter])
    return str(closestIndex)


def movePlayer(movementMap, lastSpace) -> str:
    Print.printOptionsMap(movementMap, "Movement Map")

    Select.waitPrint("Space:")
    return str(Select.takeInput(1, lastSpace))


def prepareOptions(movementMap) -> list:
    spaceOptions = {}
    firstSpace = lastSpace = 1

    for row in range(12):
        for column in range(12):
            contents = movementMap[row][column]
            if ":" in contents:
                spaceNumber = str(contents.split(':')[0])
                if any(mark in spaceNumber for mark in [".", "!"]): spaceNumber = "1"
                if "_" in spaceNumber: spaceNumber = spaceNumber.split('_')[1]
                elif "~" in spaceNumber: spaceNumber = spaceNumber.split('~')[1]

                stepCount = contents.split(':')[1]
                stepCount = stepCount[0]

                spaceOptions[spaceNumber] = [row, column, int(stepCount)]
                lastSpace += 1

    if "1" not in spaceOptions: firstSpace = 2
    return [spaceOptions, firstSpace, lastSpace]