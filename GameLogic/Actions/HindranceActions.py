from . import AttackActions, Sort
from Abilities import AttackAbilities as Attacks, Hindrances_Set as Hindrances, Hindrances_Apply as Hinder
from Systems import PlayerSelect as Select
import random


def pcSelectHindrance(fighter, enemies) -> str:
    hindranceOptions = usableHindrances(fighter, enemies)
    return Select.pickOption(hindranceOptions, "hindrance")


def npcSelectHindrance(fighter, enemies, allies):
    hindranceOptions = []
    useful, usable = usefulHindrances(fighter, enemies, allies), usableHindrances(fighter, enemies)

    for option in usable:
        if option in useful: hindranceOptions += [option]

    if len(hindranceOptions) == 0: return "None"
    else: return random.choice(hindranceOptions)


def usefulHindrances(fighter, enemies, allies):
    hindrancePreferences = []
    selfMar, allyMar = False, False

    for enemy in enemies:
        if any(attack in Attacks.martialAttack for attack in enemy.abl["attacks"]):
            hindrancePreferences += ["Harry", "Misdirect"]
        if canCompel(fighter, enemy):
            hindrancePreferences += ["Compel"]
            hindrancePreferences += ["Seal"]

    selfMar = any(attack in Attacks.martialAttack for attack in fighter.abl["attacks"])
    for ally in allies:
        allyMar = any(attack in Attacks.martialAttack for attack in ally.abl["attacks"])
         
    if selfMar or allyMar: hindrancePreferences += ["Bind", "Disorient"]

    return hindrancePreferences


def usableHindrances(fighter, enemies) -> list:
    affordableHindrances, usableHindrances = [], []

    if fighter.atrb["cur_mar"] > 0:
        affordableHindrances += Hindrances.martialHindrances
    if (fighter.atrb["cur_mag"] > 0) and AttackActions.weaponAllows(fighter, "Bring"):
        affordableHindrances += Hindrances.magicHindrances

    for hindrance in fighter.abl["hindrances"]:
        if (hindrance in affordableHindrances) and Sort.canReachAny(fighter, enemies, hindrance):
            usableHindrances += [hindrance]

    return usableHindrances


def canCompel(fighter, enemy) -> bool:
    canCompel = False
    if enemy.cndt["sapient"]: canCompel = False
    elif fighter.atrb["cur_elm"] == "Holy": canCompel = True
    elif enemy.atrb["cur_elm"] != "Holy":
        if (fighter.atrb["cur_elm"] == "Flame") and (enemy.atrb["cur_elm"] != "Ice"): canCompel = True
        elif (fighter.atrb["cur_elm"] == "Dream") and (enemy.atrb["cur_elm"] != "Rot"): canCompel = True
        elif (fighter.atrb["cur_elm"] == "Ice") and (enemy.atrb["cur_elm"] != "Flame"): canCompel = True
        elif (fighter.atrb["cur_elm"] == "Rot"): canCompel = True

    return canCompel