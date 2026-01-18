from Systems import PlayerSelect as Select
from . import Map_Update as uMap, MovementOptions, Map_Print as Print
import random


def moveFighter(fighter, battleMap, target, closeRanks) -> None:
    movementMap = MovementOptions.setMoveOptions(fighter, target, battleMap)
    moveOptions = prepareOptions(movementMap)
    spaceOptions, highestNumber = moveOptions[0], moveOptions[1]
    stationary = False

    moveChoice = None
    if fighter.rank == "player": moveChoice = movePlayer(movementMap, highestNumber)
    else: moveChoice = moveNPC(fighter, target, spaceOptions, highestNumber, closeRanks)

    if int(moveChoice) != 1:
        if fighter.rank != "player": Select.waitPrint(fighter.name + " moves.")

        row = spaceOptions[moveChoice][0]
        column = spaceOptions[moveChoice][1]
        stepCount = int(spaceOptions[moveChoice][2])
        uMap.updatePlacement(battleMap, fighter.sightMap, row, column, fighter)
        
        fighter.atrb["cur_sp"] -= stepCount
        if stepCount > fighter.atrb["base_sp"] // 2: fighter.cndt["running"] = True
    
    else: stationary = True
    return stationary


def findDistance(fighter, target):
    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    targetRow, targetColumn = target.position[0], target.position[1]
    rowDiff, columnDiff = abs(fighterRow - targetRow), abs(fighterColumn - targetColumn)

    return max(rowDiff, columnDiff)


def moveNPC(fighter, target, spaceOptions, highestNumber, closeRanks) -> str:
    distance = findDistance(fighter, target)
    reach = fighter.equipment["weapon"]["reach"]

    closestIndex = 1
    leastDistance_Target, leastDistance_Fighter = distance, distance
    highestEffectiveDistance, desiredDistance = 0, 0
    rankedOptions, rankedIndices = {}, {}

    for squareNumber in range(1, highestNumber):
        row, column = spaceOptions[str(squareNumber)][0], spaceOptions[str(squareNumber)][1]

        rowDiff_Space = abs(target.position[0] - row)
        columnDiff_Space = abs(target.position[1] - column)
        spaceDistance = max(rowDiff_Space, columnDiff_Space)

        if spaceDistance in rankedOptions: rankedOptions[spaceDistance] += [[row, column, squareNumber]]
        else: rankedOptions[spaceDistance] = [[row, column, squareNumber]]

        if spaceDistance < leastDistance_Target:
            leastDistance_Target = spaceDistance
        if (spaceDistance > highestEffectiveDistance) and (spaceDistance <= reach):
            highestEffectiveDistance = spaceDistance

    if closeRanks or (highestEffectiveDistance == 0): desiredDistance = leastDistance_Target
    else: desiredDistance = highestEffectiveDistance

    for square in rankedOptions[desiredDistance]:
        rowDiff_Fighter = abs(fighter.position[0] - square[0])
        columnDiff_Fighter = abs(fighter.position[1] - square[1])
        distanceFromFighter = max(rowDiff_Fighter, columnDiff_Fighter)

        if distanceFromFighter < leastDistance_Fighter:
            leastDistance_Fighter = distanceFromFighter
            rankedIndices[distanceFromFighter] = [square[2]]
        elif distanceFromFighter == leastDistance_Fighter:
            if distanceFromFighter not in rankedIndices: rankedIndices[distanceFromFighter] = [square[2]]
            else: rankedIndices[distanceFromFighter] += [square[2]]
    
    closestIndex = random.choice(rankedIndices[leastDistance_Fighter])

    return str(closestIndex)


def movePlayer(movementMap, highestNumber) -> str:
    Print.printOptionsMap(movementMap, "Movement Map")

    Select.waitPrint("Space:")
    return str(Select.takeInput(1, highestNumber))


def prepareOptions(movementMap) -> list:
    spaceOptions = {}
    highestNumber = 0

    for row in range(12):
        for column in range(12):
            contents = movementMap[row][column]
            if ":" in contents:
                spaceNumber = str(contents.split(':')[0])
                if "." in spaceNumber: spaceNumber = "1"
                if "_" in spaceNumber: spaceNumber = spaceNumber.split('_')[1]

                stepCount = contents.split(':')[1]
                stepCount = stepCount[0]

                spaceOptions[spaceNumber] = [row, column, stepCount]
                highestNumber += 1
    
    return [spaceOptions, highestNumber]