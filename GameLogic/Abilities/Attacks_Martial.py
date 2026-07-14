from . import Boons_Apply as Boons, Hindrances_Apply as Hinder, Reactions
from Systems import PlayerSelect as Select, Roll, Conditions, Damage


def getProbableAv(fighter, dmgType, target) -> int:
    probAv = getBaseAv("Bash", dmgType, target)

    probAv += target.effects["Guard"]["dice"] * 3
    probAv -= target.effects["Disorient"]["dice"] * 3
    probAv += target.effects["Wreath"]["dice"]

    probAv += fighter.effects["Misdirect"]["dice"] * 3
    probAv -= fighter.effects["Focus"]["dice"] * 3

    return probAv

def getBaseAv(attack, dmgType, target) -> int:
    av = (target.atrb["cur_av"] - target.atrb["injury"]) + target.equip["shield"]["modifier"]
    if (dmgType == "Pierce") and (attack != "Bodkin"): av += target.equip["armor"]["modifier"]

    return max(av, 0)


def attack(fighter, target, attack, dice) -> None:
    avIncrease = 0
    dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], attack)
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
        elif attempt >= (av + (av // 2)):
            baseDmg *= 5
            Select.waitPrint("Clean hit!")
        elif attempt >= av:
            baseDmg *= 4
            Select.waitPrint("Contact!")
        else: Select.waitPrint("Glancing blow!")

        if dmgType == fighter.atrb["cur_elm"]:
            baseDmg += fighter.equip["weapon"]["modifier"]
            inflict(fighter, target, dmgType, baseDmg)        
        else:
            inflict(fighter, target, dmgType, baseDmg)
            inflict(fighter, target, fighter.atrb["cur_elm"], fighter.equip["weapon"]["modifier"])

    else: Select.waitPrint("Attack misses!")

def inflict(fighter, target, dmgType, baseDmg):
    physicalAbsorption = Boons.applyWreath(target, dmgType)
    appliedDmg = max(0, baseDmg - physicalAbsorption)

    Select.waitPrint(fighter.props["name"] + " inflicts " + str(appliedDmg) + " " + dmgType + " damage!")
    Conditions.takeDamage(target, dmgType, appliedDmg)