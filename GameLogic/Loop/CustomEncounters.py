from Systems import PlayerSelect as Select
from Campaigns.Benediction import CustomMaps as B_Maps
from Campaigns.Avarice import CustomMaps as A_Maps
from . import Encounters

def getElement(inventory) -> str:
    choice = Select.pickOption(inventory, "Shard")
    inventory.remove(choice)
    return choice


def customLoop(playerGroup, biome, event) -> bool:
    encounter, skipCombat, timePermits, deathPermitted = None, False, True, False

    Select.readScene(event, playerGroup["campaign"])

    match playerGroup["campaign"]:
        case "Avarice":
            match event:
                case "Escape":
                    skipCombat = True
                    playerGroup["world"].worldMap[14][7] = "w/!!↑"
                case "Threshold": skipCombat = True
                case "Moose": skipCombat = True
                case "Vines":
                    skipCombat = True
                    playerGroup["world"].marker.pos = [1, 6]
                    playerGroup["world"].worldMap[1][6], playerGroup["world"].worldMap[1][7] = "D_..|", "D/!!↑"
                case "Worm":
                    playerGroup["world"].worldMap[14][7] = "w___↑"
                    encounter = A_Maps.glacierMap(playerGroup["members"])
                case "Giant":
                    playerGroup["world"].worldMap[16][7] = "K_**↑"
                    encounter = A_Maps.woodsMap(playerGroup["members"])
                case "Strider":
                    playerGroup["world"].worldMap[15][8] = "w___↑"
                    encounter = A_Maps.volcanoMap(playerGroup["members"])
                case "Breakout":
                    skipCombat = True
                    letter = getElement(playerGroup["inventory"])[0]
                    playerGroup["world"].marker.pos = [17, 7]
                    playerGroup["world"].worldMap[17][7], playerGroup["world"].worldMap[16][7] = "s_..↓", letter + "!//↑"
                case "Camp":
                    playerGroup["world"].worldMap[18][11] = "u_..↑"
                    encounter = A_Maps.campMap(playerGroup["members"])
                case "Port":
                    element = getElement(playerGroup["inventory"])
                    playerGroup["world"].marker.pos = [16, 8]
                    playerGroup["world"].worldMap[20][4], playerGroup["world"].worldMap[21][4] = letter + "!//↑"

                    encounter = A_Maps.portMap(playerGroup["members"], element)

        case "Benediction":
            match event:
                case "Leviathan":
                    encounter = B_Maps.shipMap(playerGroup["members"])
                    timePermits, deathPermitted = False, True
                    playerGroup["world"].marker.pos = [5, 9]
                    playerGroup["world"].worldMap[5][9], playerGroup["world"].worldMap[7][11] = "s_..↓", "~~~~⇓"
                case "Village":
                    encounter = B_Maps.villageMap(playerGroup["members"])
                    playerGroup["world"].worldMap[3][10], playerGroup["world"].worldMap[3][9], playerGroup["world"].worldMap[5][8] = "s___↓", "s___↓", "s___↓"
                case "Town":
                    encounter = B_Maps.townMap(playerGroup["members"])
                    playerGroup["world"].worldMap[1][4], playerGroup["world"].worldMap[6][7] = "r___↑", "d___↓"
                case "Ally": skipCombat = True
                case "Valley": skipCombat = True
                case "Lich":
                    encounter = B_Maps.cryptMap(playerGroup["members"], playerGroup["events"])
                case "Raft":
                    skipCombat = True
                    playerGroup["world"].marker.pos = [13, 2]
                    playerGroup["world"].worldMap[10][3], playerGroup["world"].worldMap[13][2] = "s___↓", "s_..↓"
                case "Dragon":
                    skipCombat = True
                    playerGroup["world"].marker.pos = [1, 6]
                    playerGroup["world"].worldMap[1][10], playerGroup["world"].worldMap[0][11] = "M_..↓", "M/!!↓"
                case "Finale":
                    encounter = B_Maps.manorMap(playerGroup["members"])

    if skipCombat: return True
    else:
        result = Encounters.encounterLoop(playerGroup, [encounter[0], encounter[1]], encounter[2], biome, timePermits)
        if result or deathPermitted: Select.readScene("Post " + event, playerGroup["campaign"])
        return result or deathPermitted