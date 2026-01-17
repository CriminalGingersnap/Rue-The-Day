
from . import Visibility


def fillVisibilityMap(rank, position, row, column, battleMap, sightMap, shadows):
    if (row > 0):
        if (column < 11):
            fillFirstOctant(rank, position, row, column, battleMap, sightMap, shadows)
            fillSecondOctant(rank, position, row, column, battleMap, sightMap, shadows)
        if (column > 0):
            fillThirdOctant(rank, position, row, column, battleMap, sightMap, shadows)
            fillForthOctant(rank, position, row, column, battleMap, sightMap, shadows)
    if (row < 11):
        if (column > 0):
            fillFifthOctant(rank, position, row, column, battleMap, sightMap, shadows)
            fillSixthOctant(rank, position, row, column, battleMap, sightMap, shadows)
        if (column < 11):
            fillSeventhOctant(rank, position, row, column, battleMap, sightMap, shadows)
            fillEighthOctant(rank, position, row, column, battleMap, sightMap, shadows)


def fillFirstOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newColumn, newRow = column + 1, row
    if rank != "player": newRow -=1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]
            
    Visibility.lookRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak) 
    Visibility.lookUpRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)

def fillSecondOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column
    if rank != "player": newColumn += 1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]

    Visibility.lookUpRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)  
    Visibility.lookUp(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)


def fillThirdOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column
    if rank != "player": newColumn -= 1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]

    Visibility.lookUp(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)
    Visibility.lookUpLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)

def fillForthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newColumn, newRow = column - 1, row
    if rank != "player": newRow -= 1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]

    Visibility.lookUpLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)
    Visibility.lookLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)


def fillFifthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newColumn, newRow = column - 1, row
    if rank != "player": newRow += 1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]

    Visibility.lookLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)
    Visibility.lookDownLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)

def fillSixthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column
    if rank != "player": newColumn -= 1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]

    Visibility.lookDownLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)
    Visibility.lookDown(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)


def fillSeventhOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column
    if rank != "player": newColumn += 1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]

    Visibility.lookDown(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)
    Visibility.lookDownRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)

def fillEighthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newColumn, newRow = column + 1, row
    if rank != "player": newRow += 1

    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0)[1]

    Visibility.lookDownRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)
    Visibility.lookRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak)