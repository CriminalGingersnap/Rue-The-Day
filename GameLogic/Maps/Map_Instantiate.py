from . import Map_Populate as pMap, Elevation
from Systems import PlayerSelect as Select
import random

wall, pool, pit =  "////|", "_~~~|", ")()(|"
impermissible = [wall, pit]

emptySpace, manaWell = "____|", "*___|"
fogSpace, mistSpace = "=___|", "-___|"
smokeSpace, rimeSpace, toxinSpace = "#___|", "%___|", "&___|"
dazzleSpace, deathSpace, sacredSpace = "+___|", "}___|", "@___|"


def combineMaps(mainMap, secondMap, thirdMap, playerGroup, enemyGroups) -> list:
    battleMap = [[], [], [], [], [], [], [], [], [], [], [], []]

    mapGroup1 = {"map": mainMap, "group": playerGroup}
    mapGroup2 = {"map": secondMap, "group": enemyGroups[0]}
    mapGroup3 = {"map": thirdMap, "group": enemyGroups[1]}
    mapGroupOrder = random.shuffle([mapGroup1, mapGroup2, mapGroup3])

    for row in range(4):
        map1 = mapGroupOrder[0]["map"]
        battleMap[row] += map1[row]
    for row in range(4, 8):
        map2 = mapGroupOrder[1]["map"]
        battleMap[row] += map2[row - 4]
        for fighter in mapGroupOrder[1]["group"]: fighter.position[0] += 4
    for row in range(8, 12):
        map3 = mapGroupOrder[2]["map"]
        battleMap[row] += map3[row - 8]
        for fighter in mapGroupOrder[2]["group"]: fighter.position[0] += 8
            
    return battleMap


def createMap(playerGroup, enemyGroups, tileMods, environment) -> list:    
    box = [emptySpace]
    mainMap, secondMap, thirdMap = [[], [], [], []], [[], [], [], []], [[], [], [], [], []]

    for column in range(12):
        for row in range(4):
            mainMap[row] += box
            secondMap[row] += box
            thirdMap[row] += box
    
    Select.waitPrint("Placing PCs...")
    for fighter in playerGroup: pMap.firstPlacement(mainMap, fighter)
    Select.waitPrint("Placing Group 1 NPCs...")
    for fighter in enemyGroups[0]: pMap.firstPlacement(secondMap, fighter)
    Select.waitPrint("Placing Group 2 NPCs...")
    for fighter in enemyGroups[1]: pMap.firstPlacement(thirdMap, fighter)
    
    battleMap = combineMaps(mainMap, secondMap, thirdMap, playerGroup, enemyGroups)

    Select.waitPrint("Placing occlusions...")
    placeOcclusions(tileMods, battleMap, 3)

    Select.waitPrint("Adjusting elevation and atmosphere...")
    Elevation.setElevation(battleMap, environment, tileMods[2])

    return battleMap


def placeOcclusions(tileMods, instanceMap, multiplier):
    obstacles, occlusions = tileMods[0], tileMods[1]

    for i in range(obstacles["wall"] * multiplier):
        available = False
        while not available: available = pMap.placeObstruction(instanceMap, wall)

    for i in range(obstacles["pit"] * multiplier):
        available = False
        while not available: available = pMap.placeObstruction(instanceMap, pit)

    for i in range(obstacles["trap"] * multiplier):
        available = False
        while not available: available = pMap.placeTrap(instanceMap)

    for atmo in occlusions:
        for i in range(occlusions[atmo] * multiplier):
            available = False
            while not available: available = pMap.placeFog(instanceMap, atmo)