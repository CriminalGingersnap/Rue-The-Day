from Systems import PlayerSelect as Select
import random


martialHindrances = ["Bind", "Harry"]
magicHindrances = ["Compel", "Confuse", "Confound", "Seal"]


def commitDice(fighter, target, hindrance) -> None:
    newDice, diceCap = 0, 0

    if hindrance in martialHindrances: diceCap = fighter.atrb["cur_mar"]
    elif hindrance in magicHindrances: diceCap = fighter.atrb["cur_mag"]

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


def hindranceComment(fighter, target, hindrance) -> str:
    phrase, end = fighter.props["name"], target.props["name"] + "!"
    trueHindrance = hindrance

    match hindrance:
        case "Bind":
            phrase += " binds with " + end
            trueHindrance = "Confound"
        case "Compel": phrase += " attempts to compel " + end
        case "Confound": phrase += " confounds " + end
        case "Confuse": phrase += " confuses " + end
        case "Harry":
            phrase += " harries " + end
            trueHindrance = "Confuse"
        case "Seal": 
            phrase += " attempts to seal " + end
            trueHindrance = "Compel"

    Select.waitPrint(phrase)
    return trueHindrance 

