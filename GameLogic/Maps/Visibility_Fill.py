from . import Visibility, MovementOptions as mOpts


def fillVisibilityMap(rank, position, row, column, battleMap, sightMap, mapHeight):
    if (row > 0):
        if (column < 11): fillFirstQuadrant(rank, position, row, column, battleMap, sightMap)
        if (column > 0): fillSecondQuadrant(rank, position, row, column, battleMap, sightMap)
    if (row < mapHeight-1):
        if (column > 0): fillThirdQuadrant(rank, position, row, column, battleMap, sightMap, mapHeight)
        if (column < 11): fillFourthQuadrant(rank, position, row, column, battleMap, sightMap, mapHeight)


def fillFirstQuadrant(rank, position, row, column, battleMap, sightMap):
    newRow, newColumn = row - 1, column + 1

    if rank != "player":
        Visibility.lookRight(rank, position, newRow, newColumn, battleMap, sightMap)
        Visibility.lookUp(rank, position, newRow, newColumn, battleMap, sightMap)
    else:
        Visibility.lookUpRight(rank, position, row, newColumn, battleMap, sightMap)
        Visibility.lookUpRight(rank, position, newRow, column, battleMap, sightMap)  


def fillSecondQuadrant(rank, position, row, column, battleMap, sightMap):
    newRow, newColumn = row - 1, column - 1
    
    if rank != "player":
        Visibility.lookUp(rank, position, newRow, newColumn, battleMap, sightMap)
        Visibility.lookLeft(rank, position, newRow, newColumn, battleMap, sightMap)
    else:
        Visibility.lookUpLeft(rank, position, newRow, column, battleMap, sightMap)
        Visibility.lookUpLeft(rank, position, row, newColumn, battleMap, sightMap)


def fillThirdQuadrant(rank, position, row, column, battleMap, sightMap, mapHeight):
    newRow, newColumn = row + 1, column - 1
    
    if rank != "player":
        Visibility.lookLeft(rank, position, newRow, newColumn, battleMap, sightMap)
        Visibility.lookDown(rank, position, newRow, newColumn, battleMap, sightMap, mapHeight)
    else:
        Visibility.lookDownLeft(rank, position, row, newColumn, battleMap, sightMap, mapHeight)
        Visibility.lookDownLeft(rank, position, newRow, column, battleMap, sightMap, mapHeight)


def fillFourthQuadrant(rank, position, row, column, battleMap, sightMap, mapHeight):
    newRow, newColumn = row + 1, column + 1

    if rank != "player":
        Visibility.lookDown(rank, position, newRow, newColumn, battleMap, sightMap, mapHeight)
        Visibility.lookRight(rank, position, newRow, newColumn, battleMap, sightMap)
    else:
        Visibility.lookDownRight(rank, position, newRow, column, battleMap, sightMap, mapHeight)
        Visibility.lookDownRight(rank, position, row, newColumn, battleMap, sightMap, mapHeight)