from Systems import PlayerSelect as Select
from . import ItemActions, BoonActions as Boons, AttackActions as Attacks
from Abilities import Move_Apply as Moves, Area_Set as Area
from Maps import Movement, Map_Update as uMap
import random


def moveAction(fighter, groups, battleMap) -> None:
    posOptions = ["Evade"] + fighter.abl["areas"]
    if fighter.atrb["base_mar"] > 0:
        posOptions += ["Set"]
        if fighter.atrb["base_mag"] > 0:
            posOptions += ["Empower"]

    hasInventory = any(invAbl in fighter.abl["boons"] for invAbl in ["Inventory", "Quick Inventory"])
    if hasInventory and ItemActions.hasItems(fighter): posOptions += ["Inventory"]

    if fighter.rank == "player":
        posOptions += ["Examine"]
        if fighter.atrb["cur_sp"] > 0: posOptions += ["Move"]
        movePlayer(fighter, groups, posOptions, battleMap)
    else: moveNPC(fighter, groups, posOptions, battleMap)
    

def movePlayer(fighter, groups, posOptions, battleMap) -> None:
    Select.waitPrint("Choose " + fighter.name + "'s Positional Action:")
    answer = Select.makeSelection(posOptions)

    if answer == "Move":
        stationary = Movement.moveFighter(fighter, battleMap, None, False)
        if stationary:
            if fighter.atrb["base_mar"] > 0: Moves.execute(fighter, groups, "Set", battleMap)
            else: Moves.execute(fighter, groups, "Evade", battleMap)
    elif answer in Moves.stationaryAbilities:
        Moves.execute(fighter, groups, answer, battleMap)
    elif answer in Area.areaAbilities:
        Area.execute(fighter, groups, answer, battleMap)


def moveNPC(fighter, groups, posOptions, battleMap) -> bool:
    reachable, fightingAllies, fightingEnemies = groups["reachable"], groups["fightingAllies"], groups["fightingEnemies"]
    reachableAllies, reachableEnemies = reachable["boonReachable"], reachable["attackReachable"] + reachable["hinderReachable"]
    stationary, choice = True, ""

    if fighter.atrb["cur_sp"] > 0:
        target, closeRanks = "None", False

        if (fighter.type == "human") and (len(reachableAllies) == 1) and (len(fightingAllies) > 1):
            closeRanks = True

            fightingAlliesMinusSelf = []
            for ally in fightingAllies:
                if ally != fighter: fightingAlliesMinusSelf += [ally]

            boonChoice = Boons.npcSelectBoon(fighter, fightingEnemies)
            if boonChoice != "None": target = Boons.npcSelectBoonTarget(fighter, fightingAlliesMinusSelf, boonChoice)
            else: target = random.choice(fightingAlliesMinusSelf)

        elif len(reachableEnemies) == 0:
            target = Attacks.npcSelectAttackTarget(fighter, fightingEnemies, True)

        if target != "None":
            stationary = Movement.moveFighter(fighter, battleMap, target, closeRanks)
                
    if stationary:
        if (target == "None") and ("Empower" in posOptions): posOptions -= ["Empower"]
        choice = random.choice(posOptions)
    if choice in Area.areaAbilities: Area.execute(fighter, groups, choice, battleMap)
    elif choice in Moves.stationaryAbilities: Moves.execute(fighter, groups, choice, battleMap)