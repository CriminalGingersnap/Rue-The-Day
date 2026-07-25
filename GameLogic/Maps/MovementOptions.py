from Maps import Elevation, Map_Instantiate as iMap, Visibility, Map_Update as uMap

heightDict = {Elevation.doubleUp: 5, Elevation.up: 4, Elevation.middle: 3,
               Elevation.down: 2, Elevation.doubleDown: 1, "]": 3}


def instantiateMoveMap(fighter, fighterRow, fighterColumn, battleMap, sightMap) -> list:
    hazards = uMap.majorHazards + uMap.minorHazards
    movementMap = [[], [], [], [], [], [], [], [], [], [], [], []]

    for row in range(12):
        for column in range(12):
            movementMap[row] += [sightMap[row][column]]
            
            if movementMap[row][column][2] in iMap.intStrings: 
                movementMap[row][column] = movementMap[row][column][:2] + "!!" + movementMap[row][column][-1]
            
            if movementMap[row][column][-1] == "]": movementMap[row][column] = movementMap[row][column][:-1] + "|"
            
            if (movementMap[row][column][0] in hazards) and (battleMap[fighterRow][fighterColumn][0] not in hazards):
                if fighter.props["rank"] != "player": movementMap[row][column] = iMap.pit

    movementMap[fighterRow][fighterColumn] = "_1:0"
    return movementMap


def setMoveOptions(fighter, target, battleMap) -> list:
    fighterRow, fighterColumn = fighter.pos[0], fighter.pos[1]
    aquatic, skittish, winged  = fighter.cndt["aquatic"], fighter.cndt["skittish"], fighter.cndt["winged"]

    npc, simulation = fighter.props["rank"] not in ["player", "world"], None
    if npc:
        if skittish: simulation = target.sightMap
        else: simulation = Visibility.createSightMap(battleMap, target.pos, fighter.props["rank"])
    sightMap = fighter.sightMap
    movementMap = instantiateMoveMap(fighter, fighterRow, fighterColumn, battleMap, sightMap)
    
    leftEdge, rightEdge = max(0, (fighterColumn-fighter.atrb["cur_sp"])), min(12, (fighterColumn+fighter.atrb["cur_sp"] + 1))
    topEdge, bottomEdge = max(0, (fighterRow-fighter.atrb["cur_sp"])), min(12, (fighterRow+fighter.atrb["cur_sp"] + 1))
    anyContact, anyUnseen = False, False
    waterLine = 0

    for runs in range(fighter.atrb["base_sp"] * 2):
        for column in range(leftEdge, rightEdge):
            for row in range(topEdge, bottomEdge):
                sightSpace = sightMap[row][column]

                if "~" in battleMap[row][column]: waterLine = max(waterLine, (heightDict[sightSpace[-1]] + 1))

                stepCount = traverse(movementMap, sightMap, fighterRow, fighterColumn, row, column, waterLine, aquatic, winged)
                
                if stepCount <= fighter.atrb["cur_sp"]:
                    freeSpace = False
                    if "___" in sightSpace:
                        movementMap[row][column] = "_:" + str(stepCount)
                        freeSpace = True
                    elif "~~~" in sightSpace:
                        movementMap[row][column] = "~:" + str(stepCount)
                        freeSpace = True
                    elif ")" in sightSpace:
                        movementMap[row][column] = "):" + str(stepCount)
                        if winged: freeSpace = True
                    elif "!" in sightSpace: movementMap[row][column] = "!:" + str(stepCount)
                    elif "/" in sightSpace: movementMap[row][column] = "/:" + str(stepCount)
                    elif any(playerMark in sightSpace for playerMark in [".", "e", "s"]): movementMap[row][column] = ".:" + str(stepCount)

                    if npc and freeSpace:
                        contact = (Visibility.unseen not in simulation[row][column]) and (Visibility.unseen not in sightSpace)
                        if contact:
                            anyContact = True
                            if skittish: movementMap[row][column] = "!:" + str(stepCount)
                        else:
                            anyUnseen = True
                            if not skittish: movementMap[row][column] = "!:" + str(stepCount)

    if npc and (((not skittish) and not anyContact) or (skittish and not anyUnseen)):
        for column in range(leftEdge, rightEdge):
            for row in range(topEdge, bottomEdge):
                if "!:" in movementMap[row][column]:
                    stepCount = movementMap[row][column].split(':')[1]
                    terrain = sightMap[row][column][1]

                    if int(stepCount) < fighter.atrb["cur_sp"] // 2:
                        movementMap[row][column] = terrain + ":" + stepCount

    counter = 2
    for column in range(12):
        for row in range(12):
            if (row == fighterRow) and (column == fighterColumn): continue

            moveSpace = movementMap[row][column]
            elevation = sightMap[row][column][-1]
            terrain = sightMap[row][column][1]

            if (":" in moveSpace) and not any(marker in moveSpace for marker in [".", "!", "/"]):
                if (")" not in moveSpace) or winged:
                    stepCount = moveSpace.split(':')[1]
                    if counter < 10: movementMap[row][column] = terrain + str(counter) + ":" + str(stepCount) + elevation
                    else: movementMap[row][column] = str(counter) + ":" + str(stepCount) + elevation
                    counter += 1

            if "." in moveSpace: movementMap[row][column] = "/../" + elevation
            elif "!" in moveSpace: movementMap[row][column] = "/!!/" + elevation
            elif "/" in moveSpace: movementMap[row][column] = "////" + elevation
            elif ")" in moveSpace and not winged: movementMap[row][column] = "))))" + elevation

    if not npc: movementMap[fighterRow][fighterColumn] = ".1:0" + sightMap[fighterRow][fighterColumn][-1]
    elif not anyContact: movementMap[fighterRow][fighterColumn] = "!1:0" + sightMap[fighterRow][fighterColumn][-1]

    return movementMap
    

def traverse(movementMap, sightMap, fighterRow, fighterColumn, squareRow, squareColumn, waterLine, aquatic, winged) -> int:
    singleStepCost = stepCost(sightMap, fighterRow, fighterColumn, squareRow, squareColumn, waterLine, aquatic, winged)

    if (fighterRow == squareRow) and (abs(fighterColumn - squareColumn) == 1): return singleStepCost
    elif (fighterColumn == squareColumn) and (abs(fighterRow - squareRow) == 1): return singleStepCost
    elif (abs(fighterRow-squareRow) == 1) and (abs(fighterColumn - squareColumn) == 1): return singleStepCost
    else:
        lowest = 50
        for adjacentRow in range(max(squareRow - 1, 0), min(squareRow + 2, 12)):
            for adjacentColumn in range(max(squareColumn - 1, 0), min(squareColumn + 2, 12)):
                contents = movementMap[adjacentRow][adjacentColumn]

                if ":" in contents:
                    stepCount = contents.split(':')[1]

                    if (int(stepCount) < lowest):
                        nextStepCost = stepCost(sightMap, adjacentRow, adjacentColumn, squareRow, squareColumn, waterLine, aquatic, winged)
                        lowest = int(stepCount) + nextStepCost

        return lowest
    

def stepCost(sightMap, lastRow, lastColumn, nextRow, nextColumn, waterLine, aquatic, winged) -> int:
    cost = 1

    lastWet = "~" in sightMap[lastRow][lastColumn]
    nextWet = "~" in sightMap[nextRow][nextColumn]
    lastFrozen = any(frozen in sightMap[lastRow][lastColumn] for frozen in ["F", "f"])
    nextFrozen = any(frozen in sightMap[nextRow][nextColumn] for frozen in ["F", "f"])

    lastZ = heightDict[sightMap[lastRow][lastColumn][-1]]
    nextZ = heightDict[sightMap[nextRow][nextColumn][-1]]
    if lastWet and (aquatic or lastFrozen): lastZ = waterLine
    if nextWet and (aquatic or nextFrozen): nextZ = waterLine

    if lastZ < nextZ: cost = (nextZ - lastZ) + 1
    elif lastZ > nextZ: cost = (lastZ - nextZ)

    if nextWet and not nextFrozen:
        if aquatic: cost -= 1
        elif not winged: cost += 1
    
    if (")" in sightMap[nextRow][nextColumn]) and (not winged): cost += 2
    elif "/" in sightMap[nextRow][nextColumn]:
        if not winged: cost += 3
        else: cost += 1

    return cost