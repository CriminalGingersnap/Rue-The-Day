from Systems import PlayerSelect as Select, Roll, Conditions
from . import Area_Locate as Locate, Area_Apply as Apply
from Maps import Map_Update as uMap

areaAbilities = ["Bless", "Breath", "Screen", "Infuse", "Slip"]


def execute(fighter, dice, groups, ability, battleMap) -> str:
    article, phrase, range = "a ", fighter.props["name"], 8
    if fighter.atrb["cur_elm"][0] in ["A", "E", "I", "O", "U"]: article = "an "

    match ability:
        case "Breath":
            phrase += " exhales " + fighter.atrb["cur_elm"] + " breath"
            if fighter.cndt["massive"]: range = 2
            else: range = 1
        case "Bless": phrase += " blesses the ground!"
        case "Infuse": phrase += " infuses the ground with " + fighter.atrb["cur_elm"] + " magic!"
        case "Screen": phrase += " raises " + article + fighter.atrb["cur_elm"] + " screen!"
        case "Slip": phrase += " slips between spaces! Rolling range."

    Select.waitPrint(phrase)

    if ability in ["Bless", "Infuse", "Screen"]: range = 0
    if ability == "Slip": range = Roll.roll(fighter, fighter, fighter.atrb["base_mag"], "Slip", "magic")
    markedSpace = Locate.findSpace(fighter, groups, range, ability)
    fighterRow, fighterColumn = fighter.pos[0], fighter.pos[1]

    if markedSpace == "None": Select.waitPrint(fighter.props["name"] + " dispels an area ability before execution.")
    else:
        Conditions.decrementStamina(fighter, dice)
        
        match ability:
            case "Bless" | "Infuse":
                halfScale = max(1, dice // 2)
                atmosphere = Apply.getAtmosphere(halfScale, fighter.atrb["cur_elm"])
                Apply.spreadAtmosphere(atmosphere, 1, markedSpace[0], markedSpace[1], battleMap)
            case "Breath":
                atmosphere, nextSpace = Apply.getAtmosphere(2, fighter.atrb["cur_elm"]), markedSpace
                for spaceNum in range(dice):
                    battleMap[nextSpace[0]][nextSpace[1]] = atmosphere + battleMap[fighterRow][fighterColumn][1:]
                    nextSpace = getNextSpace(nextSpace, fighterRow, fighterColumn)
            case "Screen":
                leastAtmosphere = Apply.getAtmosphere(1, fighter.atrb["cur_elm"])
                Apply.spreadAtmosphere(leastAtmosphere, dice, markedSpace[0], markedSpace[1], battleMap)
            case "Slip":
                tossRow, tossColumn = markedSpace[0], markedSpace[1]
                uMap.updatePlacement(battleMap, fighter.sightMap, tossRow, tossColumn, fighter)

        if ability in ["Infuse", "Screen"]:
            battleMap[fighterRow][fighterColumn] = "_" + battleMap[fighterRow][fighterColumn][1:]

def getNextSpace(markedSpace, fighterRow, fighterColumn) -> list:
    nextSpace = markedSpace[:]

    if 0 < markedSpace[0] < fighterRow: nextSpace[0] = markedSpace[0] - 1
    elif fighterRow < markedSpace[0] < 11: nextSpace[0] = markedSpace[0] + 1
    
    if 0 < markedSpace[1] < fighterColumn: nextSpace[1] = markedSpace[1] - 1
    elif fighterColumn < markedSpace[1] < 11: nextSpace[1] = markedSpace[1] + 1

    return nextSpace


def throwStone(fighter, category, dmgType, groups, battleMap) -> None:
    range = 4
    if "Sling" in fighter.equip["weapon"]["name"]: range = fighter.equip["weapon"]["reach"]
    tossSpace = Locate.findSpace(fighter, groups, range, "stone")

    if tossSpace == "None":
        Select.waitPrint(fighter.props["name"] + " cancels a throw before detonation.")
        Select.quickPrint("The stone is expended.")
    else:
        potency = 2
        if category == "cores": potency = 3
        affectSpace(tossSpace, dmgType, potency, battleMap)


def affectSpace(markSpace, dmgType, scale, battleMap) -> None:
    effectRow, effectColumn = markSpace[0], markSpace[1]

    atmosphere = Apply.getAtmosphere(scale, dmgType)
    lesserAtmosphere = Apply.getAtmosphere(scale-1, dmgType)
    leastAtmosphere = Apply.getAtmosphere(1, dmgType)

    battleMap[effectRow][effectColumn] = atmosphere + battleMap[effectRow][effectColumn][1:]
    Apply.spreadAtmosphere(leastAtmosphere, scale, effectRow, effectColumn, battleMap)
    Apply.spreadAtmosphere(lesserAtmosphere, scale-1, effectRow, effectColumn, battleMap)