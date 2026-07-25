from . import PlayerSelect as Select
from Abilities import Boons_Apply as Boons


pierceAttacks = ["Bodkin", "Bite", "Broadhead", "Claw", "Stab"]
crushAttacks = ["Bash", "Gore", "Pinch", "Ram", "Sling", "Kick"]
venomAttacks = ["Spray", "Sting"]
rotAttacks = ["Spit"]


def identifyDamageType(element, ability) -> str:
    if ability in pierceAttacks: return "Pierce"
    elif ability in crushAttacks: return "Crush"
    elif ability in venomAttacks: return "Toxic"
    elif ability in rotAttacks: return "Rot"
    else: return element


def applyResistance(damage, dmgType, target) -> int:
    tRes = target.atrb["cur_res"][dmgType]

    multiplier = 1
    match tRes:
        case "resistant": multiplier = .5
        case "immune": multiplier = 0
        case "vulnerable": multiplier = 2

    if tRes != "normal": Select.waitPrint("Target is " + tRes + " to " + dmgType + "!")

    protections, armorReduction, shieldReduction, waterReduction = [], 0, 0, 0
    armorType = target.equip["armor"]["element"]
    shieldType = target.equip["shield"]["element"]

    if (multiplier > 0) and Boons.checkCompatibility(dmgType, armorType):
        Select.waitPrint("Target is wearing " + target.equip["armor"]["element"] + " armor!")
        armorReduction = target.equip["armor"]["modifier"] * .1
        protections += [armorType]

    if (multiplier > 0) and Boons.checkCompatibility(dmgType, shieldType):
        Select.waitPrint("Target carries a talisman of " + target.equip["shield"]["element"] + "!")
        shieldReduction = .2
        protections += [shieldType]

    if target.cndt["submerged"]:
        Select.waitPrint("Target gains slight protection against damage by being submerged.")
        waterReduction = .1

    reduction = armorReduction + shieldReduction + waterReduction

    for protection in protections:
        if dmgType == protection:
            Select.waitPrint("Enchantments provide half protection against their own element!")
            multiplier = max(0, multiplier - reduction)
        else: multiplier = max(0, multiplier - (reduction * 2))

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