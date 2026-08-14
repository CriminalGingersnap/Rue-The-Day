from . import Map_Populate as pMap, Elevation, MovementOptions as mOpts
from Systems import PlayerSelect as Select
import random

wall, pool, pit, fateWell =  "////|", "_~~~|", "_)))|", "_***|"
impermissible = [wall, pit]

emptySpace = "____|"
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
    placeOcclusions(mapConditions, mainMap, 4)
    placeOcclusions(mapConditions, secondMap, 4)
    placeOcclusions(mapConditions, thirdMap, 4)

    Select.waitPrint("Placing PCs...")
    for fighter in playerGroup: pMap.firstPlacement(mainMap, 4, fighter)
    Select.quickPrint("Placing Group 1 NPCs...")
    for fighter in enemyGroups[0]: pMap.firstPlacement(secondMap, 4, fighter)
    Select.quickPrint("Placing Group 2 NPCs...")
    for fighter in enemyGroups[1]: pMap.firstPlacement(thirdMap, 4, fighter)
    
    battleMap = combineMaps(mainMap, secondMap, thirdMap, playerGroup, enemyGroups)

    Select.waitPrint("Adjusting elevation and atmosphere...")
    Elevation.setElevation(battleMap, environment, mapConditions["slope"])
    updateFighterHeight(playerGroup + enemyGroups[0] + enemyGroups[1], battleMap)

    Select.waitPrint("Placing fate well...")
    pMap.placeObstruction(battleMap, fateWell, 1, 12)

    return battleMap


def placeOcclusions(mapConditions, instanceMap, mapHeight=12):
    obstacles, occlusions = mapConditions["obstructions"], mapConditions["atmosphere"]

    pMap.placeObstruction(instanceMap, wall, obstacles["wall"], mapHeight)
    pMap.placeObstruction(instanceMap, pit, obstacles["pit"], mapHeight)
    pMap.placeTrap(instanceMap, obstacles["trap"], mapHeight)
            
    for atmo in occlusions: pMap.placeFog(instanceMap, atmo, occlusions[atmo], mapHeight)


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