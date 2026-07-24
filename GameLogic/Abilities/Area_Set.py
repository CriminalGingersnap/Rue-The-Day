from Systems import PlayerSelect as Select, Roll
from . import Area_Locate as Locate, Area_Apply as Apply
from Maps import Map_Update as uMap

areaAbilities = ["Bless", "Breath", "Hex", "Slip"]

def execute(fighter, groups, ability, battleMap) -> None:
    phrase = markSpace(fighter, groups, ability, battleMap)
    Select.waitPrint(phrase)


def markSpace(fighter, groups, ability, battleMap) -> str:
    phrase, range, dmgType = fighter.props["name"], 10, ""
    scale = max(fighter.atrb["cur_mag"], 3)

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
        affectSpace(fighter, markedSpace, dmgType, scale, battleMap)
        fighter.atrb["cur_mag"] = 0

        if ability == "Slip":
            tossRow, tossColumn = markedSpace[0], markedSpace[1]
            uMap.updatePlacement(battleMap, fighter.sightMap, tossRow, tossColumn, fighter)

    return phrase


def affectSpace(fighter, markSpace, dmgType, scale, battleMap) -> None:
    effectRow, effectColumn = markSpace[0], markSpace[1]
    coverage, intenseCoverage = scale - 2, scale - 4

    atmosphere = Apply.getAtmosphere(3, dmgType)
    petitAtmosphere = Apply.getAtmosphere(2, dmgType)
    battleMap[effectRow][effectColumn] = atmosphere + battleMap[effectRow][effectColumn][1:]

    if coverage > 0:
        Apply.spreadAtmosphere(petitAtmosphere, dmgType, coverage, effectRow, effectColumn, battleMap)
        if coverage > 2:
            Apply.spreadAtmosphere(atmosphere, dmgType, intenseCoverage, effectRow, effectColumn, battleMap)

    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    if any(hazard in battleMap[fighterRow][fighterColumn] for hazard in [petitAtmosphere, atmosphere]):
        battleMap[fighterRow][fighterColumn] = "_" + battleMap[fighterRow][fighterColumn][1:]


def throwStone(fighter, category, dmgType, groups, battleMap) -> None:
    range = 4
    if "Sling" == fighter.equip["weapon"]["name"]: range = fighter.equip["weapon"]["reach"]
    tossSpace = Locate.findSpace(fighter, groups, range, "stone")

    if tossSpace == "None":
        Select.waitPrint(fighter.name + " cancels a throw before detonation.")
        Select.quickPrint("The stone is expended.")
    else:
        tossRow, tossColumn = tossSpace[0], tossSpace[1]

        potency = 2
        if category == "cores": potency = 3

        atmosphere = Apply.getAtmosphere(potency, dmgType)
        battleMap[tossRow][tossColumn] = atmosphere + battleMap[tossRow][tossColumn][1:]

        leastAtmosphere = Apply.getAtmosphere(1, dmgType)
        Apply.spreadAtmosphere(leastAtmosphere, potency+1, tossRow, tossColumn, battleMap)

        lesserAtmosphere = Apply.getAtmosphere(potency-1, dmgType)
        Apply.spreadAtmosphere(lesserAtmosphere, potency, tossRow, tossColumn, battleMap)