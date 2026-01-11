from Systems import PlayerSelect as Select
from . import DamageTypes as Damage
import random


martialHindrance = ["Bind", "Harry"]
magicHindrance = ["Compel", "Disorient", "Misdirect", "Seal"]


def execute(fighter, target, ability) -> None:
    phrase = ""

    match ability:
        case "Bind" | "Misdirect": phrase = setMisdirect(fighter, target, ability)
        case "Compel": phrase = setCompel(fighter, target, ability)
        case "Disorient" | "Harry": phrase = setDisorient(fighter, target, ability)
        case "Seal": phrase = setSeal(fighter, target)

    Select.waitPrint(phrase)    


def setCompel(fighter, target, ability):
    dice = fighter.atrb["cur_mag"]

    fighter.commitments["Compel"]["targets"] += [target]
    target.effects["Compel"]["source"] = fighter
    target.effects["Compel"]["dice"] = dice

    return fighter.name + " attempts to compel " + target.name + "."


def setDisorient(fighter, target, ability):
    dice, dType, phrase = 0, "", fighter.name

    if ability == "Disorient":
        dice, dType = fighter.atrb["cur_mag"], "magic"
        phrase += " disorients "
    elif ability == "Harry":
        dice, dType = fighter.atrb["cur_mar"], "martial"
        phrase += " harries "

    dice = fighter.atrb[dType]

    fighter.commitments["Disorient"]["targets"] += [target]
    target.effects["Disorient"]["source"] = fighter
    target.effects["Disorient"]["dice"] = dice
    target.effects["Disorient"]["additional"] = ability

    return phrase + target.name + "."


def setMisdirect(fighter, target, ability) -> list:
    dice, dType, phrase = 0, "", fighter.name

    if ability == "Misdirect":
        dice, dType = fighter.atrb["cur_mag"], "magic"
        phrase += " misdirects "
    elif ability == "Bind":
        dice, dType = fighter.atrb["cur_mar"], "martial"
        phrase += " binds with "
    
    dice = fighter.atrb[dType]

    fighter.commitments["Misdirect"]["targets"] += [target]
    target.effects["Misdirect"]["source"] = fighter
    target.effects["Misdirect"]["dice"] = dice
    target.effects["Misdirect"]["additional"] = ability

    return phrase + target.name + "."


def setSeal(fighter, target):
    ability, phrase = "None", ""
    options = target.abl["Attacks"] + target.abl["Boons"] + target.abl["Hindrances"]

    if fighter.rank == "player":
        Select.waitPrint("Choose ability:")
        ability = Select.makeSelection(options + ["None"])
    else: ability = random.choice(options)

    if ability != "None":
        dice = fighter.atrb["cur_mag"]

        target.effects["Seal"]["dice"] = dice
        target.effects["Seal"]["source"] = fighter
        target.effects["Seal"]["additional"] = ability

        fighter.effects["Seal"]["dice"] = dice
        fighter.effects["Seal"]["source"] = fighter
        fighter.effects["Seal"]["additional"] = ability
        fighter.commitments["Seal"]["targets"] += [target, fighter]

        phrase = fighter.name + " attempts to seal " + target.name + "'s " + ability + " ability."    
    return phrase