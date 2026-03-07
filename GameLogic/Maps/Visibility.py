from . import Map_Update as uMap, MovementOptions as mOpts, Visibility_Fill as Fill

unseen = "   ?"


def createSightMap(battleMap, position, rank):
    shadows, sightMap = [], [[], [], [], [], [], [], [], [], [], [], [], []]

    for column in range(12):
        for row in range(12):
            sightMap[row] += [unseen + battleMap[row][column][-1]]

    row, column = position[0], position[1]
    sightMap[row][column] = battleMap[row][column]

    lookUp(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)
    lookDown(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)
    lookLeft(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)
    lookRight(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)
    lookUpLeft(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)    
    lookUpRight(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)
    lookDownLeft(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)
    lookDownRight(rank, position, row, column, battleMap, sightMap, shadows, 0, False, 0)

    Fill.fillVisibilityMap(rank, position, row, column, battleMap, sightMap, shadows)

    for shadow in shadows:
        row, column = shadow[0], shadow[1]
        if "/" not in sightMap[row][column]: sightMap[row][column] = unseen + sightMap[row][column][-1]

    return sightMap


def look(position, row, column, battleMap, sightMap, peak, offset):
    visible, applyShadow = True, False
    fighterSpace, vistaSpace = battleMap[position[0]][position[1]], battleMap[row][column]
    fighterHeight, vistaHeight = mOpts.heightDict[fighterSpace[-1]], mOpts.heightDict[vistaSpace[-1]]

    obstructed = any(occlusion in vistaSpace for occlusion in ["/"] + uMap.majorHazards)
    fogged = any(fog in vistaSpace for fog in ["="] + uMap.minorHazards) and ((abs(position[0] - row) > 3) or (abs(position[1] - column) > 3))
    misted = any(mist in vistaSpace for mist in ["-"] + uMap.lingeringHazards) and ((abs(position[0] - row) > 6) or (abs(position[1] - column) > 6))
    sunken = (vistaHeight - fighterHeight) > 0

    if vistaHeight <= peak: visible = False
    elif obstructed or misted or fogged:
        if vistaHeight >= fighterHeight: peak = vistaHeight
        else: applyShadow = True
    elif sunken: peak = vistaHeight
    else: peak = vistaHeight - 2

    if visible and not offset: sightMap[row][column] = battleMap[row][column]

    return [applyShadow, peak]


def lookUp(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, originalColumn):
    if rank != "player":
        newRow = row
        while newRow > 0:
            newRow -= 1

            result = look(position, newRow, column, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newRow > 0): shadows += [[newRow-1, column]]

            if offset:
                offsetPeak = look(position, newRow, originalColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)

def lookDown(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, originalColumn):
    if rank != "player":
        newRow = row
        while newRow < 11:
            newRow += 1

            result = look(position, newRow, column, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newRow < 11): shadows += [[newRow+1, column]]

            if offset:
                offsetPeak = look(position, newRow, originalColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)


def lookLeft(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, originalRow):
    if rank != "player":
        newColumn = column
        while newColumn > 0:
            newColumn -= 1

            result = look(position, row, newColumn, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newColumn > 0): shadows += [[row, newColumn-1]]

            if offset:
                offsetPeak = look(position, originalRow, newColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)
        
def lookRight(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, originalRow):
    if rank != "player":
        newColumn = column
        while newColumn < 11:
            newColumn += 1

            result = look(position, row, newColumn, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newColumn < 11): shadows += [[row, newColumn+1]]

            if offset:
                offsetPeak = look(position, originalRow, newColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)


def lookUpRight(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, shift):
    if rank == "player":
        newRow, newColumn = row, column
        while (newColumn < 11) and (newRow > 0):
            newColumn += 1
            newRow -= 1

            result = look(position, newRow, newColumn, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newColumn < 11) and (newRow > 0): shadows += [[newRow-1, newColumn+1]]

            if offset and (newRow > 0):
                offsetPeak = look(position, newRow+shift, newColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)

def lookDownRight(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, shift):
    if rank == "player":
        newRow, newColumn = row, column
        while (newColumn < 11) and (newRow < 11):
            newColumn += 1
            newRow += 1

            result = look(position, newRow, newColumn, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newColumn < 11) and (newRow < 11): shadows += [[row+1, column+1]]

            if offset and (newRow < 11):
                offsetPeak = look(position, newRow+shift, newColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)


def lookDownLeft(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, shift):
    if rank == "player":
        newRow, newColumn = row, column
        while (newColumn > 0) and (newRow < 11):
            newColumn -= 1
            newRow += 1

            result = look(position, newRow, newColumn, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newColumn > 0) and (newRow < 11): shadows += [[newRow+1, newColumn-1]] 

            if offset and (newRow < 11):
                offsetPeak = look(position, newRow+shift, newColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)

def lookUpLeft(rank, position, row, column, battleMap, sightMap, shadows, obstructionPeak, offset, shift):
    if rank == "player":
        newRow, newColumn = row, column
        while (newColumn > 0) and (newRow > 0):
            newColumn -= 1
            newRow -= 1

            result = look(position, newRow, newColumn, battleMap, sightMap, obstructionPeak, False)
            applyShadow, obstructionPeak = result[0], result[1]
            if applyShadow and (newColumn > 0) and (newRow > 0): shadows += [[newRow-1, newColumn-1]]

            if offset and (newRow > 0):
                offsetPeak = look(position, newRow+shift, newColumn, battleMap, sightMap, obstructionPeak, True)[1]
                obstructionPeak = max(obstructionPeak, offsetPeak)