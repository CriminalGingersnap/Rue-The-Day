from Systems import PlayerSelect as Select, Equipment
from Abilities import AttackAbilities as Attacks, Hindrances_Apply as Hinder, DamageTypes as Damage
from . import AssessTargets as Assess, Sort
import random


def weaponAllows(fighter, ability) -> bool:
    compatible = True
    
    if fighter.type in ["human", "undead"]:
        dmgType = Damage.identifyDamageType(fighter, ability)["base"]
        weaponDmgTypes = fighter.equipment["weapon"]["dmgTypes"]  
        if dmgType not in weaponDmgTypes: compatible = False   

    return compatible

def usableAttacks(fighter, enemies) -> list:
    affordableAttacks, usableAttacks = [], []
    if fighter.atrb["cur_mar"] > 0: affordableAttacks += Attacks.martialAttack
    if fighter.atrb["cur_mag"] > 0: affordableAttacks += Attacks.magicAttack

    for attack in fighter.abl["attacks"]:
        if (attack in affordableAttacks) and setReachable(fighter, enemies, attack):
            if weaponAllows(fighter, attack): usableAttacks += [attack]
    
    return usableAttacks

def setReachable(fighter, enemies, attack) -> bool:
    reachable = False
    attackReach = Sort.getReach(attack)
    enemyRange = Sort.setRange(fighter, enemies)

    for enemy in enemyRange:
        if enemyRange[enemy] <= attackReach:
            reachable = True

    return reachable


def pcSelectAttack(fighter, enemies) -> str:
    attackOptions = usableAttacks(fighter, enemies)
    
    if len(attackOptions) == 1: return attackOptions[0]
    else:
        Select.waitPrint("Choose Attack: ")
        answer = Select.makeSelection(attackOptions + ["None"])
        return answer


def npcSelectAttack(fighter, target) -> str:
    attackOptions = usableAttacks(fighter, target)
    if len(attackOptions) == 0: return "None"
    else: return random.choice(attackOptions)


def npcSelectAttackTarget(fighter, enemies):
    if len(enemies) == 0: return "None"

    closestEnemy = Assess.findClosest(fighter, enemies)
    highestMAGEnemy = Assess.findHighestMAG(enemies)
    highestMAREnemy = Assess.findHighestMAR(enemies)
    lowestAVEnemy = Assess.findLowestAV(fighter, enemies)
    lowestHPEnemy = Assess.findLowestHP(enemies)
    lowestResBurnEnemy = Assess.findLowestRes(enemies, "Burn")
    lowestResCrushEnemy = Assess.findLowestRes(enemies, "Crush")
    lowestResDreamEnemy = Assess.findLowestRes(enemies, "Dream")
    lowestResFreezeEnemy = Assess.findLowestRes(enemies, "Freeze")
    lowestResHolyEnemy = Assess.findLowestRes(enemies, "Holy")
    lowestResPierceEnemy = Assess.findLowestRes(enemies, "Pierce")
    lowestResRotEnemy = Assess.findLowestRes(enemies, "Rot")
    lowestResVenomEnemy = Assess.findLowestRes(enemies, "Venom")

    target = closestEnemy

    if fighter.cndt["sapient"] and random.choice([True, False]):
        job = fighter.job
        if lowestHPEnemy.atrb["cur_hp"] < 6: target = lowestHPEnemy
        elif job in ["Archer", "Dragonslayer", "Knight"]:
            target = random.choice([highestMAGEnemy, lowestAVEnemy, lowestHPEnemy])
        elif fighter.element != "Basic":
            match fighter.element:
                case "Corpse": target = random.choice([highestMAREnemy, highestMAGEnemy, lowestResRotEnemy])
                case "Fey": target = random.choice([highestMAREnemy, highestMAGEnemy, lowestResDreamEnemy])
                case "Flame": target = random.choice([highestMAREnemy, lowestHPEnemy, lowestResBurnEnemy])
                case "Blessed": target = random.choice([highestMAREnemy, highestMAGEnemy, lowestResHolyEnemy])
                case "Ice": target = random.choice([highestMAREnemy, lowestHPEnemy, lowestResFreezeEnemy])
                case "Venom": target = random.choice([highestMAREnemy, lowestHPEnemy, lowestResVenomEnemy])
        elif job == "Paladin":
            nonLivingTargets = Assess.findUndead(enemies)
            if len(nonLivingTargets) > 0:
                highestMARUndead = Assess.findHighestMAR(nonLivingTargets)
                lowestAVUndead = Assess.findLowestAV(fighter, nonLivingTargets)
                lowestHPUndead = Assess.findLowestHP(nonLivingTargets)
                target = random.choice([highestMARUndead, lowestAVUndead, lowestHPUndead])
            else:
                target = random.choice([highestMAGEnemy, lowestAVEnemy])

    return target