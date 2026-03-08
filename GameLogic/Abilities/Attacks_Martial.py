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
    dmgTypes = Damage.identifyDamageType(fighter, attack)
    av = getBaseAv(attack, dmgTypes["base"], target)

    attemptIncrease = Boons.applyFocus(fighter)
    attemptReduction = Hinder.applyMisdirect(fighter)
    avIncrease = Boons.applyGuard(target)
    avReduction = Hinder.applyDisorient(target)

    Select.quickPrint("Attack roll:")
    attempt = Roll.roll(fighter, dice, attack, "martial")
    attempt += (attemptIncrease - attemptReduction)
    av += (avIncrease - avReduction)

    if attempt >= av // 2:
        baseDmg = dice
        if attempt >= av:
            baseDmg *= 3
            Select.waitPrint("Attack hits cleanly!")
        else:
            dmgTypes["bonus"] = "None"
            Select.waitPrint("Attack barely connects!")
        contact(fighter, target, dmgTypes, bonusSource, baseDmg)
    else: Select.waitPrint("Attack misses!")    

    if avIncrease > 0: Reactions.applyRiposte(target, fighter, "Guard")
    if attemptReduction > 0: Reactions.applyRiposte(target, fighter, "Misdirect")


def contact(fighter, target, dmgTypes, bonusSource, baseDmg):
    baseDmgType, bonusDmgType = dmgTypes["base"], dmgTypes["bonus"]    

    physicalAbsorption = Boons.applyWreath(target, baseDmgType)
    appliedDmg = max(0, baseDmg - physicalAbsorption) 

    Select.waitPrint(fighter.name + " inflicts " + str(appliedDmg) + " " + baseDmgType + " damage!")
    Conditions.takeDamage(target, baseDmgType, appliedDmg)
    
    if (bonusDmgType != "None"):
        Select.waitPrint("Attack deals bonus " + bonusDmgType + " damage!")
        bonusDmg = Roll.roll(bonusSource, 1, bonusDmgType, "magic")
        bonusDmg -= Boons.applyWreath(target, bonusDmgType)

        if bonusDmg > 0: Select.waitPrint(fighter.name + " inflicts " + str(bonusDmg) + " " + bonusDmgType + " damage!")
        Conditions.takeDamage(target, bonusDmgType, bonusDmg)