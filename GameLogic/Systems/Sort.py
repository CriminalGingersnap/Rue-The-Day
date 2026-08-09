from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder
from Maps import Map_Update as uMap, Movement, Map_Instantiate as iMap
from Systems import PlayerSelect as Select


def getGroups(fighter, enemies, allies) -> list:
    reachable = sortReachable(fighter, enemies, allies)
    return {"reachable": reachable, "fightingAllies": allies, "fightingEnemies": enemies}
    

def setAlive(fighter) -> bool:
    if fighter.atrb["cur_hp"] <= 0:
        fighter.cndt["dead"] = True
        Select.waitPrint("\n" + fighter.props["name"] + " has fallen.")

        return False
    else: return True

def sortLiving(contingent, battleMap) -> list:
    fighting, downed, pacifist = [], [], []

    for candidate in contingent:
        if candidate.cndt["dead"]:
            downed += [candidate]
            if candidate.props["initials"] in battleMap[candidate.pos[0]][candidate.pos[1]]:
                uMap.removeFighter(candidate, battleMap)
        else:
            fighting += [candidate]

            if candidate.cndt["reposed"] or candidate.cndt["skittish"]: pacifist += [candidate]

            if "echo" in candidate.inv:
                echo = candidate.inv["echo"]
                if (echo != "None") and (echo.itemEffects["Animate"]["duration"] > 0):
                    fighting += [echo]

            if "standard" in candidate.inv:
                standard = candidate.inv["standard"]
                if (standard != "None") and standard.cndt["planted"]:
                    if standard.cndt["dead"]: downed += [standard]
                    else: fighting += [standard]

    return [fighting, downed, pacifist]


def sortVisible(contingent, sightMap) -> list:
    visible, invisible = [], []

    for fighter in contingent:
        for row in range(12):
            for column in range(12):
                if fighter.props["initials"] in sightMap[row][column]:
                    veiled = sightMap[row][column][0] in iMap.intStrings
                    if not veiled: visible += [fighter]
        
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