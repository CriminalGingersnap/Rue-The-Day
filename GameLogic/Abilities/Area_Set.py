from Systems import PlayerSelect as Select, Roll
from . import Area_Locate as Locate, Area_Apply as Apply
from Maps import Map_Update as uMap

areaAbilities = ["Bless", "Breath", "Screen", "Shroud", "Slip"]


def execute(fighter, dice, groups, ability, battleMap) -> str:
    article, phrase, range = "a", fighter.props["name"], 8
    if fighter.atrb["cur_elm"][0] in ["A", "E", "I", "O", "U"]: article = "an "

    match ability:
        case "Breath":
            phrase += " exhales " + fighter.atrb["cur_elm"] + " breath"
            range = 1
            if fighter.cndt["massive"]: range = 2
        case "Bless": phrase += " blesses the ground!"
        case "Screen": phrase += " raises " + article + fighter.atrb["cur_elm"] + " screen!"
        case "Shroud": phrase += " emanates " + article + fighter.atrb["cur_elm"] + " shroud!"
        case "Slip": phrase += " slips between spaces! Rolling range."

    Select.waitPrint(phrase)
    markedSpace, fighterRow, fighterColumn = [0, 0], fighter.pos[0], fighter.pos[1]

    if ability in ["Bless", "Shroud"]: markedSpace = [fighterRow, fighterColumn]
    else:
        if ability == "Slip": range = Roll.roll(fighter, fighter, fighter.atrb["base_mag"], "Slip", "magic") + 1
        markedSpace = Locate.findSpace(fighter, groups, range, ability)

    if markedSpace == "None": Select.waitPrint(fighter.props["name"] + " dispels an area ability before execution.")
    else:
        match ability:
            case "Bless" | "Shroud":
                scale = min(1, dice // 2)
                affectSpace(markedSpace, fighter.atrb["cur_elm"], scale, battleMap)
                if ability == "Shroud": battleMap[fighterRow][fighterColumn] = "_" + battleMap[fighterRow][fighterColumn][1:]
            case "Breath":
                nextSpace = markedSpace
                for spaceNum in range(dice):
                    affectSpace(nextSpace, fighter.atrb["cur_elm"], 1, battleMap)
                    nextSpace = getNextSpace(nextSpace, fighterRow, fighterColumn)
            case "Screen":
                leastAtmosphere = Apply.getAtmosphere(1, fighter.atrb["cur_elm"])
                Apply.spreadAtmosphere(leastAtmosphere, dice, markedSpace[0], markedSpace[1], battleMap)
            case "Slip":
                tossRow, tossColumn = markedSpace[0], markedSpace[1]
                uMap.updatePlacement(battleMap, fighter.sightMap, tossRow, tossColumn, fighter)


def affectSpace(markSpace, dmgType, scale, battleMap) -> None:
    effectRow, effectColumn = markSpace[0], markSpace[1]

    atmosphere = Apply.getAtmosphere(scale, dmgType)
    lesserAtmosphere = Apply.getAtmosphere(scale-1, dmgType)
    leastAtmosphere = Apply.getAtmosphere(1, dmgType)

    battleMap[effectRow][effectColumn] = atmosphere + battleMap[effectRow][effectColumn][1:]
    Apply.spreadAtmosphere(leastAtmosphere, scale+1, effectRow, effectColumn, battleMap)
    Apply.spreadAtmosphere(lesserAtmosphere, scale, effectRow, effectColumn, battleMap)

def getNextSpace(markedSpace, fighterRow, fighterColumn) -> list:
    nextSpace = markedSpace[:]

    if 0 < markedSpace[0] < fighterRow: nextSpace[0] = markedSpace[0] - 1
    elif fighterRow < markedSpace[0] < 11: nextSpace[0] = markedSpace[0] + 1
    
    if 0 < markedSpace[1] < fighterColumn: nextSpace[1] = markedSpace[1] - 1
    elif fighterColumn < markedSpace[1] < 11: nextSpace[1] = markedSpace[1] + 1

    return nextSpace


def throwStone(fighter, category, dmgType, groups, battleMap) -> None:
    range = 4
    if "Sling" == fighter.equip["weapon"]["name"]: range = fighter.equip["weapon"]["reach"]
    tossSpace = Locate.findSpace(fighter, groups, range, "stone")

    if tossSpace == "None":
        Select.waitPrint(fighter.props["name"] + " cancels a throw before detonation.")
        Select.quickPrint("The stone is expended.")
    else:
        potency = 2
        if category == "cores": potency = 3
        affectSpace(tossSpace, dmgType, potency, battleMap)