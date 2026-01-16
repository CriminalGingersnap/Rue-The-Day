from . import MovementOptions as mOpts, Map, Visibility_Fill as Fill

unseen = "   ?"


def createSightMap(fighter, battleMap):
    shadows, sightMap = [], [[], [], [], [], [], [], [], [], [], [], [], []]

    for column in range(12):
        for row in range(12):
            sightMap[row] += [unseen + battleMap[row][column][-1]]

    position, rank = fighter.position, fighter.rank
    row, column = position[0], position[1]
    viewHeight = mOpts.heightDict[battleMap[row][column][-1]]
    sightMap[row][column] = battleMap[row][column]

    lookUp(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    lookDown(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    lookLeft(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    lookRight(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    lookUpLeft(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)    
    lookUpRight(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    lookDownLeft(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    lookDownRight(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)

    Fill.fillVisibilityMap(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)

    for shadow in shadows:
        row, column = shadow[0], shadow[1]
        if "/" not in sightMap[row][column]: sightMap[row][column] = unseen + sightMap[row][column][-1]

    return sightMap


def look(position, row, column, viewHeight, battleMap, sightMap, obstructionPeak):
    visible, applyShadow = True, False
    space = battleMap[row][column]
    spaceHeight = mOpts.heightDict[space[-1]]

    obstructed = any(occlusion in space for occlusion in ["/"] + Map.majorHazards)
    fogged = any(fog in space for fog in ["="] + Map.minorHazards) and ((abs(position[0] - row) > 3) or (abs(position[1] - column) > 3))
    misted = any(mist in space for mist in ["-"] + Map.lingeringHazards) and ((abs(position[0] - row) > 7) or (abs(position[1] - column) > 7))
    sunken = (spaceHeight - viewHeight) > 1

    if spaceHeight <= obstructionPeak: visible = False
    elif obstructed or misted or fogged:
        if spaceHeight >= viewHeight: obstructionPeak = spaceHeight
        else: applyShadow = True
    elif sunken: obstructionPeak = spaceHeight
    else: obstructionPeak = spaceHeight - 2

    if visible: sightMap[row][column] = battleMap[row][column]

    return applyShadow


def lookUp(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, obstructionPeak = row, 0
    while newRow > 0:
        newRow -= 1

        applyShadow = look(position, newRow, column, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newRow > 0): shadows += [[newRow-1, column]]
        if rank == "player": break

def lookDown(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, obstructionPeak = row, 0
    while newRow < 11:
        newRow += 1

        applyShadow = look(position, newRow, column, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newRow < 11): shadows += [[newRow+1, column]]
        if rank == "player": break

def lookLeft(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newColumn, obstructionPeak = column, 0
    while newColumn > 0:
        newColumn -= 1

        applyShadow = look(position, row, newColumn, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newColumn > 0): shadows += [[row, newColumn-1]]
        if rank == "player": break
        
def lookRight(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newColumn, obstructionPeak = column, 0
    while newColumn < 11:
        newColumn += 1

        applyShadow = look(position, row, newColumn, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newColumn < 11): shadows += [[row, newColumn+1]]
        if rank == "player": break

def lookUpRight(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn, obstructionPeak = row, column, 0
    while (newColumn < 11) and (newRow > 0):
        newColumn += 1
        newRow -= 1

        applyShadow = look(position, newRow, newColumn, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newColumn < 11) and (newRow > 0): shadows += [[newRow-1, newColumn+1]]
        if rank != "player": break

def lookDownRight(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn, obstructionPeak = row, column, 0
    while (newColumn < 11) and (newRow < 11):
        newColumn += 1
        newRow += 1

        applyShadow = look(position, newRow, newColumn, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newColumn < 11) and (newRow < 11): shadows += [[row+1, column+1]]
        if rank != "player": break

def lookDownLeft(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn, obstructionPeak = row, column, 0
    while (newColumn > 0) and (newRow < 11):
        newColumn -= 1
        newRow += 1

        applyShadow = look(position, newRow, newColumn, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newColumn > 0) and (newRow < 11): shadows += [[newRow+1, newColumn-1]] 
        if rank != "player": break

def lookUpLeft(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn, obstructionPeak = row, column, 0
    while (newColumn > 0) and (newRow > 0):
        newColumn -= 1
        newRow -= 1

        applyShadow = look(position, newRow, newColumn, viewHeight, battleMap, sightMap, obstructionPeak)
        if applyShadow and (newColumn > 0) and (newRow > 0): shadows += [[newRow-1, newColumn-1]]
        if rank != "player": break