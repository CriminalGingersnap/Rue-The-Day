from Systems import PlayerSelect as Select, Damage
import random

martialBoons = ["Bandage", "Conceal", "Evade", "Fortify", "Guard", "Rally"]
magicBoons = ["Focus", "Heal", "Regenerate", "Veil", "Wreath"]


def commitDice(fighter, principal, boon) -> None: 
    dType = ""
    if boon in martialBoons: dType = "cur_mar"
    elif boon in magicBoons: dType = "cur_mag"
    
    newDice = blitzCommit(fighter, dType)
    trueBoon = boonComment(fighter, principal, boon)
    setBuff(fighter, principal, newDice, boon, trueBoon)


def blitzCommit(fighter, dType):
    diceCap, newDice = fighter.atrb[dType], 0
    if fighter.cndt["blitzing"]:
        if (fighter.props["rank"] == "player"):
            Select.waitPrint("Commit dice(" + str(diceCap) + "):")
            newDice = Select.takeInput(1, diceCap)
        else: newDice = random.randint(1, diceCap)
    else: newDice = diceCap

    fighter.atrb[dType] -= newDice
    return newDice


def setBuff(fighter, target, newDice, ability, trueAbility) -> None:
    if newDice > target.effects[trueAbility]["dice"]:
        fighter.commits[trueAbility]["targets"] += [target]
        target.effects[trueAbility]["source"] = fighter
        target.effects[trueAbility]["ability"] = ability
        if ability == "Wreath":
            dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], ability)
            target.effects["Wreath"]["additional"] = dmgType

    target.effects[trueAbility]["dice"] += newDice


def boonComment(fighter, principal, boon) -> None:
    phrase, end = fighter.props["name"], principal.props["name"] + "!"
    if fighter == principal: end = "self!"
    trueBoon = boon

    match boon:
        case "Bandage":
            phrase += " bandages " + end
            trueBoon = "Heal"
        case "Conceal":
            phrase += " conceals " + end
            trueBoon = "Veil"
        case "Evade":
            phrase += " evades!"
            trueBoon = "Guard"
        case "Heal": phrase += " heals " + end
        case "Focus": phrase += " focuses " + end
        case "Fortify": phrase += " fortifies " + end
        case "Guard": phrase += " guards " + end
        case "Rally": phrase += " rallies " + end
        case "Regenerate":
            phrase += " regenerates!"
            trueBoon = "Heal"
        case "Veil": phrase += " veils " + end
        case "Wreath": phrase += " wreaths " + end

    Select.waitPrint(phrase)
    return trueBoon