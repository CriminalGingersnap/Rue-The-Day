from Systems import PlayerSelect as Select
from . import Boons_Apply as Boons


pierceAttacks = ["Bodkin", "Bite", "Bristle", "Broadhead", "Claw", "Gore", "Stab"]
crushAttacks = ["Bash", "Ram", "Sling", "Kick"]
venomAttacks = ["Spray", "Sting"]

def identifyDamageType(fighter, ability) -> str:
    damageTypes = {"base": "", "bonus": "None"}

    match fighter.atrb["cur_elm"]:
        case "Blessed": damageTypes["bonus"] = "Holy"
        case "Corpse": damageTypes["bonus"] = "Rot"
        case "Fey": damageTypes["bonus"] = "Dream"
        case "Flame": damageTypes["bonus"] = "Burn"
        case "Ice": damageTypes["bonus"] = "Freeze"
        case "Toxin": damageTypes["bonus"] = "Venom"
    
    if ability in pierceAttacks:
        if damageTypes["bonus"] == "None": damageTypes["bonus"] = "Bleed"
        damageTypes["base"] = "Pierce"
    elif ability in crushAttacks: damageTypes["base"] = "Crush"
    elif ability in venomAttacks: damageTypes["base"] = "Venom"
    elif ability in ["Bring", "Breath"]: damageTypes["base"] = damageTypes["bonus"]

    if damageTypes["base"] == damageTypes["bonus"]: damageTypes["bonus"] = "None"

    return damageTypes

def applyResistance(damage, dmgType, target) -> int:
    tRes = target.atrb["cur_res"][dmgType]

    multiplier = 1
    match tRes:
        case "resistant": multiplier = .5
        case "immune": multiplier = 0
        case "vulnerable": multiplier = 2

    if tRes != "normal":
        Select.waitPrint("Target is " + tRes + " to " + dmgType + "!")

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
                case 3:
                    match natRes:
                        case "resistant": res = "immune"
                        case "normal": res = "immune"
                        case "vulnerable": res = "immune"
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
                case 3:
                    match natRes:
                        case "immune": res = "vulnerable"
                        case "resistant": res = "vulnerable"
                        case "normal": res = "vulnerable"

    target.atrb["cur_res"][dmgType] = res