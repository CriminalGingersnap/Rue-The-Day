from Systems import PlayerSelect as Select
from . import DamageTypes as Damage


martialBoons = ["Guard"]
magicBoons = ["Focus", "Shroud", "Slip", "Wreath"]

magicSelfBoons = ["Convert", "Regenerate"]
martialSelfBoons = ["Bristle", "Evade"]
selfBoons = magicSelfBoons + martialSelfBoons


def execute(fighter, principal, ability) -> None: 
    phrase = ""

    fighter.commitments[ability]["targets"] += [principal]
    principal.effects[ability]["source"] = fighter

    match ability:
        case "Bristle" | "Evade" | "Guard": phrase = setGuard(fighter, principal, ability)
        case "Focus": phrase = setFocus(fighter, principal)
        # case "Heal" | "Regenerate": phrase = Apply.applyRegenerate(fighter, principal, ability)
        case "Shroud": phrase = setShroud(fighter, principal)
        case "Slip": phrase = setSlip(fighter, principal)
        case "Wreath": phrase = setWreath(fighter, principal, ability)

    Select.waitPrint(phrase)


def setFocus(fighter, principal) -> list:
    phrase = ""

    principal.effects["Focus"]["dice"] = fighter.atrb["cur_mag"]

    if fighter is principal: phrase = fighter.name + " focuses self."
    else: phrase = fighter.name + " focuses " + principal.name + "."

    return phrase


def setGuard(fighter, principal, ability) -> str:
    dice, phrase = fighter.atrb["cur_mar"], ""
    
    principal.effects["Guard"]["dice"] = dice
    principal.effects["Guard"]["source"] = fighter
    principal.effects["Guard"]["additional"] = ability
    fighter.commitments["Guard"]["targets"] += [principal]

    if ability == "Guard":
        if fighter is principal: phrase = fighter.name + " guards self."
        else: phrase = fighter.name + " guards " + principal.name + "."
    elif ability == "Evade":
        phrase = fighter.name + " evades."
    elif ability == "Bristle":
        phrase = fighter.name + " bristles."

    return phrase
    

def setShroud(fighter, principal) -> str:
    phrase = ""
    dice = fighter.atrb["cur_mag"]

    if fighter is principal: phrase = fighter.name + " shrouds self."
    else: phrase = fighter.name + " shrouds " + principal.name + "."

    principal.effects["Shroud"]["dice"] = dice
    principal.effects["Shroud"]["source"] = fighter
    fighter.commitments["Shroud"]["targets"] = principal
    fighter.actionQueue += [["boon", "Shroud", principal, 0]]

    return phrase


def setSlip(fighter, principal) -> str:
    # Let fighter move through obstacles but not stop on them.
    # create a temporary movement map in which all obstacles are replaced with smoke
    phrase = ""
    return phrase


def setWreath(fighter, principal, ability) -> str:
    phrase = ""
    dice = fighter.atrb["cur_mag"]
    dmgType = Damage.identifyDamageType(fighter, ability)["basic"]

    principal.effects["Wreath"].update({"dice": dice, "source": fighter, "additional": dmgType})
    fighter.commitments["Wreath"]["targets"] += [principal]

    if fighter is principal: phrase = fighter.name + " wreaths self."
    else: phrase = fighter.name + " wreaths " + principal.name + "."

    return phrase