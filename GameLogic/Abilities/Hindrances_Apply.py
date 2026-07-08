from Systems import PlayerSelect as Select
from . import Boons_Apply as Boons


def applyCompel(target, ability) -> None:
    compelled = False
    attempt = Boons.apply(target, ability)

    if attempt > 0:
        success = resistCompulsion(attempt, target)

        if success:
            Select.waitPrint(ability + " succeeds!")
            compelled = True
        else: Select.waitPrint(ability + " fails!")

    target.effects[ability]["additional"] = compelled

def resistCompulsion(attempt, target, ability) -> list:
    penalty = target.atrb["corruption"] + target.atrb["fatigue"]
    threshold = max(1, ((3 * (target.atrb["base_mag"] + target.atrb["base_mar"])) - penalty))

    phrase = "Resistance Threshold: " + str(threshold) + " "

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
    reduction = Boons.apply(target, "Disorient")
    if reduction > 0: Select.waitPrint(target.props["name"] + "'s AV temporarily decreases by " + str(reduction) + ".")
    return reduction

def applyMisdirect(target) -> int:
    reduction = Boons.apply(target, "Misdirect")
    if reduction > 0: Select.waitPrint(target.props["name"] + "'s attempt decreases by " + str(reduction))
    return reduction