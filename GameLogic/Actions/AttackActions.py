from Systems import PlayerSelect as Select, Sort, Damage
from Abilities import AttackAbilities as Attacks
from . import AssessTargets as Assess
import random


def weaponAllows(fighter, ability) -> bool:
    compatible = True
    
    if fighter.props["type"] in ["human", "undead"]:
        dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], ability)
        weaponDmgTypes = fighter.equip["weapon"]["dmgTypes"]
        if dmgType not in weaponDmgTypes: compatible = False   

    return compatible

def usableAttacks(fighter, enemies) -> list:
    affordableAttacks, usableAttacks = [], []
    if fighter.atrb["cur_mar"] > 0: affordableAttacks += Attacks.martialAttack
    if fighter.atrb["cur_mag"] > 0: affordableAttacks += Attacks.magicAttack

    for attack in fighter.abl["attacks"]:
        if (attack in affordableAttacks):
            if Sort.canReachAny(fighter, enemies, attack) and weaponAllows(fighter, attack):
                usableAttacks += [attack]

    return usableAttacks


def pcSelectAttack(fighter, enemies) -> str:
    attackOptions = usableAttacks(fighter, enemies)

    if len(enemies) == 1:
        for option in range(len(attackOptions)):
            attackOptions[option] = attackOptions[option] + " -> " + enemies[0].props["name"]

    answer = Select.pickOption(attackOptions, "attack", False).split(" -> ")[0]
    return answer


def npcSelectAttack(fighter, target) -> str:
    attackOptions = usableAttacks(fighter, [target])
    if len(attackOptions) == 0: return "None"
    else: return random.choice(attackOptions)


def npcSelectAttackTarget(fighter, enemies, pickClosest):
    if len(enemies) == 0: return "None"

    closestEnemy = Assess.findClosest(fighter, enemies)
    highestMAGEnemy = Assess.findHighestAtrb(enemies, "cur_mag")
    highestMAREnemy = Assess.findHighestAtrb(enemies, "cur_mar")
    lowestAVEnemy = Assess.findLowestAV(fighter, enemies)
    lowestHPEnemy = Assess.findLowestAtrb(fighter, enemies, "cur_hp")
    lowestResFlameEnemy = Assess.findLowestRes(fighter, enemies, "Flame")
    lowestResCrushEnemy = Assess.findLowestRes(fighter, enemies, "Crush")
    lowestResIceEnemy = Assess.findLowestRes(fighter, enemies, "Ice")
    lowestResHolyEnemy = Assess.findLowestRes(fighter, enemies, "Holy")
    lowestResPierceEnemy = Assess.findLowestRes(fighter, enemies, "Pierce")
    lowestResRotEnemy = Assess.findLowestRes(fighter, enemies, "Rot")
    lowestResToxicEnemy = Assess.findLowestRes(fighter, enemies, "Toxic")

    target, threats, vulnerable = closestEnemy, [closestEnemy,  highestMAGEnemy, highestMAREnemy], [lowestAVEnemy, lowestHPEnemy]
    if not pickClosest:
        if not fighter.cndt["sapient"]:                            
            target = random.choice(threats + vulnerable)

        else:                            
            match fighter.atrb["cur_elm"]:
                case "Basic":
                    weaponDmgTypes = fighter.equip["weapon"]["dmgTypes"]
                    if "Pierce" in weaponDmgTypes: target = random.choice(threats + vulnerable + [lowestResPierceEnemy])
                    elif "Crush" in weaponDmgTypes: target = random.choice(threats + vulnerable + [lowestResCrushEnemy])
                case "Rot": target = random.choice(threats + [lowestResRotEnemy])
                case "Dream": target = random.choice(threats)
                case "Flame": target = random.choice(vulnerable + [lowestResFlameEnemy])
                case "Holy":
                    nonLivingTargets = Assess.findUndead(enemies)
                    if len(nonLivingTargets) > 0:
                        highestMARUndead = Assess.findHighestMAR(nonLivingTargets)
                        lowestAVUndead = Assess.findLowestAV(fighter, nonLivingTargets)
                        lowestHPUndead = Assess.findLowestHP(nonLivingTargets)
                        target = random.choice([highestMARUndead, lowestAVUndead, lowestHPUndead])
                    else: target = random.choice(threats + [lowestResHolyEnemy])
                case "Ice": target = random.choice(vulnerable + [lowestResIceEnemy])
                case "Toxic": target = random.choice(vulnerable + [lowestResToxicEnemy])

    return target