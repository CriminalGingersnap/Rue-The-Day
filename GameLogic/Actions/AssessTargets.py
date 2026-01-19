from Abilities import Attacks_Martial as Martial, DamageTypes as Damage, Boons_Apply as Boons
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


def findHighestMAG(targets):
    highestMAGTarget = random.choice(targets)
    prevMAGHigh = highestMAGTarget.atrb["cur_mag"]

    for target in targets:
        if target.atrb["cur_mag"] > prevMAGHigh:
            highestMAGTarget = target
            prevMAGHigh = target.atrb["cur_mag"]
    
    return highestMAGTarget

def findHighestMAR(targets):
    highestMARTarget = random.choice(targets)
    prevMAGHigh = highestMARTarget.atrb["cur_mar"]

    for target in targets:
        if target.atrb["cur_mar"] > prevMAGHigh:
            highestMARTarget = target
            prevMAGHigh = target.atrb["cur_mar"]
    
    return highestMARTarget


def findLowestHP(targets):
    lowestHPTarget = random.choice(targets)
    prevHPLow = lowestHPTarget.atrb["cur_hp"]

    for target in targets:
        if target.atrb["cur_hp"] < prevHPLow:
            lowestHPTarget = target
            prevHPLow = target.atrb["cur_hp"]
    
    return lowestHPTarget

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
        resInt = rankRes(target, dmgType)
        if target.effects["Wreath"]["dice"] > 0:
            compatible = Boons.checkCompatibility(dmgType, target.effects["Wreath"]["additional"])
            if compatible: resInt += (3 * target.effects["Wreath"]["dice"])

        if resInt < prevResLow:
            lowestResTarget = target
            prevResLow = resInt

    return lowestResTarget

def rankRes(target, dmgType) -> int:
    resString, resInt = target.atrb["cur_res"][dmgType], 0
    match resString:
        case "vulnerable": resInt = 0
        case "normal": resInt = 1
        case "resistant": resInt = 2
        case "immune": resInt = 3

    return resInt


def findUndead(targets): # Update for elementals
    undead = []
    for target in targets:
        if target.cndt["lifeless"]:
            undead += target

    return undead