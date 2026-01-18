from . import Map_Instantiate as iMap
import random

up, down = "\u2191", "\u2193"
doubleUp, doubleDown = "\u21d1", "\u21d3"
middle = "|"


def setElevation(battleMap, environment, slope):
    playerRow = 0
    for row in range(12):
        for column in range(2):
            if "." in battleMap[row][column]:
                playerRow = row

    if slope == "random":
        options = ["right"]
        if playerRow < 4: options += ["down"]
        elif playerRow < 8: options += ["ud"]
        else: options += ["up"]
        if environment["Hearts"] != "King": options += ["left", "lr"]

        slope = random.choice(options)

    match slope:
        case "right": slopeLeftRight(battleMap, "right")
        case "left": slopeLeftRight(battleMap, "left")
        case "lr": slopeLeftRight(battleMap, "sides")
        case "up": slopeDownUp(battleMap, "up")
        case "down": slopeDownUp(battleMap, "down")
        case "ud": slopeDownUp(battleMap, "sides")
        # case "small craters": bumps(battleMap, "down")
        # case "small hills": bumps(battleMap, "up")
        # case "tunnels":  tunnels(battleMap) # set all obstruction heights to max
    adjustObstructionHeight(battleMap)
    adjustEnvironment(battleMap, environment)


def resetLtRtElv(lean):
    if lean == "right":
        randomLeft = random.choice([doubleUp, up, middle])
        randomRight = random.choice([doubleDown, down, middle])
        randomMiddle = random.choice([randomRight, randomLeft, middle])
    elif lean == "left":
        randomLeft = random.choice([doubleDown, down, middle])
        randomRight = random.choice([doubleUp, up, middle])
        randomMiddle = random.choice([randomRight, randomLeft, middle])
    else:
        randomMiddle = random.choice([doubleUp, up, middle])
        randomLeft = random.choice([randomMiddle, doubleDown, down, middle])
        randomRight = random.choice([randomMiddle, doubleDown, down, middle])
    
    return [randomLeft, randomMiddle, randomRight]

def slopeLeftRight(battleMap, lean):
    elv = resetLtRtElv(lean)
    randomLeft, randomMiddle, randomRight = elv[0], elv[1], elv[2]

    firstEndRow = random.randint(3, 6)
    thirdStartRow = random.randint(6, 9)

    for row in range(12):
        if row in [firstEndRow, thirdStartRow]:
            elv = resetLtRtElv(lean)
            randomLeft, randomMiddle, randomRight = elv[0], elv[1], elv[2]

        firstEndCol = random.randint(2, 5)
        thirdStartCol = random.randint(7, 10)

        for column in range(0, firstEndCol):
            battleMap[row][column] = battleMap[row][column][:-1] + randomLeft
        for column in range(firstEndCol, thirdStartCol):
            battleMap[row][column] = battleMap[row][column][:-1] + randomMiddle
        for column in range(thirdStartCol, 12):
            battleMap[row][column] = battleMap[row][column][:-1] + randomRight
        
    for column in range(12):
        for row in range(11):
            selfElevation = battleMap[row][column][-1]
            downElevation = battleMap[row+1][column][-1]

            if selfElevation != downElevation:
                if random.choice([True, False]):
                    battleMap[row][column] = battleMap[row][column][:-1] + downElevation
                else:
                    battleMap[row+1][column] = battleMap[row+1][column][:-1] + selfElevation


def resetUpDnElv(lean):
    if lean == "up":
        randomTop = random.choice([doubleDown, down, middle])
        randomBottom = random.choice([doubleUp, up, middle])
        randomMiddle = random.choice([randomTop, randomBottom, middle])
    elif lean == "down":
        randomTop = random.choice([doubleUp, up, middle])
        randomBottom = random.choice([doubleDown, down, middle])
        randomMiddle = random.choice([randomTop, randomBottom, middle])
    else:
        randomMiddle = random.choice([doubleUp, up, middle])
        randomTop = random.choice([randomMiddle, doubleDown, down, middle])
        randomBottom = random.choice([randomMiddle, doubleDown, down, middle])

    return [randomTop, randomMiddle, randomBottom]

def slopeDownUp(battleMap, lean):
    elv = resetUpDnElv(lean)
    randomTop, randomMiddle, randomBottom = elv[0], elv[1], elv[2]

    firstEndCol = random.randint(3, 6)
    thirdStartCol = random.randint(6, 9)

    for column in range(12):
        if column in [firstEndCol, thirdStartCol]:
            elv = resetUpDnElv(lean)
            randomTop, randomMiddle, randomBottom = elv[0], elv[1], elv[2]
        
        firstEndRow = random.randint(2, 5)
        thirdStartRow = random.randint(7, 10)

        for row in range(0, firstEndRow):
            battleMap[row][column] = battleMap[row][column][:-1] + randomTop
        for row in range(firstEndRow, thirdStartRow):
            battleMap[row][column] = battleMap[row][column][:-1] + randomMiddle
        for row in range(thirdStartRow, 6):
            battleMap[row][column] = battleMap[row][column][:-1] + randomBottom

    for column in range(11):
        for row in range(12):
            selfElevation = battleMap[row][column][-1]
            rightElevation = battleMap[row][column+1][-1]

            if selfElevation != rightElevation:
                if random.choice([True, False]):
                    battleMap[row][column] = battleMap[row][column][:-1] + rightElevation
                else:
                    battleMap[row][column+1] = battleMap[row][column+1][:-1] + selfElevation


def adjustObstructionHeight(battleMap):
    for row in range(12):
        for column in range(12):
            if "/" in battleMap[row][column]:
                elevation = battleMap[row][column][-1]
                if elevation == doubleDown: elevation = random.choice([doubleDown, down, middle, up, doubleUp])
                elif elevation == down: elevation = random.choice([down, middle, up, doubleUp])
                elif elevation == middle: elevation = random.choice([middle, up, doubleUp])
                elif elevation == up: elevation = random.choice([up, doubleUp])
                battleMap[row][column] = battleMap[row][column][:-1] + elevation


def adjustEnvironment(battleMap, environment):
    match environment["Hearts"]:
        case "King":
            for row in range(12):
                for column in range(12):
                    spreadPits(battleMap, row, column, 2)

        case "Queen":
            for row in range(12):
                for column in range(12):
                    if "/" not in battleMap[row][column]:
                        spreadPits(battleMap, row, column, 1)
                        if down in battleMap[row][column]:
                            battleMap[row][column] = "=" + battleMap[row][column][1:]
                        if middle in battleMap[row][column]:
                            battleMap[row][column] = "-" + battleMap[row][column][1:]
                    
        case "Jack":
            for row in range(12):
                for column in range(12):
                    if doubleUp in battleMap[row][column]:
                        if battleMap[row][column][0] in ["-", "="]:
                            battleMap[row][column] = "_" + battleMap[row][column][1:]

                    elif up in battleMap[row][column]:
                        if battleMap[row][column][0] == "=":
                            battleMap[row][column] = "-" + battleMap[row][column][1:]
                        elif battleMap[row][column][0] == "-":
                            battleMap[row][column] = "_" + battleMap[row][column][1:]


def spreadPits(battleMap, row, column, severity):
    if any(downer in battleMap[row][column] for downer in [doubleDown, down]):
        if "." in battleMap[row][column]:
            battleMap[row][column] = battleMap[row][column][:-1] + middle
        elif doubleDown in battleMap[row][column]: 
            battleMap[row][column] = iMap.pit[:-1] + doubleDown

        elif ("/" not in battleMap[row][column]) and (severity == 2) and (down in battleMap[row][column]):
            battleMap[row][column] = iMap.pit[:-1] + doubleDown