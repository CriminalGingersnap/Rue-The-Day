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
        answer = Select.makeSelection(boonOptions) 
        return answer

def pcSelectBoonTarget(allies):
    choice = "None"
    if allies == []: Select.waitPrint("No valid targets remaining.")
    else: choice = Select.targetSelect(allies)

    return choice


def npcSelectBoon(fighter, enemies):
    boonOptions = []
    useful, usable = usefulBoons(fighter, enemies), usableBoons(fighter)

    for option in useful:
        if (option in usable) and (option not in boonOptions): boonOptions += [option]

    if boonOptions != []: return random.choice(boonOptions)
    else: return "None"

def enemyDamageTypes(enemy):
    damageTypes = []
    for attack in enemy.abl["attacks"]:
        attackDmg = Damage.identifyDamageType(enemy, attack)
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
        dmgTypes += enemyDamageTypes(enemy)        
        if Movement.findDistance(fighter, enemy) > 2: boonPreferences += ["Shroud"]
        if canWreath(fighter, dmgTypes): boonPreferences += ["Wreath"]
    
    if any(dType in dmgTypes for dType in ["Pierce", "Crush", "Venom"]):
        boonPreferences += ["Bristle", "Evade", "Guard"]
        if "Wreath" not in fighter.abl["boons"]: boonPreferences += ["Convert"]

    return boonPreferences


def usableBoons(fighter):
    affordableBoons, usableBoons = [], []

    if fighter.atrb["cur_mag"] > 0:
        if AttackActions.weaponAllows(fighter, "Bring"):
            affordableBoons += Boons.magicBoons
        if fighter.atrb["cur_mag"] > 1: affordableBoons += ["Convert"]
    if fighter.atrb["cur_mar"] > 0:
        affordableBoons += Boons.martialBoons
    
    for boon in fighter.abl["boons"]:
        if (boon in affordableBoons): usableBoons += [boon]

    return usableBoons


def npcSelectBoonTarget(fighter, allies, boon):
    target = "None"

    if fighter.type not in ["human", "elemental"]:
        if fighter in allies: target = fighter
    elif len(allies) > 0:
        lowestAVAlly = Assess.findLowestAV(fighter, allies)
        lowestHPAlly = Assess.findLowestHP(allies)
        lowestResBurnAlly = Assess.findLowestRes(allies, "Burn")
        lowestResCrushAlly = Assess.findLowestRes(allies, "Crush")
        lowestResDreamAlly = Assess.findLowestRes(allies, "Dream")
        lowestResFreezeAlly = Assess.findLowestRes(allies, "Freeze")
        lowestResPierceAlly = Assess.findLowestRes(allies, "Pierce")
        lowestResRotAlly = Assess.findLowestRes(allies, "Rot")
        
        if boon in ["Convert", "Evade", "Regenerate", "Slip"]: target = fighter
        else:
            match boon:
                case "Guard": target = random.choice([lowestAVAlly, lowestHPAlly])
                case "Heal": target = lowestHPAlly
                case "Shroud": target = random.choice([fighter, lowestHPAlly])
                case "Wreath":
                    dmgType = Damage.identifyDamageType(fighter, boon)["base"]
                    match dmgType:
                        case "Burn": target = random.choice([lowestHPAlly, lowestResFreezeAlly])
                        case "Dream": target = random.choice([lowestHPAlly, lowestResCrushAlly, lowestResPierceAlly])
                        case "Freeze": target = random.choice([lowestHPAlly, lowestResBurnAlly])
                        case "Holy": target = random.choice([lowestHPAlly, lowestResRotAlly])
                        case "Rot": target = random.choice([lowestHPAlly, lowestResDreamAlly])

    return target