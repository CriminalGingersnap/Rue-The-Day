from Systems import Conditions, PlayerSelect as Select
from . import Area_Apply as Apply, DamageTypes as Damage
import random

magicAreals = ["Bless", "Breath", "Hex"]
martialAreals = ["Mark", "Ready"]
areaAbilities = magicAreals + martialAreals

def execute(fighter, targets, ability, battleMap) -> None:
    phrase = markSpace(fighter, targets, ability, battleMap)
    Select.waitPrint(phrase)


def markSpace(fighter, targets, ability, battleMap) -> None:
    phrase, range, dmgType, dType = "", 10, "", "cur_mag"

    match ability:
        case "Breath":
            phrase = " exhales " + fighter.atrb["cur_elm"] + " breath"
            dmgType = Damage.identifyDamageType(fighter, "Breath")["base"]
            range = 1
        case "Bless": phrase, dmgType = " blesses the ground!", "Holy"
        case "Hex": phrase, dmgType = " hexes the ground!", Damage.identifyDamageType(fighter, "Bring")
        case "Mark": phrase, dmgType = " prepares to loose an arrow at a target space!", "Pierce"
        case "Ready":
            phrase = " readies their weapon!"
            dmgTypes = fighter.equipment["weapon"]["dmgTypes"]
            if len(dmgTypes == 1): dmgType = dmgTypes[0]
            elif fighter.rank == "player":
                Select.waitPrint("Choose damage type:")
                Select.makeSelection(dmgTypes)
            else: dmgType = random.choice(dmgTypes)
            range = fighter.equipment["weapons"]["reach"]
    
    if dmgType in ["Crush", "Pierce"]: dType = "cur_mar"
    
    boarders = setBorders(fighter, range)
    markSpace = Apply.selectSpace(fighter, targets, boarders)
    affectSpace(fighter, markSpace, dmgType, dType, battleMap)
    fighter.atrb[dType] = 0

    return fighter.name + phrase

def setBorders(fighter, range) -> list:
    column, row = fighter.position[1], fighter.position[0]
    leftEdge, rightEdge = max(0, (column-range)), min(11, (column+range))
    topEdge, bottomEdge = max(0, (row-range)), min(11, (row+range))
    return [leftEdge, rightEdge, topEdge, bottomEdge]


def affectSpace(fighter, markSpace, dmgType, dType, battleMap) -> list:
    effectRow, effectColumn = markSpace[0], markSpace[1]
    scale = max(fighter.atrb[dType], 2)

    atmosphere = Apply.getAtmosphere(fighter, min(scale, 3), dmgType)
    battleMap[effectRow][effectColumn] = atmosphere + battleMap[effectRow][effectColumn][1:]

    if scale > 3:
        potency = scale - 1
        Apply.spreadAtmosphere(atmosphere, dmgType, potency, effectRow, effectColumn, battleMap)
        Apply.setAtmosphere("_", effectRow, effectColumn, battleMap)


def throwStone(fighter, item, targets, battleMap) -> None:
    boarders = setBorders(fighter, 4)
    tossSpace = Apply.selectSpace(fighter, targets, boarders)
    tossRow, tossColumn = tossSpace[0], tossSpace[1]

    atmosphere = Apply.getAtmosphere("Stone", item)
    battleMap[tossRow][tossColumn] = atmosphere + battleMap[tossRow][tossColumn][1:]
    
    potency = 1
    if "Core" in item: potency = 2
    Apply.spreadAtmosphere(atmosphere, potency, tossRow, tossColumn, battleMap)

    return fighter.name + " throws a " + item + "!"