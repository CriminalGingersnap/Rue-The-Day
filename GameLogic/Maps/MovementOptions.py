from Maps import Elevation, Map_Instantiate as iMap, Visibility, Map_Update as uMap

heightDict = {Elevation.doubleUp: 4, Elevation.up: 3, Elevation.middle: 2,
               Elevation.down: 1, Elevation.doubleDown: 0, "]": 2, "?": 50}


def setMoveOptions(fighter, target, battleMap) -> list:
    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    leftEdge, rightEdge = max(0, (fighterColumn-fighter.atrb["cur_sp"])), min(12, (fighterColumn+fighter.atrb["cur_sp"] + 1))
    topEdge, bottomEdge = max(0, (fighterRow-fighter.atrb["cur_sp"])), min(12, (fighterRow+fighter.atrb["cur_sp"] + 1))
    hazards = uMap.majorHazards + uMap.minorHazards

    npc, simulation, noContact = fighter.rank != "player", None, False
    if npc: simulation = Visibility.createSightMap(battleMap, target.position, fighter.rank)
    instanceMap = fighter.sightMap

    movementMap = [[], [], [], [], [], [], [], [], [], [], [], []]
    for row in range(12):
        for column in range(12):
            movementMap[row] += [instanceMap[row][column]]
            if movementMap[row][column][-1] == "]": movementMap[row][column] = movementMap[row][column][:-1] + "|"
            if movementMap[row][column][0] in hazards:
                if fighter.cndt["sapient"] and (movementMap[fighterRow][fighterColumn][0] not in hazards):
                    movementMap[row][column] =  iMap.wall
                else: movementMap[row][column] = "_" + movementMap[row][column][1:]

    movementMap[fighterRow][fighterColumn] = "_1:0"

    for runs in range(fighter.atrb["cur_sp"] * fighter.atrb["cur_sp"]):
        for column in range(leftEdge, rightEdge):
            for row in range(topEdge, bottomEdge):
                stepCount = traverse(movementMap, instanceMap, fighterRow, fighterColumn, row, column)
                if stepCount <= fighter.atrb["cur_sp"]:                   
                    if npc: noContact = (Visibility.unseen in simulation[row][column]) and (Visibility.unseen not in instanceMap[row][column])
                    if npc and (("!" in instanceMap[row][column]) or noContact):
                        movementMap[row][column] = "_!:" + str(stepCount)

                    elif ("___" in instanceMap[row][column]):
                        movementMap[row][column] = ":" + str(stepCount)

                    elif "/" not in instanceMap[row][column]:
                        if ")()(" in instanceMap[row][column]:
                            movementMap[row][column] = "_):" + str(stepCount) + "_"

                        elif ("." in instanceMap[row][column]):
                            movementMap[row][column] = "_.:" + str(stepCount) + "_"

    counter = 2
    for column in range(12):
        for row in range(12):
            if (":" in movementMap[row][column]) and not any(marker in movementMap[row][column] for marker in [".", "!"]):
                stepCount = movementMap[row][column].split(':')[1]
                if counter < 10: movementMap[row][column] = "_" + str(counter) + ":" + str(stepCount)
                else: movementMap[row][column] = str(counter) + ":" + str(stepCount)
                counter += 1

            if "." in movementMap[row][column]: movementMap[row][column] = "_.._"
            elif "!" in movementMap[row][column]: movementMap[row][column] = "/!!/"
            elif ")" in movementMap[row][column]: movementMap[row][column] = ")()("

            if any(char in movementMap[row][column] for char in [":", ".", "!", ")"]):
                movementMap[row][column] += instanceMap[row][column][-1]

    movementMap[fighterRow][fighterColumn] = ".1:0" + instanceMap[fighterRow][fighterColumn][-1]

    return movementMap


def stepCost(instanceMap, lastRow, lastColumn, nextRow, nextColumn) -> int:
    cost = 1

    if ")" in instanceMap[nextRow][nextColumn]: cost = 4
    else:
        lastZ = heightDict[instanceMap[lastRow][lastColumn][-1]]
        nextZ = heightDict[instanceMap[nextRow][nextColumn][-1]]
        if lastZ < nextZ: cost = (nextZ - lastZ) + 1
        elif lastZ > nextZ: cost = (lastZ - nextZ)

    if any(plant in instanceMap[lastRow][lastColumn] for plant in ["p", "P"]): cost += 50

    return cost
    

def traverse(movementMap, instanceMap, fighterRow, fighterColumn, squareRow, squareColumn) -> int:
    startHeight = heightDict[instanceMap[fighterRow][fighterColumn][-1]]
    singleStepCost = stepCost(instanceMap, fighterRow, fighterColumn, squareRow, squareColumn)

    if (fighterRow == squareRow) and (abs(fighterColumn - squareColumn) == 1): return singleStepCost
    elif (fighterColumn == squareColumn) and (abs(fighterRow - squareRow) == 1): return singleStepCost
    elif (abs(fighterRow-squareRow) == 1) and (abs(fighterColumn - squareColumn) == 1): return singleStepCost
    else:
        lowest = 50
        for row in range(max(squareRow - 1, 0), min(squareRow + 2, 12)):
            for column in range(max(squareColumn - 1, 0), min(squareColumn + 2, 12)):
                contents = movementMap[row][column]

                if ":" in contents:
                    stepCount = contents.split(':')[1]
                    stepCount = stepCount[0]

                    if (int(stepCount) < lowest):
                        nextStepCost = stepCost(instanceMap, row, column, squareRow, squareColumn)
                        lowest = int(stepCount) + nextStepCost

        return lowest