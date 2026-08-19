from . import AttackActions
from Abilities import AttackAbilities as Attacks, Hindrances_Set as Hindrances
from Systems import PlayerSelect as Select, Sort
import random


def pcSelectHindrance(fighter, enemies) -> str:
    hindranceOptions = usableHindrances(fighter, enemies)

    if len(enemies) == 1:
        for option in range(len(hindranceOptions)):
            hindranceOptions[option] = hindranceOptions[option] + " -> " + enemies[0].props["name"]

    answer = Select.pickOption(hindranceOptions, "hindrance ability", False).split(" -> ")[0]
    return answer


def npcSelectHindrance(fighter, enemies, allies):
    useful, usable = usefulHindrances(fighter, enemies, allies), usableHindrances(fighter, enemies)
    hindranceOptions = [option for option in usable if option in useful]

    if len(hindranceOptions) == 0: return "None"
    else: return random.choice(hindranceOptions)


def usefulHindrances(fighter, enemies, allies):
    hindrancePreferences = []
    selfMar, allyMar = False, False

    for enemy in enemies:
        if any(attack in Attacks.martialAttack for attack in enemy.abl["attacks"]): hindrancePreferences += ["Bind", "Confound"]
        if canCompel(fighter, enemy, "Compel"): hindrancePreferences += ["Compel"]
        if canCompel(fighter, enemy, "Seal"): hindrancePreferences += ["Seal"]
        if enemy.atrb["cur_hp"] < enemy.atrb["base_hp"]: hindrancePreferences += ["Drain"]

    selfMar = any(attack in Attacks.martialAttack for attack in fighter.abl["attacks"])
    for ally in allies:
        allyMar = any(attack in Attacks.martialAttack for attack in ally.abl["attacks"])
         
    if selfMar or allyMar: hindrancePreferences += ["Harry", "Stun"]

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


def canCompel(fighter, enemy, ability) -> bool:
    canCompel = False
    if enemy.cndt["inviolable"] and (ability == "Compel"): canCompel = False
    elif enemy.atrb["cur_elm"] != "Holy":
        if (fighter.atrb["cur_elm"] == "Flame") and (enemy.atrb["cur_elm"] != "Ice"): canCompel = True
        elif (fighter.atrb["cur_elm"] == "Ice") and (enemy.atrb["cur_elm"] != "Flame"): canCompel = True
        elif (fighter.atrb["cur_elm"] == "Bleed") and (enemy.atrb["cur_elm"] != "Rot"): canCompel = True
        elif (fighter.atrb["cur_elm"] == "Rot") and (enemy.atrb["cur_elm"] != "Bleed"): canCompel = True
        elif fighter.atrb["cur_elm"] == "Dream": canCompel = True

    return canCompel