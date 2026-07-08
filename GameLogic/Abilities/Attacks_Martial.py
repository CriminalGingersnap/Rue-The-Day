from . import DamageTypes as Damage, Boons_Apply as Boons, Hindrances_Apply as Hinder, Reactions
from Systems import PlayerSelect as Select, Roll, Conditions


def getProbableAv(fighter, dmgType, target) -> int:
    probAv = getBaseAv("Bash", dmgType, target)

    probAv += target.effects["Guard"]["dice"] * 3
    probAv -= target.effects["Disorient"]["dice"] * 3
    probAv += target.effects["Wreath"]["dice"]

    probAv += fighter.effects["Misdirect"]["dice"] * 3
    probAv -= fighter.effects["Focus"]["dice"] * 3

    return probAv

def getBaseAv(attack, dmgType, target) -> int:
    av = (target.atrb["cur_av"] - target.atrb["injury"]) + target.equipment["shield"]["modifier"]
    if (dmgType == "Pierce") and (attack != "Bodkin"): av += target.equipment["armor"]["modifier"]

    return max(av, 0)


def attack(fighter, target, attack, dice) -> None:
    avIncrease = 0
    dmgType = Damage.identifyDamageType(fighter, attack)
    av = getBaseAv(attack, dmgType, target)

    attemptIncrease = Boons.applyFocus(fighter)
    attemptReduction = Hinder.applyMisdirect(fighter)
    avIncrease = Boons.applyGuard(target)
    avReduction = Hinder.applyDisorient(target)

    Select.quickPrint("Attack roll:")
    attempt = Roll.roll(fighter, dice, attack, "martial")
    attempt += (attemptIncrease - attemptReduction)
    av += (avIncrease - avReduction)

    contact(fighter, target, dmgType, dice, attempt, av)
    
    if avIncrease > 0: Reactions.applyRiposte(target, fighter, "Guard")
    if attemptReduction > 0: Reactions.applyRiposte(target, fighter, "Misdirect")


def contact(fighter, target, dmgType, baseDmg, attempt, av):
    if attempt >= (av // 2):
        if attempt >= (av * 2):
            baseDmg *= 6
            Select.waitPrint("Devastating blow!")
        elif attempt >= av:
            baseDmg *= 3
            Select.waitPrint("Clean hit!")
        else: Select.waitPrint("Glancing blow!")

        physicalAbsorption = Boons.applyWreath(target, dmgType)
        appliedDmg = max(0, baseDmg - physicalAbsorption)

        Select.waitPrint(fighter.props["name"] + " inflicts " + str(appliedDmg) + " " + dmgType + " damage!")
        Conditions.takeDamage(target, dmgType, appliedDmg)

    else: Select.waitPrint("Attack misses!")