from Systems import PlayerSelect as Select
from . import Boons_Apply as Boons
from Actions import HindranceActions as Hinder


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
    threshold = max(1, ((4 * (target.atrb["base_mag"] + target.atrb["base_mar"])) - penalty))

    phrase = "Resistance Threshold: " + str(threshold) + " "

    source = target.effects[ability]["source"]
    if not Hinder.canCompel(source, target):
        threshold += 5
        phrase += "+5 (Incompatible) | "

    if target.cndt["inviolable"]:
        threshold += 10
        phrase += "+10 (Inviolable) | "

    if target.cndt["sapient"]:
        threshold += 6
        phrase += "+6 (Sapient) | "
    elif target.cndt["social"] and (ability == "Compel"):
        threshold += 3
        phrase += "+3 (Social) | "

    Select.waitPrint(phrase)
    Select.waitPrint("Total: " + threshold)
    return attempt > threshold


def applyConfuse(target) -> int:
    reduction = Boons.apply(target, "Confuse")
    if reduction > 0: Select.waitPrint(target.props["name"] + "'s AV temporarily decreases by " + str(reduction) + ".")
    return reduction

def applyConfound(target) -> int:
    reduction = Boons.apply(target, "Confound")
    if reduction > 0: Select.waitPrint(target.props["name"] + "'s attempt decreases by " + str(reduction))
    return reduction