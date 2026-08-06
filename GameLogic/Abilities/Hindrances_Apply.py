from Systems import PlayerSelect as Select, Conditions
from . import Boons_Apply as Boons
from Actions import HindranceActions as Hinder


def applyCompel(target, ability) -> None:
    compelled = False
    attempt = Boons.apply(target, ability)

    if attempt > 0:
        success = resistCompulsion(attempt, target, ability)

        if success:
            Select.waitPrint(ability + " succeeds!")
            compelled = True
        else: Select.waitPrint(ability + " fails!")

    target.effects[ability]["additional"] = compelled

def resistCompulsion(attempt, target, ability) -> list:
    penalty = target.atrb["corruption"] + target.atrb["fatigue"]
    threshold = max(1, ((3 * (target.atrb["base_mag"] + target.atrb["base_mar"])) - penalty))

    phrase = "Resistance Threshold: " + str(threshold) + " "

    source = target.effects[ability]["source"]
    if Hinder.canCompel(source, target, ability):
        if target.cndt["social"] and (ability == "Compel"):
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
    if reduction > 0: Select.waitPrint(target.props["name"] + "'s attempt decreases by " + str(reduction) + ".")
    return reduction


def applyDrain(principal) -> int:
    targets = principal.commits["Drain"]["targets"]

    for target in targets:
        cap = target.atrb["base_hp"] - target.atrb["cur_hp"]

        if (cap > 0) and not target.cndt["lifeless"]:
            Conditions.takeDamage(target, "Bleed", principal.commits["Drain"]["dice"])

            cap = target.atrb["base_hp"] - target.atrb["cur_hp"]
            Select.waitPrint(target.props["name"] + " has lost " + str(cap) + " points of health.")

            gain = Boons.apply(target, "Drain")
            if principal.props["type"] != target.props["type"]:
                Select.waitPrint("Drain is half effective between creatures of different types.")
                gain //= 2

            if gain > 0:
                Select.waitPrint(principal.props["name"] + " heals " + str(gain) + " points!")
                Conditions.recoverHP(principal, gain)
        else:
            Select.waitPrint(target.props["name"] + " has no spilled blood to sup.")