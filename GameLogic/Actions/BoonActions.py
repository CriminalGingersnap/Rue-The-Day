from Abilities import DamageTypes as Damage, Hindrances_Apply as Hinder, Boons_Set as Boons
from Systems import PlayerSelect as Select
from Maps import Movement
from . import AssessTargets as Assess, AttackActions
import random


def pcSelectBoon(fighter):
    boonOptions = usableBoons(fighter)

    if len(boonOptions) == 1: return boonOptions[0]
    else:
        Select.waitPrint("Choose Boon:")
        answer = Select.makeSelection(boonOptions + ["None"]) 
        return answer


def pcSelectBoonTarget(fighter, allies, boonChoice):
    choice, candidates = "None", allies

    validTargets = winnowTargets(fighter, candidates, boonChoice)
    if validTargets == []: Select.waitPrint("No valid targets remaining.")
    else: choice = Select.targetSelect(validTargets)

    return choice


def winnowTargets(fighter, candidates, ability) -> list:
    validTargets = []
    if ability in Boons.selfBoons: validTargets = [fighter]
    else:
        for candidate in candidates:
            if any(source == candidate.effects[ability]["source"] for source in [fighter, None]):
                validTargets += [candidate]

    return validTargets


def npcSelectBoon(fighter, enemies):
    boonOptions = []
    useful, usable = usefulBoons(fighter, enemies), usableBoons(fighter)

    for option in useful:
        if (option in usable) and (option not in boonOptions):
            if fighter not in fighter.commitments["Guard"]["targets"]: boonOptions += [option]

    if boonOptions != []: return random.choice(boonOptions)
    else: return "None"

def enemyDamageTypes(enemy):
    damageTypes = []
    for attack in enemy.abl["attacks"]:
        attackDmg = Damage.identifyDamageType(attack)
        damageTypes += [attackDmg["base"]] + [attackDmg["bonus"]]
    
    return damageTypes

def canWreath(fighter, dmgTypes) -> bool:
    fighterDmgType = Damage.identifyDamageType(fighter, "Bring")["base"]
    compatible = False

    for enemyDmgType in dmgTypes:
        if Boons.checkCompatibility(enemyDmgType, fighterDmgType):
            compatible = True

    return compatible

def usefulBoons(fighter, enemies):
    dmgTypes, boonPreferences = [], ["Flee", "Heal", "Regenerate"]

    # if ally hp < nat: heal

    for enemy in enemies:
        damageTypes += enemyDamageTypes(enemy)        
        if Movement.findDistance(fighter, enemy) > 2: boonPreferences += ["Shroud"]
        if canWreath(fighter, enemyDamageTypes): boonPreferences += ["Wreath"]
    
    if any(dType in dmgTypes for dType in ["Pierce", "Crush", "Venom"]):
        boonPreferences += ["Bristle", "Evade", "Guard"]
        if "Wreath" not in fighter.abl["boons"]: boonPreferences += ["Convert"]

    return boonPreferences


def usableBoons(fighter):
    affordableBoons, usableBoons = [], []

    if fighter.atrb["cur_mag"] > 0:
        if AttackActions.weaponAllows(fighter, "Bring"):
            affordableBoons += Boons.magicSelfBoons + Boons.magicBoons
        if fighter.atrb["cur_mag"] > 1: affordableBoons += ["Convert"]
    if fighter.atrb["cur_mar"] > 0:
        affordableBoons += Boons.martialBoons + Boons.martialSelfBoons
    
    for boon in fighter.abl["boons"]:
        if (boon in affordableBoons): usableBoons += [boon]

    return usableBoons


def npcSelectBoonTarget(fighter, allies, boon):
    target, validAllies = "None", winnowTargets(fighter, allies, boon)

    if fighter.type not in ["human", "elemental"]:
        if fighter in validAllies: target = fighter
    elif len(validAllies) > 0:
        lowestAVAlly = Assess.findLowestAV(fighter, validAllies)
        lowestHPAlly = Assess.findLowestHP(validAllies)
        lowestResBurnAlly = Assess.findLowestRes(validAllies, "Burn")
        lowestResCrushAlly = Assess.findLowestRes(validAllies, "Crush")
        lowestResDreamAlly = Assess.findLowestRes(validAllies, "Dream")
        lowestResFreezeAlly = Assess.findLowestRes(validAllies, "Freeze")
        lowestResPierceAlly = Assess.findLowestRes(validAllies, "Pierce")
        lowestResRotAlly = Assess.findLowestRes(validAllies, "Rot")
        
        if boon in ["Convert", "Evade", "Regenerate", "Slip"]: target = fighter
        else:
            match boon:
                case "Guard": target = random.choice([lowestAVAlly, lowestHPAlly])
                case "Heal": target = lowestHPAlly
                case "Shroud": target = random.choice([fighter, lowestHPAlly])
                case "Wreath":
                    dmgType = Damage.identifyDamageType(fighter, boon)["basic"]
                    match dmgType:
                        case "Burn": target = random.choice([lowestHPAlly, lowestResFreezeAlly])
                        case "Dream": target = random.choice([lowestHPAlly, lowestResCrushAlly, lowestResPierceAlly])
                        case "Freeze": target = random.choice([lowestHPAlly, lowestResBurnAlly])
                        case "Holy": target = random.choice([lowestHPAlly, lowestResRotAlly])
                        case "Rot": target = random.choice([lowestHPAlly, lowestResDreamAlly])

    return target