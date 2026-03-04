from Systems import PlayerSelect as Select
from . import Area_Apply as Apply, DamageTypes as Damage


areaAbilities = ["Bless", "Breath", "Hex"]

def execute(fighter, groups, ability, battleMap) -> None:
    phrase = markSpace(fighter, groups, ability, battleMap)
    Select.waitPrint(phrase)


def markSpace(fighter, groups, ability, battleMap) -> str:
    phrase, range, dmgType, dType = "", 10, "", "cur_mag"

    match ability:
        case "Breath":
            phrase = " exhales " + fighter.atrb["cur_elm"] + " breath"
            dmgType = Damage.identifyDamageType(fighter, "Breath")["base"]
            range = 1
        case "Bless": phrase, dmgType = " blesses the ground!", "Holy"
        case "Hex": phrase, dmgType = " hexes the ground!", Damage.identifyDamageType(fighter, "Bring")
    
    if dmgType in ["Crush", "Pierce", "Venom"]: dType = "cur_mar"
    
    markedSpace = findSpace(fighter, groups, range)
    affectSpace(fighter, markedSpace, dmgType, dType, battleMap)
    fighter.atrb[dType] = 0

    return fighter.name + phrase

def findSpace(fighter, groups, range) -> list:
    column, row = fighter.position[1], fighter.position[0]
    leftEdge, rightEdge = max(0, (column - range)), min(11, (column + range))
    topEdge, bottomEdge = max(0, (row - range)), min(11, (row + range))
    borders = [leftEdge, rightEdge, topEdge, bottomEdge]

    markedSpace = Apply.selectSpace(fighter, groups, borders)
    return markedSpace


def affectSpace(fighter, markSpace, dmgType, dType, battleMap) -> None:
    effectRow, effectColumn = markSpace[0], markSpace[1]
    scale = max(fighter.atrb[dType], 2)
    coverage, intenseCoverage = scale - 2, scale - 4

    atmosphere = Apply.getAtmosphere(fighter, 3, dmgType)
    petitAtmosphere = Apply.getAtmosphere(fighter, 2, dmgType)
    battleMap[effectRow][effectColumn] = atmosphere + battleMap[effectRow][effectColumn][1:]

    if coverage > 0:
        Apply.spreadAtmosphere(petitAtmosphere, dmgType, coverage, effectRow, effectColumn, battleMap)
        if coverage > 2:
            Apply.spreadAtmosphere(atmosphere, dmgType, intenseCoverage, effectRow, effectColumn, battleMap)

    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    if any(hazard in battleMap[fighterRow][fighterColumn] for hazard in [petitAtmosphere, atmosphere]):
        battleMap[fighterRow][fighterColumn] = "_" + battleMap[fighterRow][fighterColumn][1:]


def throwStone(fighter, item, groups, battleMap) -> str:
    tossSpace = findSpace(fighter, groups, 4)
    tossRow, tossColumn = tossSpace[0], tossSpace[1]
    dmgType = ""

    if "Blessed" in item: dmgType = "Holy"
    elif "Corpse" in item: dmgType = "Rot"
    elif "Fey" in item: dmgType = "Dream"
    elif "Flame" in item: dmgType = "Burn"
    elif "Ice" in item: dmgType = "Freeze"
    elif "Toxin" in item: dmgType = "Venom"

    atmosphere = Apply.getAtmosphere("Stone", item, dmgType)
    battleMap[tossRow][tossColumn] = atmosphere + battleMap[tossRow][tossColumn][1:]

    potency = 1
    if "Core" in item: potency = 2

    if dmgType == "Dream":
        fighter.position[0], fighter.position[1] = tossSpace[0], tossSpace[1]
        if potency == 2:
            tossSpace = findSpace(fighter, groups, 4)
            tossRow, tossColumn = tossSpace[0], tossSpace[1]
            fighter.position[0], fighter.position[1] = tossSpace[0], tossSpace[1]
    else:
        Apply.spreadAtmosphere(atmosphere, dmgType, potency, tossRow, tossColumn, battleMap)

    return fighter.name + " throws a " + item + "!"


def enchant(fighter, battleMap) -> None:
    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    atmosphere, phrase = battleMap[fighterRow][fighterColumn][0], ""

    if atmosphere == "*": atmosphere = "M"
    else: atmosphere = "m"
    phrase = " casts magic dust into the air!"

    battleMap[fighterRow][fighterColumn] = atmosphere + battleMap[fighterRow][fighterColumn][1:]
    Select.waitPrint(fighter.name + phrase)