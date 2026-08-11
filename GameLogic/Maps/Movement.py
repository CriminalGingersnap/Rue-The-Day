from Systems import PlayerSelect as Select
from . import Map_Update as uMap, MovementOptions as mOpts, Map_Print as Print, Map_Instantiate as iMap
import random


def moveFighter(fighter, battleMap, target, closeRanks, mapHeight=12, mapName="") -> None:
    movementMap = mOpts.setMoveOptions(fighter, target, battleMap, mapHeight, mapName)
    moveOptions = prepareOptions(movementMap, battleMap, mapHeight)
    spaceOptions, firstSpace, lastSpace = moveOptions[0], moveOptions[1], moveOptions[2]
    stationary, moveChoice = False, None

    player = fighter.props["rank"] in ["player", "world"]
    if player: moveChoice = movePlayer(movementMap, lastSpace, fighter.props["name"], mapHeight)
    else: moveChoice = moveNPC(fighter, target, spaceOptions, firstSpace, lastSpace, closeRanks)

    row = spaceOptions[moveChoice][0]
    column = spaceOptions[moveChoice][1]
    
    if (battleMap[row][column][1] == "~") and not fighter.cndt["winged"]: fighter.cndt["submerged"] = True
    else: fighter.cndt["submerged"] = False

    if int(moveChoice) != 1:
        if not player: Select.waitPrint(fighter.props["name"] + " moves.")
        uMap.updatePlacement(battleMap, fighter.sightMap, row, column, fighter)

        stepCount = spaceOptions[moveChoice][3]
        fighter.atrb["cur_sp"] -= stepCount
        if stepCount > fighter.atrb["base_sp"] // 2: fighter.cndt["running"] = True
    elif not player: Select.waitPrint(fighter.props["name"] + " sets in place and may use two abilities.")

    else: stationary = True
    return stationary


def getTargetDistance(fighter, target) -> int:
    fighterRow, fighterColumn, fighterHeight = fighter.pos[0], fighter.pos[1], fighter.pos[2]
    targetRow, targetColumn, targetHeight = target.pos[0], target.pos[1], target.pos[2]
    return getSpaceDistance(fighterRow, targetRow, fighterColumn, targetColumn, fighterHeight, targetHeight)

def getSpaceDistance(row1, row2, column1, column2, height1, height2) -> int:
    rowDiff, columnDiff, heightDiff = abs(row1 - row2), abs(column1 - column2), abs(height1 - height2)
    return max(rowDiff, columnDiff, heightDiff)


def moveNPC(fighter, target, spaceOptions, firstSpace, lastSpace, closeRanks) -> str:
    targetDistance = getTargetDistance(fighter, target)
    reach = fighter.equip["weapon"]["reach"]

    closestIndex = 1
    leastToTarget = leastFromFighter = targetDistance
    highestEffective = desiredDistance = 0
    rankedOptions, rankedIndices = {}, {}

    for spaceNumber in range(firstSpace, lastSpace + 1):
        row, column, height = spaceOptions[str(spaceNumber)][0], spaceOptions[str(spaceNumber)][1], spaceOptions[str(spaceNumber)][2]
        spaceToTarget = getSpaceDistance(target.pos[0], row, target.pos[1], column, target.pos[2], height)

        if spaceToTarget in rankedOptions: rankedOptions[spaceToTarget] += [[row, column, spaceNumber]]
        else: rankedOptions[spaceToTarget] = [[row, column, spaceNumber]]

        if spaceToTarget < leastToTarget: leastToTarget = spaceToTarget
        if (spaceToTarget > highestEffective) and (spaceToTarget <= reach): highestEffective = spaceToTarget

    if closeRanks or (highestEffective == 0): desiredDistance = leastToTarget
    else: desiredDistance = highestEffective

    for square in rankedOptions[desiredDistance]:
        row, column = square[0], square[1]
        spaceToFighter = getSpaceDistance(fighter.pos[0], row, fighter.pos[1], column, fighter.pos[2], height)

        if spaceToFighter < leastFromFighter:
            leastFromFighter = spaceToFighter
            rankedIndices[spaceToFighter] = [square[2]]
        elif spaceToFighter == leastFromFighter:
            if spaceToFighter not in rankedIndices: rankedIndices[spaceToFighter] = [square[2]]
            else: rankedIndices[spaceToFighter] += [square[2]]

    closestIndex = random.choice(rankedIndices[leastFromFighter])
    return str(closestIndex)


def movePlayer(movementMap, lastSpace, name, mapHeight) -> str:
    Print.printOptionsMap(movementMap, name+ "'s Options Map", mapHeight)

    Select.waitPrint("Space:")
    return str(Select.takeInput(1, lastSpace))


def prepareOptions(movementMap, battleMap, mapHeight) -> list:
    spaceOptions = {}
    firstSpace, lastSpace = 1, 0

    for row in range(mapHeight):
        for column in range(12):
            contents = movementMap[row][column]
            if ":" in contents:
                spaceNumber = str(contents.split(':')[0])
                if any(mark in spaceNumber for mark in [".", "!"]): spaceNumber = "1"

                if spaceNumber[0] not in iMap.intStrings: spaceNumber = spaceNumber[1:]

                stepCount = contents.split(':')[1]
                stepCount = stepCount[0]

                height = mOpts.heightDict[battleMap[row][column][-1]]
                spaceOptions[spaceNumber] = [row, column, height, int(stepCount)]
                lastSpace += 1

    if "1" not in spaceOptions: firstSpace = 2
    return [spaceOptions, firstSpace, lastSpace]