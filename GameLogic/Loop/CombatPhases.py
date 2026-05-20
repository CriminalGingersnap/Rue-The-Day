from Actions import MoveActions as Move, ItemActions
from Actions import NPCAbilityActions as NPCAbl, PlayerAbilityActions as PlayerAbl, Sort
from Maps import Visibility, Map_Update as uMap, Map_Print as Print
from Systems import PlayerSelect as Select, Conditions, Effects, Commitments
from Abilities import Reactions, Items_Use as Items


def resetFighter(fighter) -> None:
    fighter.atrb["cur_sp"] = fighter.atrb["base_sp"] - fighter.atrb["fatigue"]
    fighter.atrb["cur_mag"], fighter.atrb["cur_mar"] = fighter.atrb["base_mag"], fighter.atrb["base_mar"]

    if fighter.type == "human":
        equipment = fighter.equipment
        speedLoss = ((equipment["armor"]["modifier"] + equipment["shield"]["modifier"] + equipment["weapon"]["modifier"]) // 2) - 1
        if speedLoss > 0: fighter.atrb["cur_sp"] -= speedLoss

    match fighter.atrb["injury"]:
        case 1: fighter.atrb["cur_sp"] -= fighter.atrb["cur_sp"] // 4
        case 2: fighter.atrb["cur_sp"] -= fighter.atrb["cur_sp"] // 2
        case 3: fighter.atrb["cur_sp"] = min(fighter.atrb["base_sp"], 1)
   
    fighter.atrb["cur_sp"] = max(0, fighter.atrb["cur_sp"])
    fighter.itemUse = 0

    Commitments.clearCommitments(fighter)
    Effects.updateItemEffects(fighter)


def setSight(fighter, enemies, allies, battleMap):
    sightMap = Visibility.createSightMap(battleMap, fighter.position, fighter.rank)
    uMap.hideShrouded(fighter, enemies + allies, sightMap)

    if fighter.rank == "player":
        uMap.revealOthers(fighter, allies, enemies, sightMap)
        uMap.hideTraps(fighter, sightMap)
    else:
        Select.waitPrint(fighter.name + "'s turn")

    Print.printSightMap(battleMap, sightMap, fighter.name + "'s Sight Map")

    return sightMap

def outro(fighter, allies, battleMap):
    alive = Sort.setAlive(fighter, allies, battleMap)

    if alive:
        intensity = max(0, (fighter.atrb["base_mag"] - fighter.atrb["cur_mag"]) + (fighter.atrb["base_mar"] - fighter.atrb["cur_mar"]))
        if fighter.cndt["running"]:
            fighter.cndt["running"] = False
            intensity += 1
        Conditions.decrementStamina(fighter, intensity)
        Reactions.applySocial(fighter, allies)
    
    if fighter.rank != "player": input("Press Enter to conclude " + fighter.name + "'s turn.")    
    
    Items.regenerate(fighter)
    Reactions.applyReinforcements(fighter, allies, battleMap)


def movementStage(fighter, enemies, allies, battleMap) -> None:
    if (fighter.atrb["cur_sp"] > 0) or ((fighter.atrb["base_mag"] > 1) or (fighter.atrb["base_mar"] > 1)):
        groups = Sort.getGroups(fighter, allies, enemies)
        Move.moveAction(fighter, groups, battleMap)

def inventoryStage(fighter, enemies, allies, battleMap) -> None:
    if fighter.itemUse > 0:
        Select.waitPrint("\n" + fighter.name + "'s inventory stage.")
        groups = Sort.getGroups(fighter, allies, enemies)
        ItemActions.itemAction(fighter, groups, battleMap)

def abilityStage(fighter, enemies, allies, battleMap) -> None:
    groups = Sort.getGroups(fighter, allies, enemies)
    reachable, fightingEnemies = groups["reachable"], groups["fightingEnemies"]

    if fighter.cndt["reposed"]: fighter.atrb["cur_mar"], fighter.atrb["cur_mag"] = 0, 0
    elif len(fightingEnemies) > 0:
        if fighter.rank == "player":
            actionChoice = PlayerAbl.chooseAction(fighter, reachable)
            PlayerAbl.takeAction(fighter, actionChoice, reachable)
        else: NPCAbl.npcAction(fighter, groups)