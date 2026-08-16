from . import PlayerSelect as Select
from Abilities import Boons_Apply as Boons


pierceAttacks = ["Bodkin", "Bite", "Broadhead", "Claw", "Peck", "Stab"]
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

    if tRes != "normal":
        Select.waitPrint("Target is " + tRes + " to " + dmgType + "!")
        Select.waitPrint("Damage multiplier set to " +  str(multiplier) + ".")

    armorEnchantReduction, shieldEnchantReduction = 0, 0
    armorType = target.equip["armor"]["element"]
    shieldType = target.equip["shield"]["element"]

    if (multiplier > 0) and Boons.checkCompatibility(dmgType, shieldType):
        Select.waitPrint("Target carries a talisman of " + target.equip["shield"]["element"] + "!")
        shieldEnchantReduction = .5
        if dmgType == shieldType:
            Select.quickPrint("Enchantments provide half protection against their own element.")
            shieldEnchantReduction = .25
        Select.waitPrint("Damage multiplier reduces by " + str(shieldEnchantReduction) + ".")

    if (multiplier > 0) and Boons.checkCompatibility(dmgType, armorType):
        armorMod, armorName = target.equip["armor"]["modifier"], target.equip["armor"]["name"]

        Select.waitPrint("Target is wearing " + armorName + " " + armorType + " armor!")
        armorEnchantReduction = armorMod * .1
        if dmgType == armorType:
            Select.quickPrint("Enchantments provide half protection against their own element.")
            armorEnchantReduction /= 2
        Select.waitPrint("Damage multiplier reduces by " + str(armorEnchantReduction) + ".")

    reduction = armorEnchantReduction + shieldEnchantReduction
    multiplier = max(0, multiplier - reduction)
    damage = int(damage * multiplier)

    if multiplier != 1:
        Select.quickPrint("Final damage: ", ending = "")
        Select.waitPrint(str(damage))

    return damage


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