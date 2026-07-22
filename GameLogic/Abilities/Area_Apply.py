def setAtmosphere(atmosphere, row, column, battleMap):
    if "////" not in battleMap[row][column]:
        battleMap[row][column] = atmosphere + battleMap[row][column][1:]

def getAtmosphere(scale, dmgType) -> str:
    atmosphere, big, little, lingering = "_", "", "", "_"

    match dmgType:
        case "Bleed": big, little, lingering = "B", "b", "="
        case "Crush": big, little = "C", "c"
        case "Dream": big, little, lingering = "D", "d", "@"
        case "Flame": big, little, lingering = "F", "f", "#"
        case "Ice": big, little, lingering = "I", "i", "%"
        case "Holy": big, little, lingering = "H", "h", "+"
        case "Pierce": big, little = "P", "p"
        case "Rot": big, little, lingering = "R", "r", "}"
        case "Toxic": big, little = "T", "t"

    match scale:
        case 1: atmosphere = lingering
        case 2: atmosphere = little
        case 3: atmosphere = big

    return atmosphere


def spreadAtmosphere(atmosphere, coverage, tossRow, tossColumn, battleMap) -> None:
    upRow, downRow = tossRow - 1, tossRow + 1
    leftColumn, rightColumn = tossColumn - 1, tossColumn + 1
    spaces = []

    for step in range(coverage - 1):
        spaces += addSpaces(tossRow, upRow, downRow, tossColumn, leftColumn, rightColumn)
        upRow -= 1
        downRow += 1
        leftColumn -= 1
        rightColumn += 1

    for space in spaces: setAtmosphere(atmosphere, space[0], space[1], battleMap)


def addSpaces(tossRow, upRow, downRow, tossColumn, leftColumn, rightColumn):
    newSpaces = []

    if upRow >= 0:
        newSpaces += [[upRow, tossColumn]]
        if leftColumn >= 0: newSpaces += [[upRow, leftColumn]]
        if rightColumn <= 11: newSpaces += [[upRow, rightColumn]]
    if downRow <= 11:
        newSpaces += [[downRow, tossColumn]]
        if leftColumn >= 0: newSpaces += [[downRow, leftColumn]]
        if rightColumn <= 11: newSpaces += [[downRow, rightColumn]]
        downRow += 1
    if leftColumn >= 0:
        newSpaces += [[tossRow, leftColumn]]
        leftColumn -= 1
    if rightColumn <= 11:
        newSpaces += [[tossRow, rightColumn]]
        rightColumn += 1

    return newSpaces