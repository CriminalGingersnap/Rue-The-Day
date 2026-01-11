from Systems import PlayerSelect as Select
from Abilities import Reactions, DamageTypes as Damage


def decrementStamina(fighter, potency):
    for point in range(potency):
        if fighter.atrb["stamina"] > 1: fighter.atrb["stamina"] -= 1
        elif fighter.atrb["stamina"] == 1:
            fighter.atrb["fatigue"] += 1
            fighter.atrb["stamina"] = fighter.atrb["endurance"]
            Select.waitPrint(fighter.name + " gains a point of fatigue!")

def decrementTolerance(fighter, potency) -> None:
    for point in range(potency):
        if fighter.atrb["tolerance"] > 1: fighter.atrb["tolerance"] -= 1
        else:
            if fighter.atrb["tolerance"] == 1:
                fighter.atrb["corruption"] += 1
                fighter.atrb["tolerance"] = getTolerance(fighter)
                Select.waitPrint(fighter.name + " gains a point of instability!")
                Select.waitPrint("Magic rolls become unstable!")
    
    if fighter.atrb["corruption"] > 0:
        Select.waitPrint(fighter.name + " takes " + str(potency) + " Bleed damage!")
        takeDamage(fighter, "Bleed", potency, False)

def getTolerance(fighter) -> int:
    value = fighter.atrb["endurance"]
    if fighter.atrb["base_elm"] == "Basic": value *= 2
    return value


def takeDamage(target, dmgType, damage, massive) -> None:
    damage = Damage.applyResistance(damage, dmgType, target)

    if dmgType != "Dream":
        target.atrb["cur_hp"] = target.atrb["cur_hp"] - damage
        setInjury(target)
    else: decrementStamina(target, damage)


def setInjury(target):
    phrase1, phrase2 = target.name + " is ", "Speed reduced "

    if target.atrb["quart_hp"] < target.atrb["cur_hp"] <= target.atrb["half_hp"]:
        if target.atrb["injury"] < 1:
            phrase1 += "injured!"
            phrase2 += "by a quarter. AV reduced by 1. "
            target.atrb["injury"] = 1
    elif 0 < target.atrb["cur_hp"] <= target.atrb["quart_hp"]:
        if target.atrb["injury"] < 2:
            phrase1 += "critically injured!"
            phrase2 += "by half. AV reduced by 2. "
            target.atrb["injury"] = 2
    elif target.atrb["cur_hp"] <= 0:
        if target.atrb["injury"] < 3:
            phrase1 += "mortally wounded!"
            phrase2 += "to 0. AV reduced by 3. "
            target.atrb["injury"] = 3

    Select.waitPrint(phrase1)
    Select.waitPrint(phrase2 + "Penalty applied to martial rolls.")

