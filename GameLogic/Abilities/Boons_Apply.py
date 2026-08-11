from Systems import PlayerSelect as Select, Roll, Conditions
from . import Boons_Set, Hindrances_Set
import random


def expend(source, principal, dice, ability, dType) -> int:
    if dice > 0 and (source.cndt["dead"] == False):
        expenditure = 0

        if dice == 1: expenditure = 1
        elif source.props["rank"] == "player":
            Select.waitPrint("Expend dice(" + str(dice) + "):")
            expenditure = Select.takeInput(1, dice)
        else: expenditure = random.randint(1, dice)

        roll = Roll.roll(source, principal, expenditure, ability, dType)
        return [roll, expenditure]
    else: return [0, 0]


def apply(principal, ability) -> int:
    dice = principal.effects[ability]["dice"]
    source = principal.effects[ability]["source"]
    specific = principal.effects[ability]["ability"]
    increase, dType = 0, ""

    if specific in Boons_Set.martialBoons + Hindrances_Set.martialHindrances: dType = "martial"
    elif specific in Boons_Set.magicBoons + Hindrances_Set.magicHindrances: dType = "magic"

    if (source != None) and (dice > 0):
        if principal in source.commits[ability]["targets"]:
            element = ""
            if ability == "Wreath": element = principal.effects[ability]["additional"] + " "
            if print: Select.waitPrint("\n" + element + specific + " triggered on " + principal.props["name"] + "!")

            roll = expend(source, principal, dice, specific, dType)
            increase = roll[0]
            principal.effects[ability]["dice"] -= roll[1]

    return increase


def applyFocus(principal):
    bonus = apply(principal, "Focus")
    if bonus > 0: Select.waitPrint(principal.props["name"] + "'s attempt increases by " + str(bonus) + ".\n")
    return bonus

def applyGuard(principal):
    bonus = apply(principal, "Guard")
    if bonus > 0: Select.waitPrint(principal.props["name"] + "'s AV increases by " + str(bonus) + ".\n")
    return bonus

def applyFortify(principal) -> str:
    bonus = apply(principal, "Fortify")
    Conditions.recoverTolerance(principal, bonus)

def applyHeal(principal) -> str:
    bonus = apply(principal, "Heal")
    Conditions.recoverHP(principal, bonus)

def applyRally(principal) -> str:
    bonus = apply(principal, "Rally")
    Conditions.recoverStamina(principal, bonus)


def applyVeil(principal):
    roll = apply(principal, "Veil")

    if roll > 0:
        distance = max(10 - roll, 1)
        principal.effects["Veil"]["additional"] = distance
        Select.waitPrint(principal.props["name"] + " is concealed beyond " + str(distance) + " spaces.\n")


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

        Select.waitPrint(principal.props["name"] + " blocks " + str(bonus) + " " + attackDmgType + " damage.\n")

    return bonus

def checkCompatibility(attackDmgType, responseDmgType) -> bool:
    compatible = False
    if (attackDmgType in ["Flame", "Ice"]) and (responseDmgType in ["Flame", "Ice"]): compatible = True
    elif (attackDmgType in ["Holy", "Rot"]) and (responseDmgType == "Holy"): compatible = True
    elif (attackDmgType in ["Rot", "Toxic"]) and (responseDmgType == "Rot"): compatible = True

    return compatible