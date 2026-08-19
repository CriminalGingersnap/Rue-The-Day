from . import Boons_Apply as Boons, Hindrances_Apply as Hinder, AttackAbilities as Attacks
from Systems import PlayerSelect as Select, Roll, Conditions, Damage, Sort
from Actions import AttackActions
from Maps import Movement
import random


def getProbableAv(fighter, dmgType, target) -> int:
    probAv = getBaseAv("Bash", dmgType, target)

    probAv += target.effects["Guard"]["dice"] * 3
    probAv -= target.effects["Stun"]["dice"] * 3
    probAv += fighter.effects["Confound"]["dice"] * 3
    probAv -= fighter.effects["Focus"]["dice"] * 3

    return probAv

def getBaseAv(attack, dmgType, target) -> int:
    av = (target.atrb["cur_av"] - target.atrb["injury"]) + target.equip["shield"]["modifier"]
    if (dmgType == "Pierce") and (attack != "Bodkin"): av += target.equip["armor"]["modifier"]

    av += target.itemEffects["Obscure"]["potency"]

    if target.cndt["aquatic"]:
        if target.cndt["submerged"]: av += 2
        else: av -= 2

    return max(av, 0)


def attack(fighter, target, attack, dice) -> None:
    avIncrease = 0
    dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], attack)
    av = getBaseAv(attack, dmgType, target)

    Select.quickPrint("Attack roll:")
    attempt = Roll.roll(fighter, target, dice, attack, "martial")

    attemptIncrease = Boons.applyFocus(fighter)
    attemptReduction = Hinder.applyConfound(fighter)
    attempt += (attemptIncrease - attemptReduction)

    avIncrease = Boons.applyGuard(target)
    avReduction = Hinder.applyStun(target)
    av += (avIncrease - avReduction)

    contact(fighter, target, dmgType, dice, attempt, av)
    applyRiposte(fighter, target)


def contact(fighter, target, dmgType, baseDmg, attempt, av):
    phrase = " against " + target.props["name"] + "!"
    if attempt >= (av // 4):
        if attempt >= (av * 2):
            baseDmg *= 6
            Select.waitPrint("Devastating blow" + phrase)
        elif attempt >= (av + (av // 2)):
            baseDmg *= 5
            Select.waitPrint("Clean hit" + phrase)
        elif attempt >= av:
            baseDmg *= 4
            Select.waitPrint("Contact" + phrase)
        elif attempt >= av // 2:
            baseDmg *= 2
            Select.waitPrint("Partial hit" + phrase)
        else: Select.waitPrint("Glancing blow" + phrase)

        if dmgType == fighter.atrb["cur_elm"]:
            baseDmg += fighter.equip["weapon"]["modifier"]
            inflict(fighter, target, dmgType, baseDmg)
        else:
            inflict(fighter, target, dmgType, baseDmg)
            bonusDmgType = fighter.atrb["cur_elm"]
            if fighter.atrb["cur_elm"] == "Basic": bonusDmgType = "Bleed"
            inflict(fighter, target, bonusDmgType, fighter.equip["weapon"]["modifier"])

    else: Select.waitPrint("Attack misses" + phrase)


def inflict(fighter, target, dmgType, baseDmg):
    if baseDmg > 0:
        physicalAbsorption = Boons.applyWreath(target, dmgType)
        appliedDmg = max(0, baseDmg - physicalAbsorption)

        Select.waitPrint(" " + fighter.props["name"] + " inflicts " + str(appliedDmg) + " " + dmgType + " damage!")
        Conditions.takeDamage(target, dmgType, appliedDmg)


def applyRiposte(attacker, defender) -> None:
    guardian = defender.effects["Guard"]["source"]
    guardDice = defender.effects["Guard"]["dice"]

    if (guardian != "None") and (guardDice > 0) and ("Riposte" in guardian.abl["reactions"]) :
        reachable = Movement.getTargetDistance(guardian, attacker) <= guardian.equip["weapon"]["reach"]
        visible = Sort.isVisible(attacker, guardian.sightMap)
        if reachable and visible: respond(guardian, guardDice, "Guard", attacker, defender)

    confounder = attacker.effects["Confound"]["source"]
    ability = attacker.effects["Confound"]["additional"]
    bindDice = attacker.effects["Confound"]["dice"]

    if (confounder != "None") and (ability == "Bind") and (bindDice > 0) and ("Riposte" in confounder.abl["reactions"]) :
        bindDistance = Movement.getTargetDistance(confounder, attacker)
        if bindDistance <= confounder.equip["weapon"]["reach"]: respond(confounder, bindDice, "Bind", attacker, defender)


def respond(source, dice, ability, target, principal):
    expense = 0

    if source.props["rank"] == "player":
        Select.waitPrint("Expend dice (" + str(dice) + ") to riposte:")
        expense = Select.takeInput(0, dice)
        source.atrb["cur_mar"] = expense
        attackChoice = AttackActions.pcSelectAttack(source, [target])
    else:
        expense = random.randint(1, dice)
        source.atrb["cur_mar"] = expense
        attackChoice = AttackActions.npcSelectAttack(source, target)

    if expense > 0:
        Attacks.execute(source, target, attackChoice, expense)
        principal.effects[ability]["dice"] -= expense