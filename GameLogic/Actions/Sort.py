from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder, Reactions
from Maps import Map, Movement
from . import  Sort
from Systems import PlayerSelect as Select


def getGroups(fighter, allies, enemies) -> list:
    fightingEnemies, fightingAllies = Sort.sortLiving(enemies)[0], Sort.sortLiving(allies)[0]
    reachable = Sort.sortReachable(fighter, fightingEnemies, fightingAllies)
    return {"reachable": reachable, "fightingAllies": fightingAllies, "fightingEnemies": fightingEnemies}

def setAlive(fighter, fightingAllies) -> bool:
    if fighter.atrb["cur_hp"] <= 0:
        fighter.cndt["dead"] = True
        Select.slowPrint(fighter.name + " has 0 hit points remaining and is slain.")
        Reactions.applyPheromones(fighter, fightingAllies)
        Map.removeFighter(fighter)
        
        return False
    else: return True

def sortLiving(contingent) -> list:
    fighting, downed = [], []

    for candidate in contingent:
        if candidate.cndt["dead"] == False: fighting += [candidate]
        else: downed += [candidate]        
    
    return [fighting, downed]

def sortVisible(contingent, sightMap) -> list:
    visible, invisible = [], []

    for fighter in contingent:
        if fighter.rank == "player": token = fighter.name[0] + "."
        else: token = fighter.name[0] + fighter.name[-2]

        for row in range(12):
            for column in range(12):
                if token in sightMap[row][column]: visible += [fighter]
        
        if fighter not in visible: invisible += [fighter]
    
    return [visible, invisible]


def sortReachable(fighter, fightingEnemies, fightingAllies) -> list:
    boonReachable, attackReachable, hinderReachable = [], [], []

    weaponReach = fighter.equipment["weapon"]["reach"]
    attackReach = min(getReach(fighter.abl["attacks"]), weaponReach)
    boonReach = min(getReach(fighter.abl["boons"]), weaponReach)
    hindReach = min(getReach(fighter.abl["hindrances"]), weaponReach)

    visibleAllies = sortVisible(fightingAllies, fighter.sightMap)[0]
    visibleEnemies = sortVisible(fightingEnemies, fighter.sightMap)[0]

    allyRange = setRange(fighter, visibleAllies)
    for ally in allyRange:
        if allyRange[ally] <= boonReach: boonReachable += [ally]

    enemyRange = setRange(fighter, visibleEnemies)
    for enemy in enemyRange:
        distance = enemyRange[enemy]
        if distance <= attackReach: attackReachable += [enemy]
        if distance <= hindReach: hinderReachable += [enemy]

    return {"boonReachable": boonReachable, "attackReachable": attackReachable, "hinderReachable": hinderReachable,
            "visibleAllies": visibleAllies, "visibleEnemies": visibleEnemies}

def setRange(fighter, contingent) -> list:
    range = {}

    for candidate in contingent:
        distance = Movement.findDistance(fighter, candidate)
        if candidate in candidate.commitments["Distant"]["targets"]: distance += 3
        range[candidate] = distance

    return range


def getReach(ability) -> int:
    twoReach = Attacks.closeMartialAttack + Boons.martialBoons + Hinder.martialHindrance
    fourReach = Attacks.midMartialAttack + Boons.magicBoons + Hinder.magicHindrance
    eight = Attacks.farMartialAttack + Attacks.magicAttack
    reach = 0
    
    if ability in twoReach: reach = 2
    elif ability in fourReach: reach = 4
    elif ability in eight: reach = 8

    return reach