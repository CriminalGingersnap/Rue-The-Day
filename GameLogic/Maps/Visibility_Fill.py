
from . import Visibility, Map


def checkTransparent(position, row, column, viewHeight, obstructionPeak, sightMap):
    unobstructed, oneOff = False, False

    if Visibility.unseen not in sightMap[row][column]:
        lineReport = Visibility.checkHeight(position, row, column, viewHeight, viewHeight-2, sightMap)
        oneOff, obstructionHeight = lineReport[1], lineReport[2]

        if ("/" not in sightMap[row][column]) or (obstructionHeight <= viewHeight):
            unobstructed = True

        if obstructionHeight > obstructionPeak: obstructionPeak = obstructionHeight
    
    return [unobstructed, oneOff, obstructionPeak]


def fillVisibilityMap(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    if (row > 0) and (column < 10):
        fillFirstOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row > 1) and (column < 11):
        fillSecondOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row > 1) and (column > 0):
        fillThirdOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row > 0) and (column > 1):
        fillForthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 11) and (column > 1):
        fillFifthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 10) and (column > 0):
        fillSixthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 10) and (column < 11):
        fillSeventhOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 11) and (column < 10):
        fillEighthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows)


def fillFirstOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column + 2
    lookResult = []

    lookResult = checkTransparent(position, newRow+1, newColumn-1, viewHeight, -1, sightMap)
    downLeftClear, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

    if downLeftClear: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newColumn < 11):
            shadows += [[newRow, newColumn+1]]
            if newRow > 0: shadows += [[newRow-1, newColumn+1]]

        # if checkTransparent(position, newRow, newColumn-1, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = 1, -1
        
        Visibility.lookRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak) 

        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookUpRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
        else: sightMap[newRow][newColumn+1] = Visibility.unseen


def fillSecondOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 2, column + 1
    lookResult = []
    
    lookResult = checkTransparent(position, newRow+1, newColumn-1, viewHeight, -1, sightMap)
    downLeftClear, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

    if downLeftClear: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newRow > 0):
            shadows += [[newRow-1, newColumn]]
            if newColumn < 11: shadows += [[newRow-1, newColumn+1]]            
        
        # if checkTransparent(position, newRow+1, newColumn, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = 1, -1
        Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)
        
        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookUpRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)  
        else: sightMap[newRow-1][newColumn] = Visibility.unseen


def fillThirdOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 2, column - 1
    lookResult = []

    lookResult = checkTransparent(position, newRow+1, newColumn+1, viewHeight, -1, sightMap)
    notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

    if notBlocked: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newRow > 0):
            shadows += [[newRow-1, newColumn]]
            if newColumn > 0: shadows += [[newRow-1, newColumn-1]]

        # if checkTransparent(position, newRow+1, newColumn, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = 1, 1
        Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookUpLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)
        else: sightMap[newRow-1][newColumn] = Visibility.unseen 


def fillForthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column - 2
    lookResult = []

    lookResult = checkTransparent(position, newRow+1, newColumn+1, viewHeight, -1, sightMap)
    notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

    if notBlocked: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newRow > 0):
            shadows += [[newRow, newColumn-1]]
            if newColumn > 0: shadows += [[newRow-1, newColumn-1]]

        # if checkTransparent(position, newRow, newColumn+1, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = 1, 1
        Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)
        
        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookUpLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
        else: sightMap[newRow][newColumn-1] = Visibility.unseen


def fillFifthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column - 2
    lookResult = []

    lookResult = checkTransparent(position, newRow-1, newColumn+1, -1, viewHeight, sightMap)
    notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

    if notBlocked: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newColumn > 0):
            shadows += [[newRow, newColumn-1]]
            if newRow < 11: shadows += [[newRow+1, newColumn-1]]
            
        # if checkTransparent(position, newRow, newColumn+1, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = -1, 1
        Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookDownLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
        else: sightMap[newRow][newColumn-1] = Visibility.unseen


def fillSixthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 2, column - 1
    lookResult = []
    
    lookResult = checkTransparent(position, newRow-1, newColumn+1, -1, viewHeight, sightMap)

    notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]
    if notBlocked: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newRow < 11):
            shadows += [[newRow+1, newColumn]]
            if newColumn > 0: shadows += [[newRow+1, newColumn-1]]

        # if checkTransparent(position, newRow-1, newColumn, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = -1, 1
        Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookDownLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)
        else: sightMap[newRow+1][newColumn] = Visibility.unseen


    # fix this
def fillSeventhOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 2, column + 1
    lookResult = []

    lookResult = checkTransparent(position, newRow-1, newColumn-1, viewHeight, -1, sightMap)

    notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]
    if notBlocked: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newRow < 11):
            shadows += [[newRow+1, newColumn]]
            if newColumn < 11: shadows += [[newRow+1, newColumn+1]]

        # if checkTransparent(position, newRow-1, newColumn, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = -1, -1
        Visibility.lookLeft(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookDownRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)
        else: sightMap[newRow+1][newColumn] = Visibility.unseen


def fillEighthOctant(rank, position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column + 2
    lookResult = []

    lookResult = checkTransparent(position, newRow-1, newColumn-1, viewHeight, -1, sightMap)

    notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]
    if notBlocked: 
        sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
        if applyShadow and (newColumn < 11):
            shadows += [[newRow, newColumn+1]]
            if newRow < 11: shadows += [[newRow+1, newColumn+1]]

        # if checkTransparent(position, newRow, newColumn-1, viewHeight, sightMap)[0]:
        rowOffset, columnOffset = -1, -1
        Visibility.lookRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

        if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
            Visibility.lookDownRight(rank, position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
        else: sightMap[newRow][newColumn+1] = Visibility.unseen