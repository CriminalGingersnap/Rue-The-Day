from Systems import PlayerSelect as Select
from . import Area_Apply as Apply, DamageTypes as Damage
from Maps import Map_Update as uMap, Map_Instantiate as iMap

areaAbilities = ["Bless", "Breath", "Hex"]

def execute(fighter, groups, ability, battleMap) -> None:
    phrase = markSpace(fighter, groups, ability, battleMap)
    Select.waitPrint(phrase)


def markSpace(fighter, groups, ability, battleMap) -> str:
    phrase, range, dmgType, dType = "", 10, "", "cur_mag"
    dmgType = Damage.convertElmToDmg(fighter.atrb["cur_elm"])

    match ability:
        case "Breath":
            phrase = " exhales " + fighter.atrb["cur_elm"] + " breath"
            range = 1
        case "Bless": phrase, dmgType = " blesses the ground!"
        case "Hex":
            article = "a"
            if fighter.atrb["cur_elm"][0] in ["A", "E", "I", "O", "U"]: article = "an"
            phrase, dmgType = " places " + article + fighter.atrb["cur_elm"] + " hex!"
    
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


def throwStone(fighter, stone, groups, battleMap) -> str:
    tossSpace = findSpace(fighter, groups, 4)
    tossRow, tossColumn = tossSpace[0], tossSpace[1]
    elm, potency = "", 2

    if "Pearl" in stone: elm = stone.split(" Pearl")[0]
    else:
        elm = stone.split(" Core")[0]
        potency = 3
    dmgType = Damage.convertElmToDmg(elm)

    if "Fey" in stone:
        uMap.updatePlacement(battleMap, fighter.sightMap, tossRow, tossSpace[1], fighter)
        if potency == 3:
            tossSpace = findSpace(fighter, groups, 4)
            tossRow, tossColumn = tossSpace[0], tossSpace[1]
            if (tossRow != fighter.position[0]) and (tossColumn != fighter.position[1]):
                uMap.updatePlacement(battleMap, fighter.sightMap, tossRow, tossColumn, fighter)
                potency -= 1
        potency -= 1

    atmosphere = Apply.getAtmosphere(potency, dmgType)
    battleMap[tossRow][tossColumn] = atmosphere + battleMap[tossRow][tossColumn][1:]
    Apply.spreadAtmosphere(atmosphere, dmgType, potency, tossRow, tossColumn, battleMap)

    return fighter.name + " throws a " + stone + "!"

def getStoneDmgType(stone) -> str:
    dmgType = ""
    if "Blessed" in stone: dmgType = "Holy"
    elif "Corpse" in stone: dmgType = "Rot"
    elif "Flame" in stone: dmgType = "Burn"
    elif "Ice" in stone: dmgType = "Freeze"
    elif "Fey" in stone: dmgType = "Dream"
    elif "Toxin" in stone: dmgType = "Venom"

    return dmgType


def enchant(fighter, battleMap) -> None:
    fighterRow, fighterColumn = fighter.position[0], fighter.position[1]
    atmosphere, phrase = battleMap[fighterRow][fighterColumn][0], ""

    if atmosphere == "*": atmosphere = "M"
    else: atmosphere = "m"
    phrase = " casts magic dust into the air!"

    battleMap[fighterRow][fighterColumn] = atmosphere + battleMap[fighterRow][fighterColumn][1:]
    Select.waitPrint(fighter.name + phrase)