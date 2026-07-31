from Systems import PlayerSelect as Select, Conditions, Commitments
from GameState import SaveLoad as Save
from Biomes import Biomes
from Campaigns.Benediction import CustomMaps as B_Maps, Journal as B_Journal
from Campaigns.Avarice import CustomMaps as A_Maps, Journal as A_Journal
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat
from collections import deque


def customLoop(playerGroup, biome, event) -> bool:
    encounter, skipCombat, timePermits = None, False, True

    match playerGroup["campaign"]:
        case "Avarice":
            match event:
                case "Beginning":
                    skipCombat = True
                    playerGroup["world"].worldMap[14][7] = "w/!!↑"
                    if Select.yesNo("Read 'Escape' journal entry?"):
                        Select.conversationPrint(A_Journal.scenes["Escape"])
                case "Threshold":
                    skipCombat = True
                    if Select.yesNo("Read 'Threshold' journal entry?"):
                        Select.conversationPrint(A_Journal.scenes["Threshold"])
                case "Moose":
                    skipCombat = True
                    if Select.yesNo("Read 'Moose' journal entry?"):
                        Select.conversationPrint(A_Journal.scenes["Moose"])
                case "Vines":
                    skipCombat = True
                    playerGroup["world"].marker.pos = [1, 6]
                    playerGroup["world"].worldMap[1][6], playerGroup["world"].worldMap[1][7] = "D_..|", "D/!!↑"
                case "Worm":
                    playerGroup["world"].worldMap[14][7] = "w___↑"
                    if Select.yesNo("Read 'Stillness' journal entry?"):
                        Select.conversationPrint(A_Journal.scenes["Stillness"])
                    encounter = A_Maps.glacierMap()
                case "Giant":
                    playerGroup["world"].worldMap[16][7] = "K___↑"
                    if Select.yesNo("Read 'Tracks' journal entry?"):
                        Select.conversationPrint(A_Journal.scenes["Tracks"])
                    encounter = A_Maps.woodsMap()
                case "Strider":
                    playerGroup["world"].worldMap[15][8] = "w___↑"
                    encounter = A_Maps.volcanoMap()
                    if Select.yesNo("Read 'Close' journal entry?"):
                        Select.conversationPrint(A_Journal.scenes["Close"])
                case "Breakout":
                    playerGroup["world"].marker.pos = [16, 8]
                    playerGroup["world"].worldMap[16][8], playerGroup["world"].worldMap[15][8] = "s_..↓", "w/!!↑"
                    encounter = A_Maps.fortMap()                    
                case "Rescue":
                    encounter = A_Maps.campMap(playerGroup)                    
                    if Select.yesNo("Read 'Vines' journal entry?"):
                        Select.conversationPrint(A_Journal.scenes["Rescue"])
                # case "Port": encounter = A_Maps.

        case "Benediction":
            match event:
                case "Leviathan":
                    encounter = B_Maps.shipMap(playerGroup["members"])
                    timePermits = False
                    playerGroup["world"].marker.pos = [5, 9]
                    playerGroup["world"].worldMap[5][9], playerGroup["world"].worldMap[7][11] = "s_..↓", "~~~~⇓"
                case "Village":
                    encounter = B_Maps.villageMap(playerGroup["members"])
                    playerGroup["world"].worldMap[3][10], playerGroup["world"].worldMap[3][9], playerGroup["world"].worldMap[5][8] = "s___↓", "s___↓", "s___↓"
                    if Select.yesNo("Read 'Shipwrecked' journal entry?"):
                        Select.conversationPrint(B_Journal.scenes["Shipwrecked"])
                case "Town":
                    encounter = B_Maps.townMap()
                    playerGroup["world"].worldMap[6][7] = "d___↓"
                case "Lich":
                    if Select.yesNo("Read 'Ziggurat' journal entry?"):
                        Select.conversationPrint(B_Journal.scenes["Ziggurat"])
                    encounter = B_Maps.cryptMap(playerGroup["members"])
                case "Dragon":
                    skipCombat = True
                    playerGroup["world"].marker.pos = [1, 6]
                    playerGroup["world"].worldMap[1][10], playerGroup["world"].worldMap[0][11] = "M_..↓", "M/!!↓"
                    if Select.yesNo("Read 'Dragon' journal entry?"):
                        Select.conversationPrint(B_Journal.scenes["Dragon"])
                case "Vampire":
                    encounter = B_Maps.manorMap()
        

    if skipCombat: return True
    else:
        result = encounterLoop(playerGroup, [encounter[0], encounter[1]], encounter[2], biome, timePermits)
        if result:
            match event:
                case "Breakout":
                    if Select.yesNo("Read 'Breakout' journal entry?"): Select.conversationPrint(A_Journal.scenes["Breakout"])
                case "Village":
                    if Select.yesNo("Read 'Village' journal entry?"): Select.conversationPrint(B_Journal.scenes["Village"])
                case "Town":
                    if Select.yesNo("Read 'Town' journal entry?"): Select.conversationPrint(B_Journal.scenes["Town"])
                case "Ziggurat":
                    if Select.yesNo("Read 'Victory' journal entry?"): Select.conversationPrint(B_Journal.scenes["Victory"])

        return result


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