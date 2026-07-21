from Systems import PlayerSelect as Select, Damage
from . import Commitments

def decrementStamina(fighter, potency):
    for point in range(potency):
        if fighter.atrb["stamina"] > 1: fighter.atrb["stamina"] -= 1
        elif fighter.atrb["stamina"] == 1:
            fighter.atrb["fatigue"] += 1
            fighter.atrb["stamina"] = fighter.atrb["endurance"]
            Select.waitPrint(fighter.props["name"] + " gains a point of fatigue!")

def decrementTolerance(fighter, potency) -> None:
    for point in range(potency):
        if fighter.atrb["tolerance"] > 1: fighter.atrb["tolerance"] -= 1
        else:
            if fighter.atrb["tolerance"] == 1:
                fighter.atrb["corruption"] += 1
                fighter.atrb["tolerance"] = getTolerance(fighter)
                Select.waitPrint(fighter.props["name"] + " gains a point of instability!")
                Select.waitPrint("Magic rolls become unstable!")
    
    if fighter.atrb["corruption"] > 0:
        Select.waitPrint(fighter.props["name"] + " takes " + str(potency) + " Bleed damage!")
        takeDamage(fighter, "Bleed", potency)

def getTolerance(fighter) -> int:
    value = fighter.atrb["endurance"]
    if fighter.atrb["base_elm"] == "Basic": value *= 2
    return value


def recoverHP(principal, points):
    if points > 0:
        principal.atrb["cur_hp"] = min(principal.atrb["base_hp"], principal.atrb["cur_hp"] + points)
        Select.waitPrint(principal.props["name"] + " receives " + str(points) + " of healing.\n")

def takeDamage(target, dmgType, damage) -> None:
    damage = Damage.applyResistance(damage, dmgType, target)

    if dmgType != "Dream":
        target.atrb["cur_hp"] = target.atrb["cur_hp"] - damage
        setInjury(target)
    else: decrementStamina(target, damage)


def setInjury(target):
    injuryPhrase, speedPhrase, avPhrase = target.props["name"] + " is ", "Speed reduced ", "Avoidance reduced "
    print = False

    if target.atrb["quart_hp"] < target.atrb["cur_hp"] <= target.atrb["half_hp"]:
        if target.atrb["injury"] < 1:
            if target.cndt["lifeless"]: injuryPhrase += "damaged!"
            else: injuryPhrase += "injured!"
            speedPhrase += "by a quarter."
            avPhrase += "by 1."

            target.atrb["injury"] = 1
            print = True

    elif 0 < target.atrb["cur_hp"] <= target.atrb["quart_hp"]:
        if target.atrb["injury"] < 2:
            if target.cndt["lifeless"]: injuryPhrase += "critically damaged!"
            else: injuryPhrase += "critically injured!"
            speedPhrase += "by half."
            avPhrase += "by 2."

            target.atrb["injury"] = 2
            print = True

    elif -target.atrb["half_hp"] < target.atrb["cur_hp"] <= 0:
        if target.atrb["injury"] < 3:
            if target.cndt["lifeless"]: injuryPhrase += "catastrophically impaired!"
            else: injuryPhrase += "mortally wounded!"
            speedPhrase += "to 1."
            avPhrase += "by 3."

            target.atrb["injury"] = 3
            print = True

    elif target.atrb["cur_hp"] <= -target.atrb["half_hp"]:
        if target.cndt["lifeless"]: injuryPhrase += "destroyed!"
        else: injuryPhrase += "slain!"
        target.cndt["dead"] = True

        Commitments.clearCommitments(target)
        Select.waitPrint(injuryPhrase)

    if print:
        Select.waitPrint(injuryPhrase)
        if target.atrb["base_sp"] > 0: Select.quickPrint(speedPhrase)
        Select.quickPrint(avPhrase)
        Select.waitPrint(str(target.atrb["injury"]) + "-point penalty applied to rolls.\n")