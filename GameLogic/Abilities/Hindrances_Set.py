from Systems import PlayerSelect as Select
import random


martialHindrances = ["Bind", "Drain", "Harry"]
magicHindrances = ["Compel", "Confound", "Seal", "Stun"]


def commitDice(fighter, target, hindrance) -> None:
    newDice, diceCap, dType = 0, 0, ""

    if hindrance in martialHindrances: dType = "cur_mar"
    elif hindrance in magicHindrances: dType = "cur_mag"
    diceCap = fighter.atrb[dType]

    if fighter.cndt["blitzing"]:
        if (fighter.props["rank"] == "player"):
            Select.waitPrint("Commit dice(" + str(diceCap) + "):")
            newDice = Select.takeInput(1, diceCap)
        else: newDice = random.randint(1, diceCap)
    else: newDice = diceCap

    trueHindrance = hindranceComment(fighter, target, hindrance)

    if newDice > target.effects[trueHindrance]["dice"]:
        fighter.commits[trueHindrance]["targets"] += [target]
        target.effects[trueHindrance]["source"] = fighter
        target.effects[trueHindrance]["ability"] = hindrance

    target.effects[trueHindrance]["dice"] += newDice
    fighter.atrb[dType] -= newDice


def hindranceComment(fighter, target, hindrance) -> str:
    phrase, end = fighter.props["name"], target.props["name"] + "!"
    trueHindrance = hindrance

    match hindrance:
        case "Bind":
            phrase += " binds with " + end
            trueHindrance = "Confound"
        case "Compel": phrase += " attempts to compel " + end
        case "Confound": phrase += " confounds " + end
        case "Drain": phrase += " drains spent vitality from " + end
        case "Harry":
            phrase += " harries " + end
            trueHindrance = "Stun"
        case "Seal": 
            phrase += " attempts to seal " + end
            trueHindrance = "Compel"
        case "Stun": phrase += " stuns " + end

    Select.waitPrint(phrase)
    return trueHindrance