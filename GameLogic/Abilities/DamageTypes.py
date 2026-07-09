from Systems import PlayerSelect as Select
from . import Boons_Apply as Boons


pierceAttacks = ["Bodkin", "Bite", "Broadhead", "Claw", "Stab"]
crushAttacks = ["Bash", "Gore", "Pinch", "Ram", "Sling", "Kick"]
venomAttacks = ["Spray", "Sting"]
rotAttacks = ["Spit"]


def convertElmToDmg(elm) -> str:
    match elm:
        case "Blessed": return "Holy"
        case "Corpse": return "Rot"
        case "Fey": return "Dream"
        case "Flame": return "Burn"
        case "Ice": return "Freeze"
        case "Toxin": return "Venom"
        case _: return "None"

def identifyDamageType(fighter, ability) -> str:
    fighterDmgType = convertElmToDmg(fighter.atrb["cur_elm"])

    if fighter.props["type"] == "elemental": return fighterDmgType
    elif ability in pierceAttacks: return "Pierce"
    elif ability in crushAttacks: return "Crush"
    elif ability in venomAttacks: return "Venom"
    elif ability in rotAttacks: return "Rot"
    else: return fighterDmgType


def applyResistance(damage, dmgType, target) -> int:
    tRes = target.atrb["cur_res"][dmgType]

    multiplier = 1
    match tRes:
        case "resistant": multiplier = .5
        case "immune": multiplier = 0
        case "vulnerable": multiplier = 2

    if tRes != "normal":
        Select.waitPrint("Target is " + tRes + " to " + dmgType + "!")

    armorType = convertElmToDmg(target.equip["armor"]["element"])
    if (multiplier > 0) and Boons.checkCompatibility(dmgType, armorType):
        Select.waitPrint("Target is wearing armor resistant to " + dmgType + " damage!")
        reduction = target.equip["armor"]["modifier"] * .1

        if dmgType == armorType:
            Select.waitPrint("Enchanted armor provides half protection against its own element!")
            multiplier = max(0, multiplier - reduction)
        else:  multiplier = max(0, multiplier - (reduction * 2))

    return int(damage * multiplier)


def modifyResistance(target, dmgType, potency, direction):
    natRes, res = target.atrb["nat_res"][dmgType], "normal"

    match direction:
        case "positive":
            match potency:
                case 1:
                    match natRes:
                        case "resistant": res = "immune"
                        case "normal": res = "resistant"
                        case "vulnerable": res = "normal"
                case 2:
                    match natRes:
                        case "resistant": res = "immune"
                        case "normal": res = "immune"
                        case "vulnerable": res = "resistant"
                case 3: res = "immune"
        case "negative":
            match potency:
                case 1:
                    match natRes:
                        case "immune": res = "resistant"
                        case "resistant": res = "normal"
                        case "normal": res = "vulnerable"
                case 2:
                    match natRes:
                        case "immune": res = "normal"
                        case "resistant": res = "vulnerable"
                        case "normal": res = "vulnerable"
                case 3: res = "vulnerable"

    target.atrb["cur_res"][dmgType] = res