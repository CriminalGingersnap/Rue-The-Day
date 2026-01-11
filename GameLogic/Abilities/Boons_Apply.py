from Systems import PlayerSelect as Select, Roll, Conditions
from . import Reactions
import random


def expend(source, dice, ability, dType) -> int:
    if dice > 0 and (source.cndt["dead"] == False):
        expenditure = 0

        if dice == 1: expenditure = 1
        elif source.rank == "player":
            Select.waitPrint("Expend dice(" + str(dice) + "):")
            expenditure = Select.takeInput(1, dice)
        else: expenditure = random.randint(1, dice)

        roll = Roll.roll(source, expenditure, ability, dType)
        return [roll, 0]
    else: return [0, 0]


def applyFocus(principal) -> int:
    dice = principal.effects["Focus"]["dice"]
    source = principal.effects["Focus"]["source"]
    increase = 0

    if (source != None) and (dice > 0):
        if principal in source.commitments["Focus"]["targets"]:
            Select.waitPrint("Focus triggered!")

            roll = expend(source, principal, dice, "Focus", "magic")
            increase = roll[0]
            principal.effects["Focus"]["dice"] -= roll[1]

            Select.waitPrint(principal.name + "'s attempt increases by " + str(increase) + ".")

    return increase


def applyGuard(principal) -> int:
    dice = principal.effects["Guard"]["dice"]
    source = principal.effects["Guard"]["source"]
    ability = principal.effects["Guard"]["ability"]
    bonus = 0

    if (source != None) and (dice > 0):
        if principal in source.commitments["Guard"]["targets"]:
            Select.waitPrint(ability + " triggered!")

            roll = expend(source, principal, dice, ability, "martial")
            bonus = roll[0]
            principal.effects["Guard"]["dice"] -= roll[1]
            
            Select.waitPrint(principal.name + "'s AV increases by " + str(bonus) + ".")

    return bonus


def applyRegenerate(fighter, principal, ability) -> str:
    dice = fighter.atrb["cur_mag"]
    roll = Roll.roll(fighter, dice, ability, "magic")
    phrase = ""

    if ability == "Heal": phrase = " heals " + principal.name + "!"
    else: phrase = " regenerates!"

    principal.atrb["cur_hp"] = min(principal.atrb["base_hp"], principal.atrb["cur_hp"] + roll)
    return fighter.name + phrase


def applyShroud(fighter) -> bool:
    dice = fighter.effects["Shroud"]["dice"]
    visible = True

    if dice > 0:
        Select.waitPrint("Shroud triggered!")
        source = fighter.effects["Shroud"]["source"]
        roll = expend(fighter, source, dice, "Shroud", "magic")
        
        distance = max((6 - roll[0]), 1)
        fighter.effects["Shroud"]["additional"] = distance
        fighter.effects["Shroud"]["dice"] -= roll[1]
        
        if fighter.rank == "player":
            Select.waitPrint(fighter.name + " is invisible beyond a distance of " + str(distance) + ".")

    return visible


def applyWreath(principal, attackDmgType) -> int:
    dice = principal.effects["Wreath"]["dice"]
    source = principal.effects["Wreath"]["source"]
    wreathElement = principal.effects["Wreath"]["additional"]
    bonus = 0

    if (source != None) and (dice > 0):
        compatible = checkCompatibility(attackDmgType, wreathElement)

        if compatible and (principal in source.commitments["Wreath"]["targets"]):
            Select.waitPrint("Wreath engaged!")
                            
            roll = expend(source, principal, dice, "Wreath", "magic")
            bonus = roll[0]
            principal.effects["Wreath"]["dice"] -= roll[1]

            if attackDmgType == wreathElement:
                bonus //= 2
                Select.waitPrint("Wreath provides half protection against it's own element!")
                Select.waitPrint("Total reduced to " + str(bonus) + "!")

            Select.waitPrint(principal.name + " blocks " + str(bonus) + " " + attackDmgType + " damage.")

    return bonus

def checkCompatibility(attackDmgType, responseDmgType) -> bool:
    compatible = False
    if (attackDmgType in ["Burn", "Freeze"]) and (responseDmgType in ["Burn", "Freeze"]): compatible = True
    elif (attackDmgType in ["Holy", "Rot"]) and (responseDmgType == "Holy"): compatible = True
    elif (attackDmgType in ["Crush", "Pierce", "Dream"]) and (responseDmgType == "Dream"): compatible = True
    elif (attackDmgType in ["Dream", "Rot", "Venom"]) and (responseDmgType == "Rot"): compatible = True
    elif (attackDmgType in ["Rot", "Venom"]) and (responseDmgType == "Venom"): compatible = True

    return compatible