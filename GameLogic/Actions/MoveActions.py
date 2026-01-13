from Systems import PlayerSelect as Select
from . import ItemActions, BoonActions as Boons, AttackActions as Attacks
from Abilities import Move_Apply as Moves, Area_Set as Area
from Maps import Movement
import random


def moveAction(fighter, groups, battleMap) -> None:
    hasInventory = any(invAbl in fighter.abl["boons"] for invAbl in ["Inventory", "Quick Inventory"])
    posOptions = ["Set"] + fighter.abl["areas"]

    if hasInventory and ItemActions.hasItems(fighter): posOptions += ["Inventory"]
    if ("*" in battleMap[fighter.position[0]][fighter.position[1]]) and (fighter.atrb["base_mag"] > 0): posOptions += ["Tap"]

    if fighter.rank == "player":
        posOptions += ["Examine", "Movement"]
        movePlayer(fighter, groups, posOptions, battleMap)
    else: moveNPC(fighter, groups, posOptions, battleMap)
    

def movePlayer(fighter, groups, posOptions, battleMap) -> None:
    Select.waitPrint("Choose " + fighter.name + "'s Positional Action:")
    answer = Select.makeSelection(posOptions)

    if answer == "Movement":
        stationary = Movement.moveFighter(fighter, battleMap, None, False)
        if stationary: Moves.execute(fighter, groups, "Set")
    elif answer in Moves.stationaryAbilities:
        Moves.execute(fighter, groups, answer)
    elif answer in Area.areaAbilities:
        Area.execute(fighter, groups["fightingEnemies"], answer, battleMap)


def moveNPC(fighter, groups, posOptions, battleMap) -> bool:
    reachable, fightingAllies, fightingEnemies = groups["reachable"], groups["fightingAllies"], groups["fightingEnemies"]
    reachableAllies, reachableEnemies = reachable["boonReachable"], reachable["attackReachable"] + reachable["hinderReachable"]
    stationary, choice = True, ""

    if fighter.atrb["cur_sp"] > 0:
        target, getClose = "None", False

        if (fighter.type == "human") and (len(reachableAllies) == 1) and (len(fightingAllies) > 1):
            getClose = True

            fightingAlliesMinusSelf = []
            for ally in fightingAllies:
                if ally != fighter: fightingAlliesMinusSelf += [ally]

            boonChoice = Boons.npcSelectBoon(fighter, fightingEnemies)
            if boonChoice != "None": target = Boons.npcSelectBoonTarget(fighter, fightingAlliesMinusSelf, boonChoice)
            else: target = random.choice(fightingAlliesMinusSelf)

        elif len(reachableEnemies) == 0:
            target = Attacks.npcSelectAttackTarget(fighter, fightingEnemies)

        if target != "None":
            stationary = False
            Movement.moveFighter(fighter, battleMap, target, getClose)
                
    if stationary: choice = random.choice(posOptions)
    if choice in Area.areaAbilities: Area.execute(fighter, groups["fightingEnemies"], choice, battleMap)
    elif choice in Moves.stationaryAbilities: Moves.execute(fighter, groups, choice)
