from Systems import PlayerSelect as Select
from Campaigns.Benediction import CustomMaps as B_Maps, Journal as B_Journal
from Campaigns.Avarice import CustomMaps as A_Maps, Journal as A_Journal
from . import Encounters

def getElement(inventory) -> str:
    choice = Select.pickOption(inventory, "Shard")
    inventory.remove(choice)
    return choice


def customLoop(playerGroup, biome, event) -> bool:
    encounter, skipCombat, timePermits, deathPermitted = None, False, True, False
    worldMap, marker = playerGroup["world"].worldMap, playerGroup["world"].marker

    Select.readScene(event, playerGroup["campaign"])

    match playerGroup["campaign"]:
        case "Avarice":
            match event:
                case "Escape":
                    worldMap[14][7] = "w/!!↑"
                    encounter = A_Maps.archerMap(playerGroup["members"])
                case "Threshold": skipCombat = True
                case "Moose": skipCombat = True
                case "Vines":
                    skipCombat = True
                    marker.pos = [1, 6, 3]
                    worldMap[1][6], worldMap[1][7] = "D_..|", "D/!!↑"
                case "Worm":
                    worldMap[1][11] = "I_..⇑"
                    worldMap[14][7] = "w___↑"
                    encounter = A_Maps.glacierMap(playerGroup["members"])
                case "Giant":
                    worldMap[0][5] = "D_..|"
                    worldMap[16][7] = "K***↑"
                    encounter = A_Maps.woodsMap(playerGroup["members"])
                case "Strider":
                    worldMap[7][1] = "F_..⇑"
                    worldMap[15][8] = "w___↑"
                    encounter = A_Maps.volcanoMap(playerGroup["members"])
                case "Breakout":
                    skipCombat = True
                    letter = getElement(playerGroup["inventory"])[0]
                    marker.pos = [17, 7, 1]
                    worldMap[17][7], worldMap[16][7] = "s_..↓", letter + "/!!↑"
                case "Camp":
                    worldMap[18][11] = "o_..↑"
                    worldMap[21][4] = "K***↑"
                    encounter = A_Maps.campMap(playerGroup["members"])
                case "Port":
                    element = getElement(playerGroup["inventory"])
                    worldMap[21][4] = letter + "_..↑"
                    encounter = A_Maps.portMap(playerGroup["members"], element)

        case "Benediction":
            match event:
                case "Leviathan":
                    encounter = B_Maps.shipMap(playerGroup["members"])
                    timePermits, deathPermitted = False, True
                    marker.pos = [5, 9, 1]
                    worldMap[5][9], worldMap[7][11] = "s_..↓", "~~~~⇓"
                case "Village":
                    encounter = B_Maps.villageMap(playerGroup["members"])
                    worldMap[4][9],worldMap[3][10], worldMap[3][9], worldMap[5][8] = "r_..↓", "s___↓", "s___↓", "s___↓"
                case "Town":
                    worldMap[0][5], worldMap[1][0], worldMap[1][4], worldMap[6][7] = "R_..↑", "R***⇓", "r___↑", "d___↓"
                    encounter = B_Maps.townMap(playerGroup["members"])
                case "Ally": skipCombat = True
                case "Valley": skipCombat = True
                case "Lich":
                    worldMap[1][0] = "R_..⇓"
                    worldMap[10][3] = "s***↓"
                    encounter = B_Maps.cryptMap(playerGroup["members"], playerGroup["events"], playerGroup["days"])
                case "Raft":
                    skipCombat = True
                    marker.pos = [13, 2, 1]
                    worldMap[10][3], worldMap[13][2] = "s___↓", "s_..↓"
                case "Dragon":
                    skipCombat = True
                    marker.pos = [1, 6, 1]
                    worldMap[1][10], worldMap[0][11] = "M_..↓", "M/!!↓"
                case "Finale":
                    worldMap[11][11] = "I_..⇑"
                    encounter = B_Maps.manorMap(playerGroup["members"], playerGroup["days"])

    if skipCombat: return True
    else:
        result = Encounters.encounterLoop(playerGroup, [encounter[0], encounter[1]], encounter[2], biome, encounter[3], timePermits)
        if result or deathPermitted:
            Select.readScene("Post " + event, playerGroup["campaign"])
            if event == "Leviathan":
                playerGroup["members"][0].equip["weapon"] = {"name": "Rag", "twoHanded": False, "modifier": 0, "dmgTypes": ["Dream"], "reach": 8}
                playerGroup["members"][1].equip["weapon"] = {"name": "Plank", "twoHanded": True, "modifier": 0, "dmgTypes": ["Crush"], "reach": 2}
                playerGroup["members"][0].equip["shield"] = {"name": "None", "modifier": 0,  "element": "Basic"}
                playerGroup["members"][1].equip["shield"] = {"name": "None", "modifier": 0,  "element": "Basic"}

        return result or deathPermitted


def readJournal(group, world) -> None:
    entries = ["None"]
    for eventOption in world.events:
        if world.events[eventOption]["complete"]:
            entries += [eventOption]
            if "Post " + eventOption in A_Journal.scenes | B_Journal.scenes: entries += ["Post" + eventOption]

    if (len(entries) > 1) and Select.yesNo("Reread a prior journal entry?"):
        entry = Select.pickOption(entries, " journal entry")
        if entry != "None": Select.readScene(entry, group["campaign"], True)