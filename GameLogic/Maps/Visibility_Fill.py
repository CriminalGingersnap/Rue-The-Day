
from . import Visibility


def fillVisibilityMap(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    if (row > 0):
        if (column < 11):
            fillFirstOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
            fillSecondOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
        if (column > 0):
            fillThirdOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
            fillForthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 11):
        if (column > 0):
            fillFifthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
            fillSixthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
        if (column < 11):
            fillSeventhOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
            fillEighthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)


def fillFirstOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newColumn, newRow = column + 1, row
    if rank != "player": newRow -=1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            
    Visibility.lookRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows) 
    Visibility.lookUpRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)

def fillSecondOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column
    if rank != "player": newColumn += 1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]

    Visibility.lookUpRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)  
    Visibility.lookUp(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)


def fillThirdOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column
    if rank != "player": newColumn -= 1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]

    Visibility.lookUp(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)
    Visibility.lookUpLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)

def fillForthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newColumn, newRow = column - 1, row
    if rank != "player": newRow -= 1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]

    Visibility.lookUpLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)
    Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)


def fillFifthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newColumn, newRow = column - 1, row
    if rank != "player": newRow += 1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]

    Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)
    Visibility.lookDownLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)

def fillSixthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column
    if rank != "player": newColumn -= 1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]

    Visibility.lookDownLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)
    Visibility.lookDown(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)


def fillSeventhOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column
    if rank != "player": newColumn += 1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]

    Visibility.lookDown(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)
    Visibility.lookDownRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)

def fillEighthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newColumn, newRow = column + 1, row
    if rank != "player": newRow += 1
    sightMap[newRow][newColumn] = battleMap[newRow][newColumn]

    Visibility.lookDownRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)
    Visibility.lookRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows)