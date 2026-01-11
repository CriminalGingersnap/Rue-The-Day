from Systems import PlayerSelect as Select
from . import DamageTypes as Damage


martialBoons = ["Bristle", "Evade", "Guard"]
magicBoons = ["Focus", "Shroud", "Wreath"]


def commitDice(fighter, principal, boon) -> None: 
    newDice = 0

    if boon in martialBoons: newDice = fighter.atrb["cur_mar"]
    elif boon in magicBoons: newDice = fighter.atrb["cur_mag"]

    trueBoon = boonComment(fighter, principal, boon)

    if newDice > principal.effects[trueBoon]["dice"]:
        fighter.commitments[trueBoon]["targets"] += [principal]
        principal.effects[trueBoon]["source"] = fighter
        principal.effects[trueBoon]["ability"] = boon
        if boon == "Wreath":
            dmgType = Damage.identifyDamageType(fighter, boon)["basic"]
            principal.effects["Wreath"]["additional"] = dmgType

    principal.effects[trueBoon]["dice"] += newDice


def boonComment(fighter, principal, boon) -> None:
    phrase, end = fighter.name, principal.name + "!"
    if fighter == principal: end = "self!"
    trueBoon = boon

    match boon:
        case "Bristle":
            phrase += " bristles!"
            trueBoon = "Guard"
        case "Guard": phrase += " guards " + end
        case "Evade":
            phrase += " evades!"
            trueBoon = "Guard"
        case "Focus": phrase += " focuses " + end
        case "Shroud": phrase += " shrouds " + end
        case "Wreath": phrase += " wreaths " + end

    Select.waitPrint(phrase)
    return trueBoon