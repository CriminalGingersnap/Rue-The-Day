from Systems import PlayerSelect as Select, Roll, Conditions
from . import Boons_Set, Hindrances_Set
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


def apply(principal, ability) -> int:
    dice = principal.effects[ability]["dice"]
    source = principal.effects[ability]["source"]
    specific = principal.effects[ability]["ability"]
    increase, dType = 0, ""

    if specific in Boons_Set.martialBoons + Hindrances_Set.martialHindrances: dType = "martial"
    elif specific in Boons_Set.magicBoons + Hindrances_Set.magicHindrances: dType = "magic"

    if (source != None) and (dice > 0):
        if principal in source.commitments[ability]["targets"]:
            Select.waitPrint(specific + " triggered!")

            roll = expend(source, dice, specific, dType)
            increase = roll[0]
            principal.effects[ability]["dice"] -= roll[1]

    return increase


def applyFocus(principal):
    bonus = apply(principal, "Focus")
    if bonus > 0: Select.waitPrint(principal.name + "'s attempt increases by " + str(bonus) + ".")
    return bonus

def applyGuard(principal):
    bonus = apply(principal, "Guard")
    if bonus > 0: Select.waitPrint(principal.name + "'s AV increases by " + str(bonus) + ".\n")
    return bonus


def applyHeal(principal, ability) -> str:
    bonus = apply(principal, ability)
    Conditions.recoverHP(principal, bonus)


def applyShroud(fighter) -> bool:
    roll = apply(fighter, "Shroud")
    visible = True

    if roll > 0:
        distance = max((12 - roll[0]), 1)
        fighter.effects["Shroud"]["additional"] = distance
        Select.waitPrint(fighter.name + " is invisible beyond a distance of " + str(distance) + ".")

    return visible


def applyWreath(principal, attackDmgType) -> int:
    wreathElement = principal.effects["Wreath"]["additional"]
    compatible = checkCompatibility(attackDmgType, wreathElement)
    bonus = 0

    if compatible :
        bonus = apply(principal, "Wreath")

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