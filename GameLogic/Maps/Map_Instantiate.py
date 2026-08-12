from . import Map_Populate as pMap, Elevation, MovementOptions as mOpts
from Systems import PlayerSelect as Select
import random

wall, pool, pit =  "////|", "_~~~|", "_)))|"
impermissible = [wall, pit]

emptySpace = "____|"
fogSpace, mistSpace = "=___|", "-___|"
dazzleSpace, deathSpace, sacredSpace = "@___|", "}___|", "+___|"
noxiousSpace, rimeSpace, smokeSpace = "&___|", "%___|", "#___|"

intStrings = ["0","1","2","3","4","5","6","7","8","9"]


def combineMaps(mainMap, secondMap, thirdMap, playerGroup, enemyGroups) -> list:
    battleMap = [[], [], [], [], [], [], [], [], [], [], [], []]

    mapGroups = [
        {"map": mainMap, "group": playerGroup},
        {"map": secondMap, "group": enemyGroups[0]},
        {"map": thirdMap, "group": enemyGroups[1]}
    ]
    random.shuffle(mapGroups)
    map1, map2, map3 = mapGroups[0]["map"], mapGroups[1]["map"], mapGroups[2]["map"]

    for row in range(4): battleMap[row] += map1[row]
    for row in range(4, 8): battleMap[row] += map2[row - 4]
    for row in range(8, 12): battleMap[row] += map3[row - 8]

    for fighter in mapGroups[1]["group"]: fighter.pos[0] += 4
    for fighter in mapGroups[2]["group"]: fighter.pos[0] += 8
            
    return battleMap


def createMap(playerGroup, enemyGroups, mapConditions, environment) -> list:    
    box = [emptySpace]
    mainMap, secondMap, thirdMap = [[], [], [], []], [[], [], [], []], [[], [], [], [], []]

    for column in range(12):
        for row in range(4):
            mainMap[row] += box
            secondMap[row] += box
            thirdMap[row] += box
    
    Select.waitPrint("\nPlacing obstructions and occlusions...")
    placeOcclusions(mapConditions, mainMap, 1)
    placeOcclusions(mapConditions, secondMap, 1)
    placeOcclusions(mapConditions, thirdMap, 1)

    Select.waitPrint("Placing PCs...")
    for fighter in playerGroup: pMap.firstPlacement(mainMap, 4, fighter)
    Select.quickPrint("Placing Group 1 NPCs...")
    for fighter in enemyGroups[0]: pMap.firstPlacement(secondMap, 4, fighter)
    Select.quickPrint("Placing Group 2 NPCs...")
    for fighter in enemyGroups[1]: pMap.firstPlacement(thirdMap, 4, fighter)
    
    battleMap = combineMaps(mainMap, secondMap, thirdMap, playerGroup, enemyGroups)

    Select.waitPrint("Adjusting elevation and atmosphere...")
    Elevation.setElevation(battleMap, environment, mapConditions["slope"])
    updateFighterHeight(playerGroup + enemyGroups, battleMap)

    return battleMap


def placeOcclusions(mapConditions, instanceMap, multiplier):
    obstacles, occlusions = mapConditions["obstructions"], mapConditions["atmosphere"]

    for i in range(obstacles["wall"] * multiplier):
        available = False
        while not available: available = pMap.placeObstruction(instanceMap, wall, multiplier)

    for i in range(obstacles["pit"] * multiplier):
        available = False
        while not available: available = pMap.placeObstruction(instanceMap, pit, multiplier)

    for i in range(obstacles["trap"] * multiplier):
        available = False
        while not available: available = pMap.placeTrap(instanceMap)

    for atmo in occlusions:
        for i in range(occlusions[atmo] * multiplier):
            available = False
            while not available: available = pMap.placeFog(instanceMap, atmo)


def updateFighterHeight(group, battleMap) -> None:
    waterLine = 0
    for column in range(12):
        for row in range(12):
            wetSpace = battleMap[row][column]
            if "~" in wetSpace: waterLine = max(waterLine, (mOpts.heightDict[wetSpace[-1]] + 1))
    
    for fighter in group:
        space = battleMap[fighter.pos[0]][fighter.pos[1]]
        fighter.pos[2] = mOpts.heightDict[space[-1]]
        
        if fighter.cndt["winged"]: fighter.pos[2] += 1
        elif(battleMap[row][column][1] == "~"):
            fighter.pos[2] = waterLine
            fighter.cndt["submerged"] = True
        else: fighter.cndt["submerged"] = False