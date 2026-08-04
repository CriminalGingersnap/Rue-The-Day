from Abilities import Attacks_Martial as Martial, Boons_Apply as Boons
from Systems import Damage
from Maps import Movement
import random


def findClosest(fighter, targets):
    closestTarget = random.choice(targets)
    prevProximity = 11

    for target in targets:
        distance = Movement.getTargetDistance(fighter, target)

        if distance < prevProximity:
            prevProximity = distance
            closestTarget = target
    
    return closestTarget


def findHighestGeneral(targets, key):
    highestRanked = random.choice(targets)
    prevHigh = highestRanked.atrb[key]

    for target in targets:
        if target.atrb[key] > prevHigh:
            highestRanked = target
            prevHigh = target.atrb[key]
    
    return highestRanked

def findLowestGeneral(targets, key):
    lowestRanked = random.choice(targets)
    prevLow = lowestRanked.atrb[key]

    for target in targets:
        if target.atrb[key] < prevLow:
            lowestRanked = target
            prevLow = target.atrb[key]
    
    return lowestRanked


def findLowestAV(fighter, targets):
    lowestAVtarget = random.choice(targets)
    prevLow, dmgType = 15, "Crush"

    if any(attack in Damage.pierceAttacks for attack in fighter.abl["attacks"]): dmgType = "Pierce"

    for target in targets:
        guess = Martial.getProbableAv(fighter, dmgType, target)

        if guess < prevLow:
            lowestAVtarget = target
            prevLow = guess

    return lowestAVtarget


def findLowestRes(targets, dmgType):
    lowestResTarget = random.choice(targets)
    prevResLow = 1

    for target in targets:
        resInt = rankRes(target, dmgType) + target.effects["Guard"]["dice"]
        if target.effects["Wreath"]["dice"] > 0:
            compatible = Boons.checkCompatibility(dmgType, target.effects["Wreath"]["additional"])
            if compatible: resInt += (3 * target.effects["Wreath"]["dice"])

        if resInt < prevResLow:
            lowestResTarget = target
            prevResLow = resInt

    return lowestResTarget

def rankRes(target, dmgType) -> int:
    resInt = 0
    match target.atrb["cur_res"][dmgType]:
        case "vulnerable": resInt = 0
        case "normal": resInt = 3
        case "resistant": resInt = 6
        case "immune": resInt = 9

    if Boons.checkCompatibility(dmgType, target.equip["armor"]["element"]):
        resInt += target.equip["armor"]["modifier"]

    return resInt


def findUndead(targets): # Update for elementals
    undead = []
    for target in targets:
        if target.cndt["lifeless"]:
            undead += target

    return undead