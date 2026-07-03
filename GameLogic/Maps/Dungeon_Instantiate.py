from . import Map_Instantiate as iMap, Map_Populate as pMap, Elevation, Map_Update
from Systems import PlayerSelect as Select
import random


def createMap(playerGroup, enemyGroups, mapConditions, environment) -> list:
    mainMap, secondMap, thirdMap = [[], [], [], []], [[], [], [], []], [[], [], [], [], []]

    Select.waitPrint("Creating rooms...")
    setColumns([mainMap, secondMap, thirdMap])
    
    Select.waitPrint("Placing PCs...")
    for fighter in playerGroup: pMap.firstPlacement(mainMap, fighter)
    Select.waitPrint("Placing Group 1 NPCs...")
    for fighter in enemyGroups[0]: pMap.firstPlacement(secondMap, fighter)
    Select.waitPrint("Placing Group 2 NPCs...")
    for fighter in enemyGroups[1]: pMap.firstPlacement(thirdMap, fighter)

    battleMap = iMap.combineMaps(mainMap, secondMap, thirdMap, playerGroup, enemyGroups)

    Select.waitPrint("Adjusting rooms...")
    carveTunnels(battleMap)
    fixCorners(battleMap)
    
    Select.waitPrint("Placing occlusions...")
    iMap.placeOcclusions(mapConditions, battleMap, 1)
         
    Select.waitPrint("Adjusting elevation and atmosphere...")
    Elevation.setElevation(battleMap, environment, "flat")
   
    return battleMap


def setColumns(maps):
    forceHallway = [True, False, False]

    for map in maps:
        for columnBlock in range(3):
            cell = setCell(forceHallway[columnBlock])
            for row in range(4): map[row] += cell[row]
        forceHallway = [False, False, True]


def setCell(forceHallway) -> list:
    cellType = random.choice(["Blocked", "Blocked", "Hallway"])
    direction = random.choice(["startTop", "startBottom"])
    if forceHallway: cellType = "Hallway"

    cell = [[], [], [], []]
    for column in range(4):
        for row in range(4): cell[column] += [iMap.emptySpace]

    match cellType:
        case "Blocked": blockedCell(cell)
        case "Hallway": hallway(cell, direction)

    return cell


def hallway(cell, direction):
    seq1, seq2 = [0, 0, 1], [0, 1, 0]
    seq3, seq4 = [3, 3, 2], [3, 2, 3]

    rowList1, colList1 = [], []
    rowList2, colList2 = [], []

    match direction:
        case "startBottom":
            rowList1, colList1 = seq1, seq2
            rowList2, colList2 = seq3, seq4
        case "startTop":
            rowList1, colList1 = seq2, seq3
            rowList2, colList2 = seq4, seq1

    rowList = rowList1 + rowList2
    colList = colList1 + colList2

    for i in range(6):
        row, column = rowList[i], colList[i]
        cell[row][column] = iMap.wall


def blockedCell(cell):
    for row in range(4):
        for column in range(4): cell[row][column] = iMap.wall


def fixCorners(battleMap):
    for row in range(12):
        for column in range(1, 11):
            selfClosed = "/" in battleMap[row][column]
            rightOpen = "/" not in battleMap[row][column + 1]

            if selfClosed and rightOpen:
                approach = random.choice(["Open", "Close"])
                targetRow = random.choice(["Own", "Other"])

                if row > 0:
                    upOpen = "/" not in battleMap[row - 1][column]
                    upRightClosed = "/" in battleMap[row - 1][column + 1]

                    if upRightClosed and upOpen:
                        if approach == "Open":
                            if targetRow == "Own": battleMap[row][column] = iMap.emptySpace
                            else: battleMap[row - 1][column + 1] = iMap.emptySpace
                        elif targetRow == "Own": battleMap[row][column + 1] = iMap.wall
                        else: battleMap[row - 1][column] = iMap.wall

                if row < 5:
                    downOpen = "/" not in battleMap[row + 1][column]
                    downRightClosed = "/" in battleMap[row + 1][column + 1]
                    
                    if downRightClosed and downOpen:
                        if approach == "Open":
                            if targetRow == "Own": battleMap[row][column] = iMap.emptySpace
                            else: battleMap[row + 1][column + 1] = iMap.emptySpace
                        elif targetRow == "Own": battleMap[row][column + 1] = iMap.wall
                        else: battleMap[row + 1][column] = iMap.wall
                

def carveTunnels(battleMap):
    for column in range(11):
        for row in range(11):
            reverseColumn, reverseRow = 11 - column, 11 - row

            currentFree = "/" not in battleMap[row][column]
            rightFree = "/" not in battleMap[row][column + 1]
            downFree = "/" not in battleMap[row + 1][column]
            if currentFree and not (rightFree or downFree):
                if random.choice(["Down", "Right"]) == "Down":
                    battleMap[row + 1][column] = iMap.emptySpace
                else: battleMap[row][column + 1] = iMap.emptySpace

            currentFree = "/" not in battleMap[reverseRow][reverseColumn]
            leftFree = "/" not in battleMap[reverseRow][reverseColumn - 1]
            up = "/" not in battleMap[reverseRow - 1][reverseColumn]
            if currentFree and not (leftFree or up):
                if random.choice(["Up", "Left"]) == "Up":
                    battleMap[reverseRow - 1][reverseColumn] = iMap.emptySpace
                else: battleMap[reverseRow][reverseColumn - 1] = iMap.emptySpace
        
            currentFree = "/" not in battleMap[reverseRow][column]
            up = "/" not in battleMap[reverseRow - 1][column]
            rightFree = "/" not in battleMap[reverseRow][column + 1]
            if currentFree and not (rightFree or up):
                if random.choice(["Up", "Right"]) == "Up":
                    battleMap[reverseRow - 1][column] = iMap.emptySpace
                else: battleMap[reverseRow][column + 1] = iMap.emptySpace

            currentFree = "/" not in battleMap[row][reverseColumn]
            leftFree = "/" not in battleMap[row][reverseColumn - 1]
            downFree = "/" not in battleMap[row + 1][reverseColumn]
            if currentFree and not (leftFree or downFree):
                if random.choice(["Down", "Left"]) == "Down":
                    battleMap[row + 1][reverseColumn] = iMap.emptySpace
                else: battleMap[row][reverseColumn - 1] = iMap.emptySpace