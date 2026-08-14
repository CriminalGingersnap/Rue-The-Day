from . import Visibility, MovementOptions as mOpts


def fillVisibilityMap(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight):
    if (row > 0):
        if (column < 11): fillFirstQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap)
        if (column > 0): fillSecondQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap)
    if (row < mapHeight-1):
        if (column > 0): fillThirdQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight)
        if (column < 11): fillFourthQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight)


def fillFirstQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap):
    newRow, newColumn = row - 1, column + 1

    Visibility.lookRight(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap)
    Visibility.lookUp(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap)
    Visibility.lookUpRight(playerRank, insightful, position, row, newColumn, battleMap, sightMap)
    Visibility.lookUpRight(playerRank, insightful, position, newRow, column, battleMap, sightMap) 


def fillSecondQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap):
    newRow, newColumn = row - 1, column - 1
    
    Visibility.lookUp(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap)
    Visibility.lookLeft(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap)
    Visibility.lookUpLeft(playerRank, insightful, position, row, newColumn, battleMap, sightMap)
    Visibility.lookUpLeft(playerRank, insightful, position, newRow, column, battleMap, sightMap)


def fillThirdQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight):
    newRow, newColumn = row + 1, column - 1
    
    Visibility.lookLeft(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap)
    Visibility.lookDown(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap, mapHeight)
    Visibility.lookDownLeft(playerRank, insightful, position, row, newColumn, battleMap, sightMap, mapHeight)
    Visibility.lookDownLeft(playerRank, insightful, position, newRow, column, battleMap, sightMap, mapHeight)


def fillFourthQuadrant(playerRank, insightful, position, row, column, battleMap, sightMap, mapHeight):
    newRow, newColumn = row + 1, column + 1

    Visibility.lookDown(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap, mapHeight)
    Visibility.lookRight(playerRank, insightful, position, newRow, newColumn, battleMap, sightMap)
    Visibility.lookDownRight(playerRank, insightful, position, row, newColumn, battleMap, sightMap, mapHeight)
    Visibility.lookDownRight(playerRank, insightful, position, newRow, column, battleMap, sightMap, mapHeight)