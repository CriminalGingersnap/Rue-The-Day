from Systems import PlayerSelect as Select, Damage
from . import Boons_Apply as Apply

martialBoons = ["Conceal", "Guard"]
magicBoons = ["Focus", "Shroud", "Wreath"]


def commitDice(fighter, principal, boon) -> None: 
    newDice = 0

    if boon in martialBoons: newDice = fighter.atrb["cur_mar"]
    elif boon in magicBoons: newDice = fighter.atrb["cur_mag"]

    trueBoon = boonComment(fighter, principal, boon)

    if newDice > principal.effects[trueBoon]["dice"]:
        fighter.commits[trueBoon]["targets"] += [principal]
        principal.effects[trueBoon]["source"] = fighter
        principal.effects[trueBoon]["ability"] = boon
        if boon == "Wreath":
            dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], boon)
            principal.effects["Wreath"]["additional"] = dmgType

    principal.effects[trueBoon]["dice"] += newDice

    if boon in ["Conceal", "Shroud"]:
        roll = Apply.apply(principal, trueBoon)
        distance = max(10 - roll, 2)
        fighter.effects["Shroud"]["additional"] = distance
        Select.waitPrint("Fighter is concealed beyond " + str(distance) + " spaces.")


def boonComment(fighter, principal, boon) -> None:
    phrase, end = fighter.props["name"], principal.props["name"] + "!"
    if fighter == principal: end = "self!"
    trueBoon = boon

    match boon:
        case "Conceal":
            phrase += " conceals " + end
            trueBoon = "Shroud"
        case "Focus": phrase += " focuses " + end
        case "Guard": phrase += " guards " + end
        case "Shroud": phrase += " shrouds " + end
        case "Wreath": phrase += " wreaths " + end

    Select.waitPrint(phrase)
    return trueBoon