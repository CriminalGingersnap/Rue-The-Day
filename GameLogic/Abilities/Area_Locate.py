from Systems import PlayerSelect as Select
from Maps import Movement, Map_Instantiate as iMap, Map_Print as Print
from Actions import AttackActions as Attacks
import random



def findSpace(fighter, groups, range, source) -> list:
    column, row = fighter.pos[1], fighter.pos[0]
    leftEdge, rightEdge = max(0, (column - range)), min(11, (column + range))
    topEdge, bottomEdge = max(0, (row - range)), min(11, (row + range))

    markedSpace = selectSpace(fighter, groups, source, leftEdge, rightEdge, topEdge, bottomEdge)
    return markedSpace


def selectSpace(fighter, groups, source, leftEdge, rightEdge, topEdge, bottomEdge) -> int:
    enemies, allies = groups["fightingEnemies"], groups["fightingAllies"]
    sightMap = fighter.sightMap

    if (leftEdge == rightEdge) and (topEdge == bottomEdge): return [leftEdge, topEdge]
    else:
        optionsMap = [[], [], [], [], [], [], [], [], [], [], [], []]
        for row in range(12):
            for column in range(12):
                optionsMap[row] += [sightMap[row][column]]

                if optionsMap[row][column][2] in iMap.intStrings: 
                    optionsMap[row][column] = optionsMap[row][column][:2] + "!!" + optionsMap[row][column][-1]

        counter, optionDict = 0, {"0": "None"}
        
        blockers = ["?", "/", ")"]
        if source in ["echo", "standard", "Slip"]: blockers += [".", "!", "e", "s"]
        if source == "standard": blockers += ["~"]

        for column in range(leftEdge, rightEdge+1):
            for row in range(topEdge, bottomEdge+1):
                if not any(blocker in optionsMap[row][column] for blocker in blockers):
                    if fighter.props["rank"] == "player":
                        optionDict[str(counter)] = [row, column]
                        setSpace(sightMap, optionsMap, row, column, counter)
                    elif source == "Slip":
                        optionDict[str(counter)] = [row, column, 0]
                        setSpace(sightMap, optionsMap, row, column, counter)
                    elif enemyInRange(row, column, enemies) and ((source == "echo") or allyNotInRange(row, column, allies)):
                        optionDict[str(counter)] = [row, column]
                        setSpace(sightMap, optionsMap, row, column, counter)                    

        choice = ""
        if fighter.props["rank"] == "player":
            Print.printOptionsMap(optionsMap, "Options Map")
            choice = Select.takeInput(0, counter)
        elif len(optionDict) > 1:
            if source == "Slip":
                target = Attacks.npcSelectAttackTarget(fighter, groups["fightingEnemies"], True)
                choice = Movement.moveNPC(fighter, target, optionDict, 1, counter, False)
            else: choice = random.randint(1, counter)
        else: choice = 0

        return optionDict[str(choice)]


def enemyInRange(row, column, enemies) -> bool:
    inRange = False
    for enemy in enemies:
        if Movement.getSpaceDistance(enemy.pos[0], row, enemy.pos[1], column) <= 3: 
            inRange = True

    return inRange

def allyNotInRange(row, column, allies):
    notInRange = True
    for ally in allies:
        if Movement.getSpaceDistance(ally.pos[0], row, ally.pos[1], column) <= 3: 
            notInRange = False

    return notInRange


def setSpace(sightMap, optionsMap, row, column, counter) -> None:
    atmosphere = sightMap[row][column][0]
    marker = sightMap[row][column][1]
    elevation = sightMap[row][column][-1]

    if any(playerMark in optionsMap[row][column] for playerMark in [".", "e", "s"]): marker = "."
    elif "!" in optionsMap[row][column]: marker = "!"

    filler = ""
    if counter < 10: filler = "_"
    
    optionsMap[row][column] = atmosphere + marker + str(counter) + filler + elevation
    counter += 1