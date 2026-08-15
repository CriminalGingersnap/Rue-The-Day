from Systems import PlayerSelect as Select
from . import Boons_Set as Boons
import random


martialHindrances = ["Bind", "Drain", "Harry"]
magicHindrances = ["Compel", "Confound", "Seal", "Stun"]


def commitDice(fighter, target, hindrance) -> None:
    dType = ""
    if hindrance in martialHindrances: dType = "cur_mar"
    elif hindrance in magicHindrances: dType = "cur_mag"

    newDice = Boons.blitzCommit(fighter, dType)
    trueHindrance = hindranceComment(fighter, target, hindrance)
    Boons.setBuff(fighter, target, newDice, hindrance, trueHindrance)


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