
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


def fillVisibilityMap(position, row, column, viewHeight, battleMap, sightMap, shadows):
    if (row > 0) and (column < 10):
        fillFirstOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row > 1) and (column < 11):
        fillSecondOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row > 1) and (column > 0):
        fillThirdOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row > 0) and (column > 1):
        fillForthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 11) and (column > 1):
        fillFifthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 10) and (column > 0):
        fillSixthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 10) and (column < 11):
        fillSeventhOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)
    if (row < 11) and (column < 10):
        fillEighthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows)


def fillFirstOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column + 2
    lookResult = []

    while (newRow >= 0) and (newColumn <= 11):
        lookResult = checkTransparent(position, newRow+1, newColumn-1, viewHeight, -1, sightMap)
        downLeftClear, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

        if downLeftClear: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newColumn < 11):
                shadows += [[newRow, newColumn+1]]
                if newRow > 0: shadows += [[newRow-1, newColumn+1]]

            # if checkTransparent(position, newRow, newColumn-1, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = 1, -1
            Visibility.lookRight(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak) 

            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookUpRight(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
            else: sightMap[newRow][newColumn+1] = Visibility.unseen

        newRow -= 1
        newColumn += 2


def fillSecondOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 2, column + 1
    lookResult = []
    
    while (newRow >= 0) and (newColumn <= 11):
        lookResult = checkTransparent(position, newRow+1, newColumn-1, viewHeight, -1, sightMap)
        downLeftClear, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

        if downLeftClear: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newRow > 0):
                shadows += [[newRow-1, newColumn]]
                if newColumn < 11: shadows += [[newRow-1, newColumn+1]]            
            
            # if checkTransparent(position, newRow+1, newColumn, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = 1, -1
            Visibility.lookUp(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)
            
            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookUpRight(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)  
            else: sightMap[newRow-1][newColumn] = Visibility.unseen

        newRow -= 2
        newColumn += 1


def fillThirdOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 2, column - 1
    lookResult = []

    while (newRow >= 0) and (newColumn >= 0):
        lookResult = checkTransparent(position, newRow+1, newColumn+1, viewHeight, -1, sightMap)
        notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

        if notBlocked: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newRow > 0):
                shadows += [[newRow-1, newColumn]]
                if newColumn > 0: shadows += [[newRow-1, newColumn-1]]

            # if checkTransparent(position, newRow+1, newColumn, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = 1, 1
            Visibility.lookUp(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookUpLeft(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)
            else: sightMap[newRow-1][newColumn] = Visibility.unseen 

        newRow -= 2
        newColumn -= 1


def fillForthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row - 1, column - 2
    lookResult = []

    while (newRow >= 0) and (newColumn >= 0):
        lookResult = checkTransparent(position, newRow+1, newColumn+1, viewHeight, -1, sightMap)
        notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

        if notBlocked: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newRow > 0):
                shadows += [[newRow, newColumn-1]]
                if newColumn > 0: shadows += [[newRow-1, newColumn-1]]

            # if checkTransparent(position, newRow, newColumn+1, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = 1, 1
            Visibility.lookLeft(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)
            
            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookUpLeft(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
            else: sightMap[newRow][newColumn-1] = Visibility.unseen

        newRow -= 1
        newColumn -= 2


def fillFifthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column - 2
    lookResult = []

    while (newRow <= 11) and (newColumn >= 0):
        lookResult = checkTransparent(position, newRow-1, newColumn+1, -1, viewHeight, sightMap)
        notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]

        if notBlocked: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newColumn > 0):
                shadows += [[newRow, newColumn-1]]
                if newRow < 11: shadows += [[newRow+1, newColumn-1]]
                
            # if checkTransparent(position, newRow, newColumn+1, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = -1, 1
            Visibility.lookLeft(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookDownLeft(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
            else: sightMap[newRow][newColumn-1] = Visibility.unseen

        newRow += 1
        newColumn -= 2


def fillSixthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 2, column - 1
    lookResult = []
    
    while (newRow <= 11) and (newColumn >= 0):
        lookResult = checkTransparent(position, newRow-1, newColumn+1, -1, viewHeight, sightMap)

        notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]
        if notBlocked: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newRow < 11):
                shadows += [[newRow+1, newColumn]]
                if newColumn > 0: shadows += [[newRow+1, newColumn-1]]

            # if checkTransparent(position, newRow-1, newColumn, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = -1, 1
            Visibility.lookDown(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookDownLeft(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)
            else: sightMap[newRow+1][newColumn] = Visibility.unseen

        newRow += 2
        newColumn -= 1

    # fix this
def fillSeventhOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 2, column + 1
    lookResult = []

    while (newRow <= 11) and (newColumn <= 11):
        lookResult = checkTransparent(position, newRow-1, newColumn-1, viewHeight, -1, sightMap)

        notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]
        if notBlocked: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newRow < 11):
                shadows += [[newRow+1, newColumn]]
                if newColumn < 11: shadows += [[newRow+1, newColumn+1]]

            # if checkTransparent(position, newRow-1, newColumn, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = -1, -1
            Visibility.lookDown(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookDownRight(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, 0, obstructionPeak)
            else: sightMap[newRow+1][newColumn] = Visibility.unseen

        newRow += 2
        newColumn += 1


def fillEighthOctant(position, row, column, viewHeight, battleMap, sightMap, shadows):
    newRow, newColumn = row + 1, column + 2
    lookResult = []

    while (newRow <= 11) and (newColumn <= 11):
        lookResult = checkTransparent(position, newRow-1, newColumn-1, viewHeight, -1, sightMap)

        notBlocked, applyShadow, obstructionPeak = lookResult[0], lookResult[1], lookResult[2]
        if notBlocked: 
            sightMap[newRow][newColumn] = battleMap[newRow][newColumn]
            if applyShadow and (newColumn < 11):
                shadows += [[newRow, newColumn+1]]
                if newRow < 11: shadows += [[newRow+1, newColumn+1]]

            # if checkTransparent(position, newRow, newColumn-1, viewHeight, sightMap)[0]:
            rowOffset, columnOffset = -1, -1
            Visibility.lookRight(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, rowOffset, columnOffset, obstructionPeak)

            if checkTransparent(position, newRow, newColumn, viewHeight, obstructionPeak, sightMap)[0]:
                Visibility.lookDownRight(position, newRow, newColumn, viewHeight, battleMap, sightMap, shadows, 0, columnOffset, obstructionPeak)
            else: sightMap[newRow][newColumn+1] = Visibility.unseen

        newRow += 1
        newColumn += 2