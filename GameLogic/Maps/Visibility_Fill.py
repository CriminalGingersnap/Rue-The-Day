from . import Visibility, MovementOptions as mOpts


def fillVisibilityMap(rank, position, row, column, battleMap, sightMap):
    peak = mOpts.heightDict[battleMap[row][column][-1]]

    if (row > 0):
        if (column < 11): fillFirstQuadrant(rank, position, row, column, peak, battleMap, sightMap)
        if (column > 0): fillSecondQuadrant(rank, position, row, column, peak, battleMap, sightMap)
    if (row < 11):
        if (column > 0): fillThirdQuadrant(rank, position, row, column, peak, battleMap, sightMap)
        if (column < 11): fillFourthQuadrant(rank, position, row, column, peak, battleMap, sightMap)


def fillFirstQuadrant(rank, position, row, column, peak, battleMap, sightMap):
    newRow, newColumn = row - 1, column + 1

    if rank != "player":
        Visibility.lookRight(rank, position, newRow, column, battleMap, sightMap, peak)
        Visibility.lookUp(rank, position, row, newColumn, battleMap, sightMap, peak)
    else:
        Visibility.lookUpRight(rank, position, row, newColumn, battleMap, sightMap, peak)
        Visibility.lookUpRight(rank, position, newRow, column, battleMap, sightMap, peak)  


def fillSecondQuadrant(rank, position, row, column, peak, battleMap, sightMap):
    newRow, newColumn = row - 1, column - 1
    
    if rank != "player":
        Visibility.lookUp(rank, position, row, newColumn, battleMap, sightMap, peak)
        Visibility.lookLeft(rank, position, newRow, column, battleMap, sightMap, peak)
    else:
        Visibility.lookUpLeft(rank, position, newRow, column, battleMap, sightMap, peak)
        Visibility.lookUpLeft(rank, position, row, newColumn, battleMap, sightMap, peak)


def fillThirdQuadrant(rank, position, row, column, peak, battleMap, sightMap):
    newRow, newColumn = row + 1, column - 1
    
    if rank != "player":
        Visibility.lookLeft(rank, position, newRow, column, battleMap, sightMap, peak)
        Visibility.lookDown(rank, position, row, newColumn, battleMap, sightMap, peak)
    else:
        Visibility.lookDownLeft(rank, position, row, newColumn, battleMap, sightMap, peak)
        Visibility.lookDownLeft(rank, position, newRow, column, battleMap, sightMap, peak)


def fillFourthQuadrant(rank, position, row, column, peak, battleMap, sightMap):
    newRow, newColumn = row + 1, column + 1

    if rank != "player":
        Visibility.lookDown(rank, position, row, newColumn, battleMap, sightMap, peak)
        Visibility.lookRight(rank, position, newRow, column, battleMap, sightMap, peak)
    else:
        Visibility.lookDownRight(rank, position, newRow, column, battleMap, sightMap, peak)
        Visibility.lookDownRight(rank, position, row, newColumn, battleMap, sightMap, peak)