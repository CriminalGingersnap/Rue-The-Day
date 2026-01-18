from . import AttackActions, Sort
from Abilities import AttackAbilities as Attacks, Hindrances_Set as Hindrances, Hindrances_Apply as Hinder, DamageTypes as Damage
from Systems import PlayerSelect as Select
import random


def pcSelectHindrance(fighter, enemies) -> str:
    hindranceOptions = usableHindrances(fighter, enemies)

    if len(hindranceOptions) == 1: return hindranceOptions[0]
    else:
        Select.waitPrint("Choose Hindrance:")
        answer = Select.makeSelection(hindranceOptions)
        return answer


def npcSelectHindrance(fighter, enemies, allies):
    hindranceOptions = []
    useful, usable = usefulHindrances(fighter, enemies, allies), usableHindrances(fighter, enemies)

    for option in usable:
        if option in useful: hindranceOptions += [option]

    if hindranceOptions != []: return random.choice(hindranceOptions)
    else: return "None"


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
            usable = False

            if hindrance in ["Compel", "Seal"]:
                compelTargets = compellableTargets(enemies, hindrance)
                if len(compelTargets > 0): usable = True
            else: usable = True
            
            if usable: usableHindrances += [hindrance]

    return usableHindrances


def npcSelectHindranceTarget(fighter, enemies, hindrance):
    targets = compellableTargets(fighter, enemies, hindrance) 
    return AttackActions.npcSelectAttackTarget(fighter, targets)

def compellableTargets(fighter, enemies):
    compelTargets = []
    for enemy in enemies:
        if canCompel(fighter, enemy): compelTargets += [enemy]

    return compelTargets

def canCompel(fighter, enemy) -> bool:
    canCompel = False
    if fighter.atrb["cur_elm"] == "Blessed": True
    elif enemy.atrb["cur_elm"] != "Blessed":
        if (fighter.atrb["cur_elm"] == "Flame") and (enemy.atrb["cur_elm"] != "Ice"): True
        elif (fighter.atrb["cur_elm"] == "Fey") and (enemy.atrb["cur_elm"] != "Corpse"): True
        elif (fighter.atrb["cur_elm"] == "Ice") and (enemy.atrb["cur_elm"] != "Flame"): True
        elif (fighter.atrb["cur_elm"] in ["Corpse", "Venom"]): True

    return canCompel