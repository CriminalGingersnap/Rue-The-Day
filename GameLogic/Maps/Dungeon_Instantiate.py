from . import Map_Instantiate as iMap, Map_Populate as pMap, Elevation, Map_Update
import random


def narrowHallway(cell, direction):
    line = random.randint(0, 3)
    if direction == "horizontal":
        for row in range(4):
            if row != line:
                for column in range(4): cell[row][column] = iMap.wall
    else:
        for row in range(4):
            for column in range(4):
                if column != line: cell[row][column] = iMap.wall

def blockedCell(cell):
    for row in range(4):
        for column in range(4): cell[row][column] = iMap.wall

def wall(cell, direction):
    line = random.randint(0, 3)
    if direction == "horizontal":
        for column in range(4): cell[line][column] = iMap.wall
    else:
        for row in range(4): cell[row][line] = iMap.wall


def setCell(isStarter) -> list:
    cellType = random.choice(["Blocked", "Blocked", "Hallway"])
    direction = random.choice(["horizontal", "vertical"])

    if isStarter: cellType, direction = random.choice(["Wall", "Hallway"]), "horizontal"
    cell, box = [[], [], [], []], [iMap.emptySpace]

    for column in range(4):
        for row in range(4): cell[column] += box

    match cellType:
        case "Blocked": blockedCell(cell)
        case "Hallway": narrowHallway(cell, direction)
        case "Wall": wall(cell, direction)

    return cell


def fixCorners(battleMap):
    for row in range(12):
        for column in range(1, 11):
            if ("/" in battleMap[row][column]) and not ("/" in battleMap[row][column + 1]):
                approach = random.choice(["Open", "Close"])
                square = random.choice(["same", "other"])

                if row > 0:
                    up = "/" in battleMap[row - 1][column]
                    upRight = "/" in battleMap[row - 1][column + 1]

                    if upRight and not up:
                        if approach == "Open":
                            if square == "same": battleMap[row][column] = iMap.emptySpace
                            else: battleMap[row - 1][column + 1] = iMap.emptySpace
                        elif square == "same": battleMap[row][column + 1] = iMap.wall
                        else: battleMap[row - 1][column] = iMap.wall

                if row < 5:
                    down = "/" in battleMap[row + 1][column]
                    downRight = "/" in battleMap[row + 1][column + 1]
                    
                    if downRight and not down:
                        if approach == "Open":
                            if square == "same": battleMap[row][column] = iMap.emptySpace
                            else: battleMap[row + 1][column + 1] = iMap.emptySpace
                        elif square == "same": battleMap[row][column + 1] = iMap.wall
                        else: battleMap[row + 1][column] = iMap.wall
                

def carveTunnels(battleMap):
    for column in range(11):
        for row in range(11):
            reverseColumn, reverseRow = 11 - column, 11 - row

            current = "/" not in battleMap[row][column]
            right = "/" not in battleMap[row][column + 1]
            down = "/" not in battleMap[row + 1][column]
            if current and not (right or down):
                if random.choice(["Down", "Right"]) == "Down":
                    battleMap[row + 1][column] = iMap.emptySpace
                else: battleMap[row][column + 1] = iMap.emptySpace

            current = "/" not in battleMap[reverseRow][reverseColumn]
            left = "/" not in battleMap[reverseRow][reverseColumn - 1]
            up = "/" not in battleMap[reverseRow - 1][reverseColumn]
            if current and not (left or up):
                if random.choice(["Up", "Left"]) == "Up":
                    battleMap[reverseRow - 1][reverseColumn] = iMap.emptySpace
                else: battleMap[reverseRow][reverseColumn - 1] = iMap.emptySpace
        
            current = "/" not in battleMap[reverseRow][column]
            up = "/" not in battleMap[reverseRow - 1][column]
            right = "/" not in battleMap[reverseRow][column + 1]
            if current and not (right or up):
                if random.choice(["Up", "Right"]) == "Up":
                    battleMap[reverseRow - 1][column] = iMap.emptySpace
                else: battleMap[reverseRow][column + 1] = iMap.emptySpace

            current = "/" not in battleMap[row][reverseColumn]
            left = "/" not in battleMap[row][reverseColumn - 1]
            down = "/" not in battleMap[row + 1][reverseColumn]
            if current and not (left or down):
                if random.choice(["Down", "Left"]) == "Down":
                    battleMap[row + 1][reverseColumn] = iMap.emptySpace
                else: battleMap[row][reverseColumn - 1] = iMap.emptySpace                
    

def setColumns(mainMap, secondMap):
    isStarter = True

    for columnBlock in range(3):
        cell1 = setCell(isStarter)
        for row in range(4): mainMap[row] += cell1[row]
        if isStarter: isStarter = False

        for rowBlock in range(2):
            start = 4 * rowBlock
            cell2 = setCell(False)
            for row in range(4): secondMap[row + start] += cell2[row]


def createMap(playerGroup, enemyGroup, atmoList, feature) -> list:
    mainMap = [[], [], [], []]
    secondMap = [[], [], [], [], [], [], [], []]
    setColumns(mainMap, secondMap)

    # iMap.placeOcclusions(atmoList, mainMap, 1)
    # iMap.placeOcclusions(atmoList, secondMap, 3)
    
    for fighter in playerGroup: pMap.firstPlacement(mainMap, fighter, 4)
    battleMap = iMap.combineMaps(mainMap, secondMap, 4, playerGroup)

    # for i in range(2):
    fixCorners(battleMap)
    carveTunnels(battleMap)
    fixCorners(battleMap)

        
    for enemy in enemyGroup: pMap.firstPlacement(battleMap, enemy, 12)
    
    return battleMap