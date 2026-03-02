from Systems import Conditions, PlayerSelect as Select
from . import Area_Apply as Apply, DamageTypes as Damage
import random

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
    
    boarders = setBorders(fighter, range)
    markSpace = Apply.selectSpace(fighter, groups, boarders)
    affectSpace(fighter, markSpace, dmgType, dType, battleMap)
    fighter.atrb[dType] = 0

    return fighter.name + phrase

def setBorders(fighter, range) -> list:
    column, row = fighter.position[1], fighter.position[0]
    leftEdge, rightEdge = max(0, (column - range)), min(11, (column + range))
    topEdge, bottomEdge = max(0, (row - range)), min(11, (row + range))
    return [leftEdge, rightEdge, topEdge, bottomEdge]


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
    boarders = setBorders(fighter, 4)
    tossSpace = Apply.selectSpace(fighter, groups, boarders)
    tossRow, tossColumn = tossSpace[0], tossSpace[1]

    atmosphere = Apply.getAtmosphere("Stone", item)
    battleMap[tossRow][tossColumn] = atmosphere + battleMap[tossRow][tossColumn][1:]
    
    potency = 1
    if "Core" in item: potency = 2
    Apply.spreadAtmosphere(atmosphere, potency, tossRow, tossColumn, battleMap)

    return fighter.name + " throws a " + item + "!"


def enchant(fighter, battleMap, potency) -> None:
    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    atmosphere, phrase = battleMap[fighterRow][fighterColumn][0], ""

    match potency:
        case "1":
            if atmosphere == "*": atmosphere, phrase = "m", " invests raw mana into the earth!"
            else: atmosphere, phrase = "*", " prepares the ground for enchantment!"
        case "2":
            if atmosphere == "*": atmosphere = "M"
            else: atmosphere = "m"
            phrase = " casts magic dust into the air!"

    battleMap[fighterRow][fighterColumn] = atmosphere + battleMap[fighterRow][fighterColumn][1:]
    Select.waitPrint(fighter.name + phrase)