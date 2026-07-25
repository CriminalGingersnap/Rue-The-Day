from Systems import PlayerSelect as Select, Roll
from . import Area_Locate as Locate, Area_Apply as Apply
from Maps import Map_Update as uMap

areaAbilities = ["Bless", "Breath", "Hex", "Shroud", "Slip"]


def execute(fighter, groups, ability, battleMap) -> str:
    phrase, range = fighter.props["name"], 10
    scale = fighter.atrb["cur_mag"]
    fighter.atrb["cur_mag"] = 0

    article = "a"
    if fighter.atrb["cur_elm"][0] in ["A", "E", "I", "O", "U"]: article = "an"

    match ability:
        case "Breath":
            phrase += " exhales " + fighter.atrb["cur_elm"] + " breath"
            range = 1
            if fighter.cndt["massive"]: range = 2
        case "Bless": phrase += " blesses the ground!"
        case "Hex": phrase += " places " + article + fighter.atrb["cur_elm"] + " hex!"
        case "Shroud": phrase += " emanates " + article + fighter.atrb["cur_elm"] + " shroud!"
        case "Slip": phrase += " slips between spaces! Rolling range."

    Select.waitPrint(phrase)

    markedSpace = [0, 0]
    if ability == "Shroud": markedSpace = [fighter.pos[0], fighter.pos[1]]
    else:
        if ability == "Slip": range = Roll.roll(fighter, fighter.atrb["cur_mag"], "Slip", "magic")
        markedSpace = Locate.findSpace(fighter, groups, range, ability)

    if markedSpace == "None":
        Select.waitPrint(fighter.props["name"] + " dispels an area ability before execution.")
    elif ability == "Slip":
        tossRow, tossColumn = markedSpace[0], markedSpace[1]
        uMap.updatePlacement(battleMap, fighter.sightMap, tossRow, tossColumn, fighter)
    else:
        affectSpace(fighter, markedSpace, fighter.atrb["cur_elm"], scale, battleMap)


def affectSpace(fighter, markSpace, dmgType, scale, battleMap) -> None:
    effectRow, effectColumn = markSpace[0], markSpace[1]

    atmosphere = Apply.getAtmosphere(scale, dmgType)
    lesserAtmosphere = Apply.getAtmosphere(scale-1, dmgType)
    leastAtmosphere = Apply.getAtmosphere(1, dmgType)

    battleMap[effectRow][effectColumn] = atmosphere + battleMap[effectRow][effectColumn][1:]
    Apply.spreadAtmosphere(leastAtmosphere, scale+1, effectRow, effectColumn, battleMap)
    Apply.spreadAtmosphere(lesserAtmosphere, scale, effectRow, effectColumn, battleMap)

    fighterRow, fighterColumn = fighter.pos[0], fighter.pos[1]
    if any(hazard in battleMap[fighterRow][fighterColumn] for hazard in [lesserAtmosphere, atmosphere]):
        battleMap[fighterRow][fighterColumn] = "_" + battleMap[fighterRow][fighterColumn][1:]


def throwStone(fighter, category, dmgType, groups, battleMap) -> None:
    range = 4
    if "Sling" == fighter.equip["weapon"]["name"]: range = fighter.equip["weapon"]["reach"]
    tossSpace = Locate.findSpace(fighter, groups, range, "stone")

    if tossSpace == "None":
        Select.waitPrint(fighter.name + " cancels a throw before detonation.")
        Select.quickPrint("The stone is expended.")
    else:
        potency = 2
        if category == "cores": potency = 3
        affectSpace(fighter, tossSpace, dmgType, potency, battleMap)