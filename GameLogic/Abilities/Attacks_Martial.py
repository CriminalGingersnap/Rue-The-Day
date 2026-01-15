from . import DamageTypes as Damage, Boons_Apply as Boons, Hindrances_Apply as Hinder, Reactions
from Actions import AssessTargets as Assess
from Systems import PlayerSelect as Select, Roll, Conditions


def getProbableAv(fighter, dmgType, target) -> int:
    probAv = getBaseAv("Bash", dmgType, target)

    probAv += target.effects["Guard"]["dice"] * 3
    probAv -= target.effects["Disorient"]["dice"] * 3
    probAv += fighter.effects["Misdirect"]["dice"] * 3
    probAv -= fighter.effects["Focus"]["dice"] * 3

    return probAv

def getBaseAv(attack, dmgType, target) -> int:
    av = (target.atrb["cur_av"] - target.atrb["injury"]) + target.equipment["shield"]["modifier"]
    if (dmgType == "Pierce") and (attack != "Bodkin"): av += target.equipment["armor"]["modifier"]

    return max(av, 0)


def attack(fighter, target, attack, dice) -> None:
    bonusSource, avIncrease = fighter, 0
    dmgType = Damage.identifyDamageType(fighter, attack)
    av = getBaseAv(attack, dmgType, target)

    attemptIncrease = Boons.applyFocus(fighter)
    attemptReduction = Hinder.applyMisdirect(fighter)
    avIncrease = Boons.applyGuard(target)
    avReduction = Hinder.applyDisorient(target)

    attempt = Roll.roll(fighter, dice, attack, "martial")
    attempt += (attemptIncrease - attemptReduction)
    av += (avIncrease - avReduction)

    if attempt >= av: contact(fighter, target, dmgType, bonusSource, dice)   
    else:
        Select.waitPrint("Attack misses!")
        if avIncrease > 0: Reactions.applyRiposte(target, fighter, "Guard")
        if attemptReduction > 0: Reactions.applyRiposte(target, fighter, "Misdirect")


def contact(fighter, target, dmgType, bonusSource, dice):
    massive = fighter.cndt["massive"]
    baseDmgType, bonusDmgType = dmgType["base"], dmgType["bonus"]

    Select.waitPrint("Attack hits!")

    baseDmg = (3 + fighter.equipment["weapon"]["modifier"]) * dice
    physicalAbsorption = Boons.applyWreath(target, dmgType)
    appliedDmg = max(0, baseDmg - physicalAbsorption) 

    Select.waitPrint(fighter.name + " inflicts " + str(appliedDmg) + " " + baseDmgType + " damage!")
    Conditions.takeDamage(target, baseDmgType, appliedDmg, massive)
    
    if bonusDmgType != "None":
        Select.waitPrint("Attack deals bonus " + bonusDmgType + " damage!")
        bonusDmg = Roll.roll(bonusSource, dice, bonusDmgType, "magic")
        bonusDmg -= Boons.applyWreath(target, bonusDmgType)

        if bonusDmg > 0: Select.waitPrint(fighter.name + " inflicts " + str(bonusDmg) + " " + bonusDmgType + " damage!")
        Conditions.takeDamage(target, bonusDmgType, bonusDmg, False)