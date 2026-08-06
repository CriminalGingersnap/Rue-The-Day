from Abilities import Boons_Set as Boons, Boons_Apply
from Systems import PlayerSelect as Select, Damage
from Maps import Movement
from . import AssessTargets as Assess, AttackActions
import random


def pcSelectBoon(fighter, allies):
    boonOptions = usableBoons(fighter)
    
    if len(allies) == 1:
        for option in range(len(boonOptions)):
            boonOptions[option] = boonOptions[option] + " -> " + allies[0].props["name"]

    answer = Select.pickOption(boonOptions, "boon").split(" -> ")[0]
    return answer


def npcSelectBoon(fighter, enemies):
    boonOptions = []
    useful, usable = usefulBoons(fighter, enemies), usableBoons(fighter)

    for option in useful:
        if (option in usable) and (option not in boonOptions): boonOptions += [option]

    if boonOptions != []: return random.choice(boonOptions)
    else: return "None"


def canWreath(fighter, dmgTypes) -> bool:
    compatible = False

    for enemyDmgType in dmgTypes:
        if Boons_Apply.checkCompatibility(enemyDmgType, fighter.atrb["cur_elm"]):
            compatible = True
    return compatible

def usefulBoons(fighter, enemies):
    dmgTypes, boonPreferences = [], ["Bandage", "Fortify", "Heal", "Rally", "Regenerate"]
    someFar, anyClose = False, False

    for enemy in enemies:
        dmgTypes += enemy.equip["weapon"]["dmgTypes"]
        if canWreath(fighter, dmgTypes): boonPreferences += ["Wreath"]

        distance = Movement.getTargetDistance(fighter, enemy)
        if distance > 6: someFar = True
        if distance < 3: anyClose = True

    if any(dType in dmgTypes for dType in ["Pierce", "Crush", "Toxic"]): boonPreferences += ["Guard"]
    if someFar and not anyClose: boonPreferences += ["Conceal", "Veil"]

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
    target = fighter

    if (fighter.cndt["social"] or fighter.cndt["sapient"]) and (len(allies) > 0):
        lowestAVAlly = Assess.findLowestAV(fighter, allies)
        lowestHPAlly = Assess.findLowestGeneral(allies, "cur_hp")
        lowestResDreamAlly = Assess.findLowestRes(allies, "Dream")
        lowestResFlameAlly = Assess.findLowestRes(allies, "Flame")
        lowestResIceAlly = Assess.findLowestRes(allies, "Ice")
        lowestResRotAlly = Assess.findLowestRes(allies, "Rot")
        lowestStaminaAlly = Assess.findLowestGeneral(allies, "stamina")
        lowestToleranceAlly = Assess.findLowestGeneral(allies, "tolerance")
        
        if boon in ["Conceal", "Regenerate"]: target = fighter
        else:
            match boon:
                case "Bandage" | "Heal": target = lowestHPAlly
                case "Guard": target = random.choice([lowestAVAlly, lowestHPAlly])
                case "Fortify": target = lowestToleranceAlly
                case "Rally": target = lowestStaminaAlly
                case "Veil": target = random.choice([fighter, lowestHPAlly])
                case "Wreath":
                    dmgType = Damage.identifyDamageType(fighter.atrb["cur_elm"], boon)
                    match dmgType:
                        case "Flame": target = random.choice([lowestHPAlly, lowestResIceAlly])
                        case "Ice": target = random.choice([lowestHPAlly, lowestResFlameAlly])
                        case "Holy": target = random.choice([lowestHPAlly, lowestResRotAlly])
                        case "Rot": target = random.choice([lowestHPAlly, lowestResDreamAlly])

    return target