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


def findHighestAtrb(targets, key):
    highestRanked = random.choice(targets)
    prevHigh = 0

    for target in targets:
        if target.atrb[key] > prevHigh:
            highestRanked = target
            prevHigh = target.atrb[key]
    
    return highestRanked

def findLowestAtrb(fighter, targets, key, includeSelf=True):
    lowestRanked = random.choice(targets)
    prevLow = 100

    for target in targets:        
        if includeSelf or (fighter != target):
            if target.atrb[key] < prevLow:
                lowestRanked = target
                prevLow = target.atrb[key]
    
    return lowestRanked


def findLowestAV(fighter, targets, includeSelf=True):
    lowestAVtarget = random.choice(targets)
    prevLow, dmgType = 100, "Crush"

    if any(attack in Damage.pierceAttacks for attack in fighter.abl["attacks"]): dmgType = "Pierce"

    for target in targets:
        if includeSelf or (fighter != target):
            guess = Martial.getProbableAv(fighter, dmgType, target)

            if guess < prevLow:
                lowestAVtarget = target
                prevLow = guess

    return lowestAVtarget


def findLowestRes(fighter, targets, dmgType, includeSelf=True):
    lowestResTarget = random.choice(targets)
    prevResLow = 100

    for target in targets:
        if includeSelf or (fighter != target):
            resInt = rankRes(target, dmgType)
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