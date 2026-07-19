from Systems import PlayerSelect as Select
from Maps import Movement, Map_Instantiate as iMap, Map_Print as Print
import random



def findSpace(fighter, groups, range) -> list:
    column, row = fighter.position[1], fighter.position[0]
    leftEdge, rightEdge = max(0, (column - range)), min(11, (column + range))
    topEdge, bottomEdge = max(0, (row - range)), min(11, (row + range))
    borders = [leftEdge, rightEdge, topEdge, bottomEdge]

    markedSpace = selectSpace(fighter, groups, borders)
    return markedSpace


def selectSpace(fighter, groups, boarders) -> int:
    enemies, allies = groups["fightingEnemies"], groups["fightingAllies"]
    sightMap = fighter.sightMap
    leftEdge, rightEdge, topEdge, bottomEdge = boarders[0], boarders[1], boarders[2], boarders[3]

    if (leftEdge == rightEdge) and (topEdge == bottomEdge): return [leftEdge, topEdge]
    else:
        optionsMap = [[], [], [], [], [], [], [], [], [], [], [], []]
        for row in range(12):
            for column in range(12):
                optionsMap[row] += [sightMap[row][column]]

                if optionsMap[row][column][2] in iMap.intStrings: 
                    optionsMap[row][column] = optionsMap[row][column][:2] + "!!" + optionsMap[row][column][-1]

        counter, optionDict = 1, {}

        for column in range(leftEdge, rightEdge+1):
            for row in range(topEdge, bottomEdge+1):
                if not any(blocker in optionsMap[row][column] for blocker in ["?", "/"]):
                    if fighter.props["rank"] == "player": optionDict[str(counter)] = [row, column]
                    elif enemyCanSee(row, column, enemies) and allyNotInRange(row, column, allies):
                        optionDict[str(counter)] = [row, column]

                    atmosphere = sightMap[row][column][0]
                    marker = sightMap[row][column][1]
                    elevation = sightMap[row][column][-1]

                    if "." in optionsMap[row][column]: marker = "."
                    elif "!" in optionsMap[row][column]: marker = "!"

                    filler = ""
                    if counter < 10: filler = "_"
                    
                    optionsMap[row][column] = atmosphere + marker + str(counter) + filler + elevation
                    counter += 1

        choice = ""
        if fighter.props["rank"] == "player":
            Print.printOptionsMap(optionsMap, "Options Map")
            choice = Select.takeInput(1, counter)
        elif len(optionsMap) > 0: choice = random.randint(1, counter)

        return optionDict[str(choice)]


def enemyCanSee(row, column, enemies) -> bool:
    enemySees = False
    for enemy in enemies:
        enemySpace = enemy.sightMap[row][column]
        if "?" != enemySpace[-1]: enemySees = True

    return enemySees

def allyNotInRange(row, column, allies):
    notInRange = True
    for ally in allies:
        if Movement.getSpaceDistance(ally.position[0], row, ally.position[1], column) <= 3: 
            notInRange = False

    return notInRange