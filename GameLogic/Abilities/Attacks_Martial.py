from . import Boons_Apply as Boons, Hindrances_Apply as Hinder, AttackAbilities as Attacks
from Systems import PlayerSelect as Select, Roll, Conditions, Damage
from Actions import AttackActions
from Maps import Movement
import random


def getProbableAv(fighter, dmgType, target) -> int:
    probAv = getBaseAv("Bash", dmgType, target)

    probAv += target.effects["Guard"]["dice"] * 3
    probAv -= target.effects["Confuse"]["dice"] * 3
    probAv += target.effects["Wreath"]["dice"]

    probAv += fighter.effects["Confound"]["dice"] * 3
    probAv -= fighter.effects["Focus"]["dice"] * 3

    if fighter.cndt["aquatic"]:
        if fighter.cndt["submerged"]: probAv += 2
        else: probAv -= 2

    return probAv

def getBaseAv(attack, dmgType, target) -> int:
    av = (target.atrb["cur_av"] - target.atrb["injury"]) + target.equip["shield"]["modifier"]
    if (dmgType == "Pierce") and (attack != "Bodkin"): av += target.equip["armor"]["modifier"]

    if target.cndt["aquatic"]:
        if target.cndt["submerged"]: av += 2
        else: av -= 2

    return max(av, 0)


def attack(fighter, target, attack, dice) -> None:
    avIncrease = 0
    dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], attack)
    av = getBaseAv(attack, dmgType, target)

    attemptIncrease = Boons.applyFocus(fighter)
    attemptReduction = Hinder.applyConfound(fighter)
    avIncrease = Boons.applyGuard(target)
    avReduction = Hinder.applyConfuse(target)

    Select.quickPrint("Attack roll:")
    attempt = Roll.roll(fighter, dice, attack, "martial")
    attempt += (attemptIncrease - attemptReduction)
    av += (avIncrease - avReduction)

    contact(fighter, target, dmgType, dice, attempt, av)
    applyRiposte(fighter, target)


def contact(fighter, target, dmgType, baseDmg, attempt, av):
    phrase = " against " + target.props["name"] + "!"
    if attempt >= (av // 2):
        if attempt >= (av * 2):
            baseDmg *= 6
            Select.waitPrint("Devastating blow" + phrase)
        elif attempt >= (av + (av // 2)):
            baseDmg *= 5
            Select.waitPrint("Clean hit" + phrase)
        elif attempt >= av:
            baseDmg *= 4
            Select.waitPrint("Contact" + phrase)
        else: Select.waitPrint("Glancing blow" + phrase)

        if dmgType == fighter.atrb["cur_elm"]:
            baseDmg += fighter.equip["weapon"]["modifier"]
            inflict(fighter, target, dmgType, baseDmg)
        else:
            inflict(fighter, target, dmgType, baseDmg)
            if target.atrb["cur_hp"] > -target.atrb["half_hp"]:
                bonusDmgType = fighter.atrb["cur_elm"]
                if fighter.atrb["cur_elm"] == "Basic": bonusDmgType = "Bleed"
                inflict(fighter, target, bonusDmgType, fighter.equip["weapon"]["modifier"])

    else: Select.waitPrint("Attack misses" + phrase)


def inflict(fighter, target, dmgType, baseDmg):
    physicalAbsorption = Boons.applyWreath(target, dmgType)
    appliedDmg = max(0, baseDmg - physicalAbsorption)

    Select.waitPrint(fighter.props["name"] + " inflicts " + str(appliedDmg) + " " + dmgType + " damage!")
    Conditions.takeDamage(target, dmgType, appliedDmg)


def applyRiposte(attacker, defender) -> None:
    guardian = defender.effects["Guard"]["source"]
    guardDice = defender.effects["Guard"]["dice"]

    if (guardian != "None") and (guardDice > 0) and ("Riposte" in guardian.abl["reactions"]) :
        guardDistance = Movement.getTargetDistance(guardian, attacker)
        if guardDistance <= guardian.equip["weapon"]["reach"]: respond(guardian, guardDice, "Guard", attacker, defender)

    confounder = attacker.effects["Confound"]["source"]
    ability = attacker.effects["Confound"]["additional"]
    bindDice = attacker.effects["Confound"]["dice"]

    if (confounder != "None") and (ability == "Bind") and (bindDice > 0) and ("Riposte" in confounder.abl["reactions"]) :
        bindDistance = Movement.getTargetDistance(confounder, attacker)
        if bindDistance <= confounder.equip["weapon"]["reach"]: respond(confounder, bindDice, "Bind", attacker, defender)


def respond(source, dice, ability, target, principal):
    expense, proceed = 0, True

    if source.props["rank"] == "player":
        proceed = Select.yesNo("Trigger riposte?")

        if proceed:
            attackChoice = AttackActions.pcSelectAttack(source)
            Select.waitPrint("Expend dice (" + str(dice) + "):")
            expense = Select.takeInput(1, dice)
    else:
        attackChoice = AttackActions.npcSelectAttack(source, target)
        expense = random.randint(1, dice)

    if proceed:
        Attacks.execute(source, target, attackChoice, expense)
        principal.effects[ability]["dice"] -= expense