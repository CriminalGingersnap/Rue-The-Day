from . import Map_Update as uMap, MovementOptions as mOpts, Visibility_Fill as Fill

unseen = "   ?"


def createSightMap(battleMap, position, rank):
    sightMap = [[], [], [], [], [], [], [], [], [], [], [], []]

    for column in range(12):
        for row in range(12):
            sightMap[row] += [unseen + battleMap[row][column][-1]]

    row, column, peak = position[0], position[1], 0
    sightMap[row][column] = battleMap[row][column]

    lookUp(rank, position, row, column, battleMap, sightMap, peak)
    lookDown(rank, position, row, column, battleMap, sightMap, peak)
    lookLeft(rank, position, row, column, battleMap, sightMap, peak)
    lookRight(rank, position, row, column, battleMap, sightMap, peak)
    lookUpLeft(rank, position, row, column, battleMap, sightMap, peak) 
    lookUpRight(rank, position, row, column, battleMap, sightMap, peak)
    lookDownLeft(rank, position, row, column, battleMap, sightMap, peak)
    lookDownRight(rank, position, row, column, battleMap, sightMap, peak)

    Fill.fillVisibilityMap(rank, position, row, column, battleMap, sightMap)

    return sightMap


def look(position, row, column, battleMap, sightMap, peak):
    fighterSpace, vistaSpace = battleMap[position[0]][position[1]], battleMap[row][column]
    standingHeight, vistaHeight = mOpts.heightDict[fighterSpace[-1]], mOpts.heightDict[vistaSpace[-1]]

    visible = True

    obstructed = any(occlusion in vistaSpace for occlusion in ["/"] + uMap.majorHazards)
    fogged = any(fog in vistaSpace for fog in ["="] + uMap.minorHazards) and ((abs(position[0] - row) > 3) or (abs(position[1] - column) > 3))
    misted = any(mist in vistaSpace for mist in ["-"] + uMap.lingeringHazards) and ((abs(position[0] - row) > 6) or (abs(position[1] - column) > 6))

    if vistaHeight < peak: visible = False
    elif obstructed or misted or fogged: peak = max(peak, vistaHeight + 1)
    elif standingHeight < vistaHeight > peak: peak = vistaHeight
    
    if visible: sightMap[row][column] = battleMap[row][column]

    return peak


def lookUp(rank, position, row, column, battleMap, sightMap, peak):
    if rank != "player":
        newRow = row
        while (newRow >= 0):
            peak = look(position, newRow, column, battleMap, sightMap, peak)
            newRow -= 1

def lookDown(rank, position, row, column, battleMap, sightMap, peak):
    if rank != "player":
        newRow = row
        while newRow <= 11:
            peak = look(position, newRow, column, battleMap, sightMap, peak)
            newRow += 1


def lookLeft(rank, position, row, column, battleMap, sightMap, peak):
    if rank != "player":
        newColumn = column
        while newColumn >= 0:
            peak = look(position, row, newColumn, battleMap, sightMap, peak)
            newColumn -= 1
        
def lookRight(rank, position, row, column, battleMap, sightMap, peak):
    if rank != "player":
        newColumn = column
        while newColumn <= 11:
            peak = look(position, row, newColumn, battleMap, sightMap, peak)
            newColumn += 1


def lookUpRight(rank, position, row, column, battleMap, sightMap, peak):
    if rank in ["player", "world"]:
        newRow, newColumn = row, column
        while (newColumn <= 11) and (newRow >= 0):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)                
            newColumn += 1
            newRow -= 1

def lookDownRight(rank, position, row, column, battleMap, sightMap, peak):
    if rank in ["player", "world"]:
        newRow, newColumn = row, column
        while (newColumn <= 11) and (newRow <= 11):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)        
            newColumn += 1
            newRow += 1


def lookDownLeft(rank, position, row, column, battleMap, sightMap, peak):
    if rank in ["player", "world"]:
        newRow, newColumn = row, column
        while (newColumn >= 0) and (newRow <= 11):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)            
            newColumn -= 1
            newRow += 1

def lookUpLeft(rank, position, row, column, battleMap, sightMap, peak):
    if rank in ["player", "world"]:
        newRow, newColumn = row, column
        while (newColumn >= 0) and (newRow >= 0):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)        
            newColumn -= 1
            newRow -= 1