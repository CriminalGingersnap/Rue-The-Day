from Systems import PlayerSelect as Select, Roll
from . import Area_Locate as Locate, Area_Apply as Apply
from Maps import Map_Update as uMap

areaAbilities = ["Bless", "Breath", "Hex", "Slip"]

def execute(fighter, groups, ability, battleMap) -> None:
    phrase = markSpace(fighter, groups, ability, battleMap)
    Select.waitPrint(phrase)


def markSpace(fighter, groups, ability, battleMap) -> str:
    phrase, range, dmgType = fighter.props["name"], 10, ""
    scale = fighter.atrb["cur_mag"]

    match ability:
        case "Breath":
            phrase += " exhales " + fighter.atrb["cur_elm"] + " breath"
            range = 1
        case "Bless": phrase += " blesses the ground!"
        case "Hex":
            article = "a"
            if fighter.atrb["cur_elm"][0] in ["A", "E", "I", "O", "U"]: article = "an"
            phrase += " places " + article + fighter.atrb["cur_elm"] + " hex!"
        case "Slip": 
            phrase += " slips between spaces! Rolling range."
            range = Roll.roll(fighter, fighter.atrb["cur_mag"], "Slip", "magic")
            scale = max(0, scale - 1)
    
    markedSpace = Locate.findSpace(fighter, groups, range, ability)

    if markedSpace == "None":
        phrase = fighter.props["name"] + " cancels an area ability before execution."
    else:
        affectSpace(fighter, markedSpace, fighter.atrb["cur_elm"], scale, battleMap)
        fighter.atrb["cur_mag"] = 0

        if ability == "Slip":
            tossRow, tossColumn = markedSpace[0], markedSpace[1]
            uMap.updatePlacement(battleMap, fighter.sightMap, tossRow, tossColumn, fighter)

    return phrase


def affectSpace(fighter, markSpace, dmgType, scale, battleMap) -> None:
    effectRow, effectColumn = markSpace[0], markSpace[1]

    atmosphere = Apply.getAtmosphere(scale, dmgType)
    lesserAtmosphere = Apply.getAtmosphere(scale-1, dmgType)
    leastAtmosphere = Apply.getAtmosphere(1, dmgType)

    battleMap[effectRow][effectColumn] = atmosphere + battleMap[effectRow][effectColumn][1:]
    Apply.spreadAtmosphere(leastAtmosphere, scale+1, effectRow, effectColumn, battleMap)
    Apply.spreadAtmosphere(lesserAtmosphere, scale, effectRow, effectColumn, battleMap)

    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
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