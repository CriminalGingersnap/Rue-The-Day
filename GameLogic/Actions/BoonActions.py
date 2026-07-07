from Abilities import DamageTypes as Damage, Boons_Set as Boons, Boons_Apply
from Systems import PlayerSelect as Select
from Maps import Movement
from . import AssessTargets as Assess, AttackActions
import random


def pcSelectBoon(fighter):
    boonOptions = usableBoons(fighter)
    return Select.pickOption(boonOptions, "boon") 

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
        damageTypes += Damage.identifyDamageType(enemy, attack)
    
    return damageTypes

def canWreath(fighter, dmgTypes) -> bool:
    fighterDmgType = Damage.convertElmToDmg(fighter.atrb["cur_elm"])
    compatible = False

    for enemyDmgType in dmgTypes:
        if Boons_Apply.checkCompatibility(enemyDmgType, fighterDmgType):
            compatible = True

    return compatible

def usefulBoons(fighter, enemies):
    dmgTypes, boonPreferences = [], ["Flee", "Heal", "Regenerate"]

    # if ally hp < nat: heal

    for enemy in enemies:
        dmgTypes += enemyDamageTypes(enemy)        
        if Movement.getTargetDistance(fighter, enemy) > 2: boonPreferences += ["Conceal", "Shroud"]
        if canWreath(fighter, dmgTypes): boonPreferences += ["Wreath"]
    
    if any(dType in dmgTypes for dType in ["Pierce", "Crush", "Venom"]):
        boonPreferences += ["Evade", "Guard"]

    return boonPreferences


def usableBoons(fighter):
    affordableBoons, usableBoons = [], []

    if (fighter.atrb["cur_mag"] > 0) and AttackActions.weaponAllows(fighter, "Bring"):
        affordableBoons += Boons.magicBoons
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
        
        if boon in ["Conceal", "Evade", "Regenerate", "Slip"]: target = fighter
        else:
            match boon:
                case "Guard": target = random.choice([lowestAVAlly, lowestHPAlly])
                case "Heal": target = lowestHPAlly
                case "Shroud": target = random.choice([fighter, lowestHPAlly])
                case "Wreath":
                    dmgType = Damage.identifyDamageType(fighter, boon)
                    match dmgType:
                        case "Burn": target = random.choice([lowestHPAlly, lowestResFreezeAlly])
                        case "Dream": target = random.choice([lowestHPAlly, lowestResCrushAlly, lowestResPierceAlly])
                        case "Freeze": target = random.choice([lowestHPAlly, lowestResBurnAlly])
                        case "Holy": target = random.choice([lowestHPAlly, lowestResRotAlly])
                        case "Rot": target = random.choice([lowestHPAlly, lowestResDreamAlly])

    return target