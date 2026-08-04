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

    answer = Select.pickOption(attackOptions, "attack").split(" -> ")[0]
    return answer


def npcSelectAttack(fighter, target) -> str:
    attackOptions = usableAttacks(fighter, [target])
    if len(attackOptions) == 0: return "None"
    else: return random.choice(attackOptions)


def npcSelectAttackTarget(fighter, enemies, pickClosest):
    if len(enemies) == 0: return "None"

    closestEnemy = Assess.findClosest(fighter, enemies)
    highestMAGEnemy = Assess.findHighestGeneral(enemies, "cur_mag")
    highestMAREnemy = Assess.findHighestGeneral(enemies, "cur_mar")
    lowestAVEnemy = Assess.findLowestAV(fighter, enemies)
    lowestHPEnemy = Assess.findLowestGeneral(enemies, "cur_hp")
    lowestResFlameEnemy = Assess.findLowestRes(enemies, "Flame")
    lowestResCrushEnemy = Assess.findLowestRes(enemies, "Crush")
    lowestResDreamEnemy = Assess.findLowestRes(enemies, "Dream")
    lowestResIceEnemy = Assess.findLowestRes(enemies, "Ice")
    lowestResHolyEnemy = Assess.findLowestRes(enemies, "Holy")
    lowestResPierceEnemy = Assess.findLowestRes(enemies, "Pierce")
    lowestResRotEnemy = Assess.findLowestRes(enemies, "Rot")
    lowestResToxicEnemy = Assess.findLowestRes(enemies, "Toxic")

    target = closestEnemy
    if not pickClosest:
        if not fighter.cndt["sapient"]:                            
            target = random.choice([closestEnemy, lowestHPEnemy, lowestAVEnemy])

        else:                            
            match fighter.atrb["cur_elm"]:
                case "Basic":
                    weaponDmgTypes = fighter.equip["weapon"]["dmgTypes"]
                    if "Pierce" in weaponDmgTypes: target = random.choice([lowestResPierceEnemy, highestMAGEnemy, lowestAVEnemy, lowestHPEnemy])
                    elif "Crush" in weaponDmgTypes: target = random.choice([lowestResCrushEnemy, highestMAGEnemy, lowestAVEnemy, lowestHPEnemy])
                case "Rot": target = random.choice([highestMAREnemy, highestMAGEnemy, lowestResRotEnemy])
                case "Dream": target = random.choice([highestMAGEnemy, lowestResDreamEnemy])
                case "Flame": target = random.choice([highestMAREnemy, lowestHPEnemy, lowestResFlameEnemy])
                case "Holy":
                    nonLivingTargets = Assess.findUndead(enemies)
                    if len(nonLivingTargets) > 0:
                        highestMARUndead = Assess.findHighestMAR(nonLivingTargets)
                        lowestAVUndead = Assess.findLowestAV(fighter, nonLivingTargets)
                        lowestHPUndead = Assess.findLowestHP(nonLivingTargets)
                        target = random.choice([highestMARUndead, lowestAVUndead, lowestHPUndead])
                    else: target = random.choice([highestMAGEnemy, lowestAVEnemy, lowestResHolyEnemy])
                case "Ice": target = random.choice([highestMAREnemy, lowestHPEnemy, lowestResIceEnemy])
                case "Toxic": target = random.choice([highestMAREnemy, lowestHPEnemy, lowestResToxicEnemy])

    return target