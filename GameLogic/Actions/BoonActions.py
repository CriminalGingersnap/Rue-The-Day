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

    answer = Select.pickOption(boonOptions, "boon ability", False).split(" -> ")[0]
    return answer


def npcSelectBoon(fighter, enemies):
    boonOptions = []
    useful, usable = usefulBoons(fighter, enemies), usableBoons(fighter)

    for option in useful:
        if (option in usable) and (option not in boonOptions): boonOptions += [option]

    if boonOptions != []: return random.choice(boonOptions)
    else: return "None"


def usableBoons(fighter):
    affordableBoons, usableBoons = [], []

    if (fighter.atrb["cur_mag"] > 0) and AttackActions.weaponAllows(fighter, "Bring"):
        affordableBoons += Boons.magicBoons
    if fighter.atrb["cur_mar"] > 0:
        affordableBoons += Boons.martialBoons
    
    for boon in fighter.abl["boons"]:
        if (boon in affordableBoons): usableBoons += [boon]

    return usableBoons


def canWreath(fighter, dmgTypes) -> bool:
    compatible = False
    for enemyDmgType in dmgTypes:
        if Boons_Apply.checkCompatibility(enemyDmgType, fighter.atrb["cur_elm"]):
            compatible = True
    return compatible

def usefulBoons(fighter, enemies):
    boonPreferences = ["Bandage", "Fortify", "Heal", "Rally", "Regenerate"]

    dmgDist = getDmgAndDistance(fighter, enemies)
    dmgTypes, someFar, anyClose = dmgDist[0], dmgDist[1], dmgDist[2]

    if any(dType in dmgTypes for dType in ["Pierce", "Crush", "Toxic"]): boonPreferences += ["Guard"]
    if someFar and not anyClose: boonPreferences += ["Conceal", "Veil"]
    if canWreath(fighter, dmgTypes): boonPreferences += ["Wreath"]

    return boonPreferences

def getDmgAndDistance(fighter, enemies):
    dmgTypes, someFar, anyClose = [], False, False
    for enemy in enemies:
        dmgTypes += enemy.equip["weapon"]["dmgTypes"]

        distance = Movement.getTargetDistance(fighter, enemy)
        if distance > 6: someFar = True
        if distance < 3: anyClose = True

    return [dmgTypes, someFar, anyClose]


def npcSelectBoonTarget(fighter, allies, boon):
    target, includeSelf = fighter, ((fighter.props["type"] not in ["echo", "totem"]) or (fighter.props["job"] == "Door"))
    cooperative = (fighter.cndt["social"] or fighter.cndt["sapient"])

    if (boon not in ["Conceal", "Regenerate"]) and cooperative and (len(allies) > 1):
        lowestAVAlly = Assess.findLowestAV(fighter, allies, includeSelf)
        lowestHPAlly = Assess.findLowestAtrb(fighter, allies, "cur_hp", includeSelf)
        lowestResDreamAlly = Assess.findLowestRes(fighter, allies, "Dream", includeSelf)
        lowestResFlameAlly = Assess.findLowestRes(fighter, allies, "Flame", includeSelf)
        lowestResIceAlly = Assess.findLowestRes(fighter, allies, "Ice", includeSelf)
        lowestResRotAlly = Assess.findLowestRes(fighter, allies, "Rot", includeSelf)
        lowestStaminaAlly = Assess.findLowestAtrb(fighter, allies, "stamina", includeSelf)
        lowestToleranceAlly = Assess.findLowestAtrb(fighter, allies, "tolerance", includeSelf)
    
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