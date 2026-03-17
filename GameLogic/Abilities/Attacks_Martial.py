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

    if attempt >= av // 2:
        if attempt >= av: contact(fighter, target, dmgType, dice, True)
        else: contact(fighter, target, dmgType, dice, False)
    else: Select.waitPrint("Attack misses!")    

    if avIncrease > 0: Reactions.applyRiposte(target, fighter, "Guard")
    if attemptReduction > 0: Reactions.applyRiposte(target, fighter, "Misdirect")


def contact(fighter, target, dmgType, baseDmg, cleanHit):
    bonusDmgType = "None"

    if cleanHit:
        baseDmg *= 3
        bonusDmgType = Damage.identifyBonusDamageType(fighter, dmgType)
        Select.waitPrint("Attack hits cleanly!")
    else: Select.waitPrint("Attack barely connects!")

    physicalAbsorption = Boons.applyWreath(target, dmgType)
    appliedDmg = max(0, baseDmg - physicalAbsorption)

    Select.waitPrint(fighter.name + " inflicts " + str(appliedDmg) + " " + dmgType + " damage!")
    Conditions.takeDamage(target, dmgType, appliedDmg)

    if bonusDmgType != "None":
        Select.waitPrint("Attack inflicts additional " + str(baseDmg) + " " + bonusDmgType + " damage!")
        Conditions.takeDamage(target, bonusDmgType, baseDmg)