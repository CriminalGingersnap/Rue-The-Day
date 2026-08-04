from Systems import PlayerSelect as Select, Damage
import random

martialBoons = ["Conceal", "Guard"]
magicBoons = ["Focus", "Heal", "Regenerate", "Veil", "Wreath"]


def commitDice(fighter, principal, boon) -> None: 
    newDice, diceCap, dType = 0, 0, ""

    if boon in martialBoons: dType = "cur_mar"
    elif boon in magicBoons: dType = "cur_mag"
    diceCap = fighter.atrb[dType]
    
    if fighter.cndt["blitzing"]:
        if (fighter.props["rank"] == "player"):
            Select.waitPrint("Commit dice(" + str(diceCap) + "):")
            newDice = Select.takeInput(1, diceCap)
        else: newDice = random.randint(1, diceCap)
    else: newDice = diceCap

    trueBoon = boonComment(fighter, principal, boon)

    if newDice > principal.effects[trueBoon]["dice"]:
        fighter.commits[trueBoon]["targets"] += [principal]
        principal.effects[trueBoon]["source"] = fighter
        principal.effects[trueBoon]["ability"] = boon
        if boon == "Wreath":
            dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], boon)
            principal.effects["Wreath"]["additional"] = dmgType

    principal.effects[trueBoon]["dice"] += newDice
    fighter.atrb[dType] -= newDice


def boonComment(fighter, principal, boon) -> None:
    phrase, end = fighter.props["name"], principal.props["name"] + "!"
    if fighter == principal: end = "self!"
    trueBoon = boon

    match boon:
        case "Conceal":
            phrase += " conceals " + end
            trueBoon = "Veil"
        case "Heal": phrase += " heals " + end
        case "Focus": phrase += " focuses " + end
        case "Guard": phrase += " guards " + end
        case "Regenerate":
            phrase += " regenerates!"
            trueBoon = "Heal"
        case "Veil": phrase += " veils " + end
        case "Wreath": phrase += " wreaths " + end

    Select.waitPrint(phrase)
    return trueBoon