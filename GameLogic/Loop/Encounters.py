from Systems import PlayerSelect as Select, Commitments
from GameState import SaveLoad as Save
from Biomes import Biomes
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat, Loot, CustomEncounters
from collections import deque


def randomLoop(playerGroup, biome) -> bool:
    players = playerGroup["members"]
    ace = playerGroup["world"].ace

    mapConditions = Environment.randomEnvironment(ace, biome)
    enemyGroups = Biomes.setFoes(biome, mapConditions["budget"], mapConditions["luck"])

    battleMap = None
    if (mapConditions["slope"] == "ruin") or (biome in ["Kingdom Fort", "Rot Locus"]):
        battleMap = dMap.createMap(players, enemyGroups, mapConditions, ace)
    else: battleMap = iMap.createMap(players, enemyGroups, mapConditions, ace)

    return encounterLoop(playerGroup, enemyGroups, battleMap, biome, mapConditions["atmosphere"])


def encounterLoop(playerGroup, enemyGroups, battleMap, biome, atmosphere, timePermits = True) -> bool:
    players = playerGroup["members"]    

    result = Combat.engage(players, enemyGroups, battleMap, atmosphere)
    playerVictory = result[0]

    if playerVictory:
        if timePermits: Loot.searchAll(playerGroup, result[1])
        takeRest = handleAftermath(players)
        if takeRest: playerVictory = rest(playerGroup, biome)

    if not playerVictory: 
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

    if not takeRest:
        takeRest = Select.yesNo("Rest?")
        if not takeRest:
            for fighter in victorGroup:
                fighter.atrb["corruption"] = max(fighter.atrb["corruption"] - 1, 0)
                fighter.atrb["fatigue"] = min(fighter.atrb["fatigue"], 1)
                fighter.atrb["injury"] = max(fighter.atrb["injury"] - 1, 0)

    return takeRest


def rest(group, biome) -> bool:
    for fighter in group["members"]: refresh(fighter)
    world = group["world"]

    group["days"] += 1
    world.marker.lastCleared = deque([world.marker.pos,[],[],[],[],[],[]])
    world.ace = Environment.updateAce(world.ace, biome)

    if group["days"] == 1: Select.waitPrint("First day completed.")
    else: Select.waitPrint(str(group["days"]) + " days completed.")
    achievable = True

    match group["campaign"]:
        case "Avarice":
            consequence, warning, allowance = "", "", 35
            if group["doubleDays"]: allowance *= 2
            if world.events["Camp"]["complete"]:
                remaining = (allowance + 10) - group["days"]
                consequence = "the duke escapes."
            else:
                remaining = allowance - group["days"]
                consequence = "Willem's execution."

            if remaining == 1: warning = str(remaining) + " day remains before " + consequence
            elif remaining > 1: warning = str(remaining) + " days remain before " + consequence
            else: warning, achievable = "Mission failed.", False
            
            Select.conversationPrint(warning + "\n")

        case "Benediction": Select.conversationPrint("Disturbed dreams warn of a creeping evil.\n")

    Save.saveGroup(group)
    CustomEncounters.readJournal(group, world)

    return achievable
        

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