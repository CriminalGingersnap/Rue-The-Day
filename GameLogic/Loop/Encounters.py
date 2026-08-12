from Systems import PlayerSelect as Select, Commitments
from GameState import SaveLoad as Save
from Biomes import Biomes
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat, Loot, CustomEncounters
from collections import deque


def randomLoop(playerGroup, biome) -> bool:
    players = playerGroup["members"]
    ace = playerGroup["world"].ace

    mapConditions = Environment.randomEnvironment(biome)
    enemyGroups = Biomes.setFoes(biome, mapConditions["budget"], mapConditions["luck"])

    battleMap = None
    if (mapConditions["slope"] == "ruin") or (biome in ["Kingdom Fort", "Rot Locus"]):
        battleMap = dMap.createMap(players, enemyGroups, mapConditions, ace)
    else: battleMap = iMap.createMap(players, enemyGroups, mapConditions, ace)

    return encounterLoop(playerGroup, enemyGroups, battleMap, biome)


def encounterLoop(playerGroup, enemyGroups, battleMap, biome, timePermits = True) -> bool:
    players = playerGroup["members"]    

    result = Combat.engage(players, enemyGroups, battleMap)
    playerVictory = result[0]

    if playerVictory:
        if timePermits: Loot.searchAll(playerGroup, result[1])
        takeRest = handleAftermath(players)
        if takeRest: rest(playerGroup, biome)
    else: 
        Select.waitPrint("Reload a save or start a new game to continue.")
        playerGroup = Save.loadGroup(playerGroup["campaign"])

    return playerVictory


def handleAftermath(victorGroup) -> bool:
    takeRest = False

    for fighter in victorGroup:
        if fighter.props["rank"] != "player": victorGroup.remove(fighter)

        else:
            Commitments.clearCommitments(fighter)
            
            if fighter.atrb["cur_hp"] <= 0:
                Select.waitPrint(fighter.props["name"] + " requires immediate resuscitation!")
                takeRest = True
            elif fighter.atrb["fatigue"] >=  fighter.atrb["endurance"]:
                Select.waitPrint(fighter.props["name"] + " collapses from exhaustion!")
                takeRest = True
            elif fighter.atrb["corruption"] >=  fighter.atrb["endurance"]:
                Select.waitPrint(fighter.props["name"] + " collapses from sickness!")
                takeRest = True

    if not takeRest: takeRest = Select.yesNo("Rest?")
    return takeRest


def rest(group, biome) -> None:
    for fighter in group["members"]: refresh(fighter)
    world = group["world"]

    group["days"] += 1
    world.marker.lastCleared = deque([world.marker.pos,[],[],[],[],[],[]])
    world.ace = Environment.updateAce(world.ace, biome)

    Select.waitPrint(str(group["days"]) + " days completed.")
    Select.waitPrint(str(35 - group["days"]) + " days remain.")

    Save.saveGroup(group)
    CustomEncounters.readJournal(group, world)
        

def refresh(fighter) -> None:
    fighter.atrb["stamina"] = fighter.atrb["endurance"]
    fighter.atrb["fatigue"] = 0

    fighter.atrb["tolerance"] = fighter.atrb["endurance"]
    fighter.atrb["corruption"] = 0

    fighter.dead = False
    fighter.atrb["cur_hp"] = fighter.atrb["base_hp"]
    fighter.atrb["injury"] = 0

    if ("echo" in fighter.inv) and (fighter.inv["echo"] != "None"): refresh(fighter.inv["echo"])
    if ("standard" in fighter.inv) and (fighter.inv["standard"] != "None"): refresh(fighter.inv["standard"])