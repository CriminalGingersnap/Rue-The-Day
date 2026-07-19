from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder, Reactions
from Maps import Map_Update as uMap, Movement
from Systems import PlayerSelect as Select


def getGroups(fighter, enemies, allies) -> list:
    reachable = sortReachable(fighter, enemies, allies)
    return {"reachable": reachable, "fightingAllies": allies, "fightingEnemies": enemies}
    

def setAlive(fighter) -> bool:
    inanimate = fighter.itemEffects["Animate"]["additional"] and (fighter.itemEffects["Animate"]["duration"] <= 1)
    
    if (fighter.atrb["cur_hp"] <= 0) or inanimate:
        fighter.cndt["dead"] = True
        if fighter.props["rank"] == "player": Select.slowPrint(fighter.props["name"] + " will perish soon.")
        
        return False
    else: return True

def sortLiving(contingent, battleMap) -> list:
    fighting, downed = [], []

    for candidate in contingent:
        if candidate.cndt["dead"]: 
            Reactions.applyPheromones(candidate, contingent)
            uMap.removeFighter(candidate, battleMap)

            if candidate.itemEffects["Animate"]["additional"]: contingent.remove(candidate)
            else: downed += [candidate]   

        else: fighting += [candidate]
    
    return [fighting, downed]


def sortVisible(contingent, sightMap) -> list:
    visible, invisible = [], []

    for fighter in contingent:
        for row in range(12):
            for column in range(12):
                if fighter.props["initials"] in sightMap[row][column]: visible += [fighter]
        
        if fighter not in visible: invisible += [fighter]
    
    return [visible, invisible]


def canReachAny(fighter, group, ability):
    reachAny = False

    for target in group:
        if canReach(fighter, target, ability): reachAny = True
    
    return reachAny

def canReach(fighter, target, ability) -> bool:
    reachable, weaponReach = False, fighter.equip["weapon"]["reach"]
    abilityReach = min(getReach(ability), weaponReach)

    distance = Movement.getTargetDistance(fighter, target)
    if distance <= abilityReach:
        reachable = True

    return reachable


def sortReachable(fighter, fightingEnemies, fightingAllies) -> list:
    boonReachable, attackReachable, hinderReachable = [], [], []
    visibleAllies = sortVisible(fightingAllies, fighter.sightMap)[0]
    visibleEnemies = sortVisible(fightingEnemies, fighter.sightMap)[0]

    for ally in visibleAllies:
        for boon in fighter.abl["boons"]:
            if canReach(fighter, ally, boon):
                boonReachable += [ally]
                break

    for enemy in visibleEnemies:
        for attack in fighter.abl["attacks"]:
            if canReach(fighter, enemy, attack):
                attackReachable += [enemy]
                break
        
        for hindrance in fighter.abl["hindrances"]:
            if canReach(fighter, enemy, hindrance):
                hinderReachable += [enemy]
                break

    return {"boonReachable": boonReachable, "attackReachable": attackReachable, "hinderReachable": hinderReachable,
            "visibleAllies": visibleAllies, "visibleEnemies": visibleEnemies}


def getReach(ability) -> int:
    twoReach = Attacks.closeMartialAttack + Boons.martialBoons + Hinder.martialHindrances
    fourReach = Attacks.midMartialAttack + Boons.magicBoons + Hinder.magicHindrances
    eight = Attacks.farMartialAttack + Attacks.magicAttack
    reach = 0
    
    if ability in twoReach: reach = 2
    elif ability in fourReach: reach = 4
    elif ability in eight: reach = 8

    return reach