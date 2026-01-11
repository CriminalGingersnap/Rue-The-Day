from Systems import PlayerSelect as Select
from . import Boons_Apply as Boons, Reactions


def applyCompel(target, ability) -> bool:
    dice = target.effects[ability]["dice"]
    source = target.effects[ability]["source"]
    compelled = False

    if (source != None) and (dice > 0):
        if target in source.commitments[ability]["targets"]:
            Select.waitPrint(ability + " triggered!")

            roll = Boons.expend(source, target, dice, ability, "magic")
            success = resistCompulsion(roll, target)

            if success:
                Select.waitPrint(ability + " succeeds!")
                compelled = True
            else: Select.waitPrint(ability + " fails!")

    target.effects[ability]["additional"] = compelled

def resistCompulsion(roll, target, ability) -> list:
    attempt, phrase = roll[0], "Resistance Threshold: "
    target.effects[ability]["dice"] -= roll[1]

    threshold = max(1, ((3 * (target.atrb["base_mag"] + target.atrb["base_mar"])) - target.atrb["corruption"]))
    phrase += threshold + " "

    if ability == "Compel":
        if target.cndt["sapient"]:
            threshold += 3
            phrase += "+3 (Sapient) | "
        elif target.cndt["social"]:
            threshold += 3
            phrase += "+3 (Social) | "
    if target.cndt["inviolable"]:
        threshold += 10
        phrase += "+10 (Inviolable) | "

    Select.waitPrint(phrase)
    Select.waitPrint("Total: " + threshold)
    return attempt > threshold


def applyDisorient(target) -> int:
    dice = target.effects["Disorient"]["dice"]
    source = target.effects["Disorient"]["source"]
    ability = target.effects["Disorient"]["ability"]

    reduction, dType = 0, ""
    if ability == "Disorient": dType = "magic"
    elif ability == "Harry": dType = "martial"

    if (source != None) and (dice > 0):
        if target in source.commitments["Disorient"]["targets"]:
            Select.waitPrint(ability + " triggered!")

            roll = Boons.expend(source, target, dice, ability, dType)
            reduction = roll[0]
            target.effects["Disorient"]["dice"] -= roll[1]

            Select.waitPrint(target.name + "'s AV temporarily decreases by " + str(reduction) + ".")
            Select.waitPrint(source.name + "'s AV decreases by the same amount.")

    return reduction


def applyMisdirect(target) -> int:
    dice = target.effects["Misdirect"]["dice"]
    source = target.effects["Misdirect"]["source"]
    ability = target.effects["Misdirect"]["ability"]

    reduction, dType = 0, ""
    if ability == "Misdirect": dType = "magic"
    elif ability == "Bind": dType = "martial"

    if (source != None) and (dice > 0):
        if target in source.commitments["Misdirect"]["targets"]:
            Select.waitPrint(ability + " triggered!")

            roll = Boons.expend(source, target, dice, ability, dType)
            reduction = roll[0]
            target.effects["Misdirect"]["dice"] -= roll[1]

            Select.waitPrint(target.name + "'s attempt decreases by " + str(reduction))
            
    return reduction