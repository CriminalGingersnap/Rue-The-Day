from . import Map_Populate as pMap, Elevation
from Systems import PlayerSelect as Select
import random

wall, pit, emptySpace, manaWell = "////|", ")()(|", "____|", "*___|"
fogSpace, mistSpace = "=___|", "-___|"
smokeSpace, rimeSpace, toxicSpace = "#___|", "%___|", "&___|"
dazzleSpace, deathSpace, sacredSpace = "+___|", "}___|", "@___|"


def combineMaps(mainMap, secondMap, mainHeight, playerGroup) -> list:
    battleMap = [[], [], [], [], [], [], [], [], [], [], [], []]

    insertRow = random.randint(0, 8)

    for row in range(insertRow):
        battleMap[row] += secondMap[row]
    for row in range(mainHeight):
        battleMap[row + insertRow] += mainMap[row]
    for row in range(insertRow + mainHeight, 12):
        battleMap[row] += secondMap[row - mainHeight]

    for fighter in playerGroup:
        fighter.position[0] += insertRow
            
    return battleMap


def createMap(playerGroup, enemyGroup, tileMods, environment, slope) -> list:    
    box = [emptySpace]
    mainMap = [[], [], []]
    secondMap = [[], [], [], [], [], [], [], [], []]

    for column in range(12):
        for row in range(3): mainMap[row] += box
        for row in range(9): secondMap[row] += box

    Select.waitPrint("Placing occlusions...")
    placeOcclusions(tileMods, mainMap, 1)
    placeOcclusions(tileMods, secondMap, 3)
    
    Select.waitPrint("Placing PCs...")
    for fighter in playerGroup: pMap.firstPlacement(mainMap, fighter, 3)
    battleMap = combineMaps(mainMap, secondMap, 3, playerGroup)

    Select.waitPrint("Adjusting elevation and atmosphere...")
    Elevation.setElevation(battleMap, environment, slope)
    Select.waitPrint("Placing NPCs...")
    for enemy in enemyGroup: pMap.firstPlacement(battleMap, enemy, 12)

    return battleMap


def placeOcclusions(tileMods, instanceMap, thirdHeight):
    obstacles, occlusions = tileMods[0], tileMods[1]
    topIndex = (thirdHeight * 3) - 1

    for i in range(obstacles["wall"] * thirdHeight):
        available = False
        while not available: available = pMap.placeObstruction(instanceMap, wall, topIndex)

    for i in range(obstacles["pit"] * thirdHeight):
        available = False
        while not available: available = pMap.placeObstruction(instanceMap, pit, topIndex)

    for i in range(obstacles["trap"] * thirdHeight):
        available = False
        while not available: available = pMap.placeTrap(instanceMap, topIndex)

    for atmo in occlusions:
        for i in range(occlusions[atmo] * thirdHeight):
            available = False
            while not available: available = pMap.placeFog(instanceMap, atmo, topIndex)