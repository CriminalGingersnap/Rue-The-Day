from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder, Reactions
from Maps import Map_Update as uMap, Movement
from Systems import PlayerSelect as Select


def getGroups(fighter, allies, enemies) -> list:
    fightingEnemies, fightingAllies = sortLiving(enemies)[0], sortLiving(allies)[0]
    reachable = sortReachable(fighter, fightingEnemies, fightingAllies)
    return {"reachable": reachable, "fightingAllies": fightingAllies, "fightingEnemies": fightingEnemies}


def setAlive(fighter, fightingAllies, battleMap) -> bool:
    if fighter.atrb["cur_hp"] <= 0:
        fighter.cndt["dead"] = True
        Select.slowPrint(fighter.props["name"] + " has 0 hit points remaining and will perish soon.")
        Reactions.applyPheromones(fighter, fightingAllies)
        uMap.removeFighter(fighter, battleMap)
        
        return False
    else: return True

def sortLiving(contingent) -> list:
    fighting, downed = [], []

    for candidate in contingent:
        if candidate.cndt["dead"] == False:
            fighting += [candidate]
        else: downed += [candidate]        
    
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
    reachable, weaponReach = False, fighter.equipment["weapon"]["reach"]
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