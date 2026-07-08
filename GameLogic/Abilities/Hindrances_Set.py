from Systems import PlayerSelect as Select
from . import DamageTypes as Damage
import random


martialHindrances = ["Bind", "Harry"]
magicHindrances = ["Compel", "Disorient", "Misdirect", "Seal"]


def commitDice(fighter, target, hindrance) -> None:
    newDice = 0

    if hindrance in martialHindrances: newDice = fighter.atrb["cur_mar"]
    elif hindrance in magicHindrances: newDice = fighter.atrb["cur_mag"]

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
            trueHindrance = "Misdirect"
        case "Compel": phrase += " attempts to compel " + end
        case "Disorient": phrase += " disorients " + end
        case "Harry":
            phrase += " harries " + end
            trueHindrance = "Disorient"
        case "Misdirect": phrase += " misdirects " + end
        case "Seal": 
            phrase += " attempts to seal " + end
            trueHindrance = "Compel"

    Select.waitPrint(phrase)
    return trueHindrance 

