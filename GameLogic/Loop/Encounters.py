from Systems import PlayerSelect as Select, Conditions, Commitments
from GameState import SaveLoad as Save
from Biomes import Biomes
from Campaigns.Benediction import CustomMaps as B_Maps, Journal as B_Journal
from Campaigns.Metamorphosis import CustomMaps as M_Maps, Journal as M_Journal
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat
from collections import deque


def customLoop(playerGroup, biome, event) -> bool:
    encounter, timePermits = None, True

    match playerGroup["campaign"]:
        case "Benediction":
            match event:
                case "Leviathan":
                    encounter = B_Maps.shipMap(playerGroup["members"])
                    timePermits = False
                    playerGroup["world"].marker.pos = [5, 9]
                    playerGroup["world"].worldMap[5][9], playerGroup["world"].worldMap[7][11] = "s_..↓", "~~~~⇓"
                case "Village":
                    encounter = B_Maps.villageMap(playerGroup["members"])
                    playerGroup["world"].worldMap[3][10], playerGroup["world"].worldMap[3][9] = "s___↓" ,"s___↓"
                    playerGroup["world"].worldMap[3][8], playerGroup["world"].worldMap[5][8] = "d___↓", "d___↓"
                    if Select.yesNo("Read 'Shipwrecked' journal entry?"):
                        Select.conversationPrint(B_Journal.scenes["Shipwrecked"])
                case "Town":
                    encounter = B_Maps.townMap()
                    playerGroup["world"].worldMap[6][7] = "d___↓"
                    if Select.yesNo("Read '' journal entry?"):
                        Select.conversationPrint(B_Journal.scenes["Shipwrecked"])
                case "Lich":
                    encounter = B_Maps.cryptMap(playerGroup["members"])
                case "Vampire":
                    encounter = B_Maps.manorMap()
        # case "Metamorphosis":
        #     match event:
                # case "Giant": encounter = M_Maps.
                # case "Strider": encounter = M_Maps.
                # case "Worm": encounter = M_Maps.
                # case "Prison": encounter = M_Maps.
                # case "King": encounter = M_Maps.

    return encounterLoop(playerGroup, [encounter[0], encounter[1]], encounter[2], biome, timePermits)


def randomLoop(playerGroup, biome) -> bool:
    players = playerGroup["members"]
    ace = playerGroup["world"].ace

    mapConditions = Environment.randomEnvironment(biome)
    enemyGroups = Biomes.setFoes(biome, mapConditions["budget"], mapConditions["luck"])

    battleMap = None
    if (mapConditions["slope"] == "ruin") or (biome == "Kingdom Fort"):
        battleMap = dMap.createMap(players, enemyGroups, mapConditions, ace)
    else: battleMap = iMap.createMap(players, enemyGroups, mapConditions, ace)

    return encounterLoop(playerGroup, enemyGroups, battleMap, biome)


def encounterLoop(playerGroup, enemyGroups, battleMap, biome, timePermits = True) -> bool:
    players = playerGroup["members"]    

    playerVictory = Combat.engage(players, enemyGroups, battleMap, timePermits)
    if playerVictory:
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
            elif fighter.atrb["corruption"] >=  Conditions.getTolerance(fighter):
                Select.waitPrint(fighter.props["name"] + " collapses from sickness!")
                takeRest = True

    if not takeRest: takeRest = Select.yesNo("Rest?")
    return takeRest


def rest(group, biome) -> None:
    for fighter in group["members"]: refresh(fighter)

    group["days"] += 1
    group["world"].marker.lastCleared = deque([group["world"].marker.pos,[],[],[],[],[],[]])
    group["world"].ace = Environment.updateAce(group["world"].ace, biome)

    Save.saveGroup(group)

def refresh(fighter) -> None:
    fighter.atrb["stamina"] = fighter.atrb["endurance"]
    fighter.atrb["fatigue"] = 0

    fighter.atrb["tolerance"] = Conditions.getTolerance(fighter)
    fighter.atrb["corruption"] = 0

    fighter.dead = False
    fighter.atrb["cur_hp"] = fighter.atrb["base_hp"]
    fighter.atrb["injury"] = 0

    if ("echo" in fighter.inv) and (fighter.inv["echo"] != "None"): refresh(fighter.inv["echo"])
    if ("standard" in fighter.inv) and (fighter.inv["standard"] != "None"): refresh(fighter.inv["standard"])