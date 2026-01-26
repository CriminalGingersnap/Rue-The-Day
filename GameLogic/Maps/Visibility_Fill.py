from . import Visibility


def getCoreRowPeak(position, newRow, newColumn, battleMap, sightMap, row) -> int:
    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0, False)[1]
    offsetPeak = Visibility.look(position, row, newColumn, battleMap, sightMap, obstructionPeak, True)[1]
    obstructionPeak = max(obstructionPeak, offsetPeak)

    return obstructionPeak

def getCoreColumnPeak(position, newRow, newColumn, battleMap, sightMap, column) -> int:
    obstructionPeak = Visibility.look(position, newRow, newColumn, battleMap, sightMap, 0, False)[1]
    offsetPeak = Visibility.look(position, newRow, column, battleMap, sightMap, obstructionPeak, True)[1]
    obstructionPeak = max(obstructionPeak, offsetPeak)

    return obstructionPeak


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

    obstructionPeak = getCoreRowPeak(position, newRow, newColumn, battleMap, sightMap, row)

    Visibility.lookRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, row) 
    Visibility.lookUpRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, -1)


def fillSecondOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column
    if rank != "player": newColumn += 1

    obstructionPeak = getCoreColumnPeak(position, newRow, newColumn, battleMap, sightMap, column)

    Visibility.lookUpRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, 1)  
    Visibility.lookUp(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, column)


def fillThirdOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column
    if rank != "player": newColumn -= 1

    obstructionPeak = getCoreColumnPeak(position, newRow, newColumn, battleMap, sightMap, column)

    Visibility.lookUp(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, column)
    Visibility.lookUpLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, -1)

def fillForthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newColumn, newRow = column - 1, row
    if rank != "player": newRow -= 1

    obstructionPeak = getCoreRowPeak(position, newRow, newColumn, battleMap, sightMap, row)

    Visibility.lookUpLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, 1)
    Visibility.lookLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, row)


def fillFifthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newColumn, newRow = column - 1, row
    if rank != "player": newRow += 1

    obstructionPeak = getCoreRowPeak(position, newRow, newColumn, battleMap, sightMap, row)

    Visibility.lookLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, row)
    Visibility.lookDownLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, 1)

def fillSixthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column
    if rank != "player": newColumn -= 1

    obstructionPeak = getCoreColumnPeak(position, newRow, newColumn, battleMap, sightMap, column)

    Visibility.lookDownLeft(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, -1)
    Visibility.lookDown(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, column)


def fillSeventhOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column
    if rank != "player": newColumn += 1

    obstructionPeak = getCoreColumnPeak(position, newRow, newColumn, battleMap, sightMap, column)

    Visibility.lookDown(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, column)
    Visibility.lookDownRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, 1)

def fillEighthOctant(rank, position, row, column, battleMap, sightMap, shadows):
    newColumn, newRow = column + 1, row
    if rank != "player": newRow += 1

    obstructionPeak = getCoreRowPeak(position, newRow, newColumn, battleMap, sightMap, row)

    Visibility.lookDownRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, -1)
    Visibility.lookRight(rank, position, newRow, newColumn, battleMap, sightMap, shadows, obstructionPeak, True, row)