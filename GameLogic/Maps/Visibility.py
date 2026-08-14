from . import Map_Instantiate as iMap, Map_Update as uMap, MovementOptions as mOpts, Visibility_Fill as Fill

unseen = "   ?"


def createSightMap(battleMap, position, rank, insightful, mapHeight=12):
    sightMap = [[], [], [], [], [], [], [], [], [], [], [], []]
    if mapHeight == 24: sightMap = [[], [], [], [], [], [], [], [], [], [], [], [],
                                    [], [], [], [], [], [], [], [], [], [], [], []]

    for column in range(12):
        for row in range(mapHeight):
            sightMap[row] += [unseen + battleMap[row][column][-1]]

    row, column = position[0], position[1]
    sightMap[row][column] = battleMap[row][column]
    playerRank = rank == "player"

    lookUp(playerRank, insightful, position, row, column, battleMap, sightMap)
    lookDown(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight)
    lookLeft(playerRank, insightful, position, row, column, battleMap, sightMap)
    lookRight(playerRank, insightful, position, row, column, battleMap, sightMap)
    lookUpLeft(playerRank, insightful, position, row, column, battleMap, sightMap) 
    lookUpRight(playerRank, insightful, position, row, column, battleMap, sightMap)
    lookDownLeft(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight)
    lookDownRight(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight)

    Fill.fillVisibilityMap(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight)

    return sightMap


def look(position, row, column, battleMap, sightMap, peak):
    vistaSpace = battleMap[row][column]
    standingHeight, vistaHeight = position[2], mOpts.heightDict[vistaSpace[-1]]

    rowDiff, colDiff = abs(position[0] - row), abs(position[1] - column)

    visible = True

    obstructed = any(obstruction in vistaSpace for obstruction in ["/", ".", "e", "s"] + iMap.intStrings) and ((rowDiff > 0) or (colDiff > 0))
    clouded = any(cloud in vistaSpace for cloud in uMap.majorHazards) and ((rowDiff > 1) or (colDiff > 1))
    fogged = any(fog in vistaSpace for fog in ["="] + uMap.minorHazards) and ((rowDiff > 3) or (colDiff > 3))
    misted = any(mist in vistaSpace for mist in ["-"] + uMap.lingeringHazards) and ((rowDiff > 5) or (colDiff > 5))

    if vistaHeight < peak: visible = False
    elif obstructed or clouded or misted or fogged: peak = max(peak, vistaHeight + 1)
    elif standingHeight < vistaHeight > peak: peak = vistaHeight
    
    if visible: sightMap[row][column] = battleMap[row][column]

    return peak


def lookUp(playerRank, insightful, position, row, column, battleMap, sightMap):
    if insightful or not playerRank:
        newRow, peak = row, 0
        while (newRow >= 0):
            peak = look(position, newRow, column, battleMap, sightMap, peak)
            newRow -= 1

def lookDown(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight):
    if insightful or not playerRank:
        newRow, peak = row, 0
        while newRow < mapHeight:
            peak = look(position, newRow, column, battleMap, sightMap, peak)
            newRow += 1

def lookLeft(playerRank, insightful, position, row, column, battleMap, sightMap):
    if insightful or not playerRank:
        newColumn, peak = column, 0
        while newColumn >= 0:
            peak = look(position, row, newColumn, battleMap, sightMap, peak)
            newColumn -= 1
        
def lookRight(playerRank, insightful, position, row, column, battleMap, sightMap):
    if insightful or not playerRank:
        newColumn, peak = column, 0
        while newColumn <= 11:
            peak = look(position, row, newColumn, battleMap, sightMap, peak)
            newColumn += 1


def lookUpRight(playerRank, insightful, position, row, column, battleMap, sightMap):
    if playerRank or insightful:
        newRow, newColumn, peak = row, column, 0
        while (newColumn <= 11) and (newRow >= 0):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)                
            newColumn += 1
            newRow -= 1

def lookDownRight(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight):
    if playerRank or insightful:
        newRow, newColumn, peak = row, column, 0
        while (newColumn <= 11) and (newRow < mapHeight):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)        
            newColumn += 1
            newRow += 1

def lookDownLeft(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight):
    if playerRank or insightful:
        newRow, newColumn, peak = row, column, 0
        while (newColumn >= 0) and (newRow < mapHeight):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)            
            newColumn -= 1
            newRow += 1

def lookUpLeft(playerRank, insightful, position, row, column, battleMap, sightMap):
    if playerRank or insightful:
        newRow, newColumn, peak = row, column, 0
        while (newColumn >= 0) and (newRow >= 0):
            peak = look(position, newRow, newColumn, battleMap, sightMap, peak)        
            newColumn -= 1
            newRow -= 1