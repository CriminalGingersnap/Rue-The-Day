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
                fighter.atrb["tolerance"] = fighter.atrb["endurance"]
                Select.waitPrint(fighter.props["name"] + " gains a point of instability!")
                Select.waitPrint("Magic rolls lose stability!")

    corruption = fighter.atrb["corruption"]
    if corruption > 0:
        Select.waitPrint(fighter.props["name"] + " takes " + str(corruption) + " Bleed damage!")
        takeDamage(fighter, "Bleed", corruption)


def recoverHP(principal, points):
    if points > 0:
        principal.atrb["cur_hp"] = min(principal.atrb["base_hp"], principal.atrb["cur_hp"] + points)
        Select.waitPrint(principal.props["name"] + " receives " + str(points) + " of healing.\n")

def recoverStamina(principal, points):
    if points > 0:
        principal.atrb["stamina"] = min(principal.atrb["base_hp"], principal.atrb["stamina"] + points)
        Select.waitPrint(principal.props["name"] + " rallies for " + str(points) + " of stamina.\n")

def recoverTolerance(principal, points):
    if points > 0:
        principal.atrb["tolerance"] = min(principal.atrb["base_hp"], principal.atrb["tolerance"] + points)
        Select.waitPrint(principal.props["name"] + " fortifies for " + str(points) + " of tolerance.\n")


def takeDamage(target, dmgType, damage) -> None:
    damage = Damage.applyResistance(damage, dmgType, target)

    if dmgType != "Dream": target.atrb["cur_hp"] = target.atrb["cur_hp"] - damage
    else: decrementStamina(target, damage)


def setInjury(target):
    injuryPhrase, speedPhrase, avPhrase = "\n" + target.props["name"] + " is ", "Speed reduced ", "Avoidance reduced "
    print = False

    if target.atrb["half_hp"] < target.atrb["cur_hp"] <= (target.atrb["half_hp"] + target.atrb["quart_hp"]):
        if target.atrb["injury"] < 1:
            if target.cndt["lifeless"]: injuryPhrase += "lightly damaged!"
            else: injuryPhrase += "lightly injured!"
            speedPhrase += "by a quarter."
            avPhrase += "by 1."

            target.atrb["injury"] = 1
            print = True

    elif target.atrb["quart_hp"] < target.atrb["cur_hp"] <= target.atrb["half_hp"]:
        if target.atrb["injury"] < 2:
            if target.cndt["lifeless"]: injuryPhrase += "severely damaged!"
            else: injuryPhrase += "severely injured!"
            speedPhrase += "by half."
            avPhrase += "by 2."

            target.atrb["injury"] = 2
            print = True

    elif 0 < target.atrb["cur_hp"] <= target.atrb["quart_hp"]:
        if target.atrb["injury"] < 3:
            if target.cndt["lifeless"]: injuryPhrase += "critically damaged!"
            else: injuryPhrase += "critically injured!"
            speedPhrase += "by three quarters."
            avPhrase += "by 3."

            target.atrb["injury"] = 3
            print = True

    elif -target.atrb["half_hp"] < target.atrb["cur_hp"] <= 0:
        if target.atrb["injury"] < 4:
            if target.cndt["lifeless"]: injuryPhrase += "catastrophically impaired!"
            else: injuryPhrase += "mortally wounded!"
            speedPhrase += "to 1."
            avPhrase += "by 4."

            target.atrb["injury"] = 4
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