from Systems import PlayerSelect as Select
from . import ItemActions, BoonActions as Boons, AttackActions as Attacks
from Abilities import Move_Apply as Moves, Area_Set as Area
from Maps import Movement
import random, copy


def moveAction(fighter, groups, battleMap) -> None:
    posOptions = copy.deepcopy(fighter.abl["areas"])

    if (fighter.atrb["cur_mag"] > 0) and (fighter.atrb["cur_mar"] > 0): posOptions += ["Empower"]
    
    if ("Inventory" in fighter.abl["boons"]) and ItemActions.hasItems(fighter): posOptions += ["Inventory"]
    if "spares" in fighter.inv:
        if (fighter.inv["spares"]["weapon"]["name"] != "None"): posOptions += ["Swap Weapon"]
        if (fighter.inv["spares"]["shield"]["name"] != "None"): posOptions += ["Swap Shield"]

    if fighter.props["rank"] == "player":
        reachable = groups["reachable"]
        visibleTargets = reachable["visibleAllies"] + reachable["visibleEnemies"]
        if len(visibleTargets) > 1: posOptions += ["Examine"]
        else: posOptions += ["Examine -> " + visibleTargets[0].props["name"]]

        if fighter.atrb["cur_sp"] > 0: posOptions += ["Move", "Stay"]
        movePlayer(fighter, groups, posOptions, battleMap)
    else:
        if fighter.atrb["cur_sp"] > 0: posOptions += ["Move"]
        moveNPC(fighter, groups, posOptions, battleMap)
    

def movePlayer(fighter, groups, posOptions, battleMap) -> None:
    answer = Select.pickOption(posOptions, fighter.props["name"] + "'s positional action")
    if "Examine" in answer: answer = "Examine"

    if answer in ["Move", "Stay"]:
        stationary = True
        if answer == "Move": stationary = Movement.moveFighter(fighter, battleMap, None, False)
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
    stationary, target, choice = True, "None", ""

    if fighter.atrb["cur_sp"] > 0:
        closeRanks = False

        if (fighter.props["type"] == "human") and (len(reachableAllies) == 1) and (len(fightingAllies) > 1):
            closeRanks = True

            fightingAlliesMinusSelf = []
            for ally in fightingAllies:
                if ally != fighter: fightingAlliesMinusSelf += [ally]

            boonChoice = Boons.npcSelectBoon(fighter, fightingEnemies)
            if boonChoice != "None": target = Boons.npcSelectBoonTarget(fighter, fightingAlliesMinusSelf, boonChoice)
            else: target = random.choice(fightingAlliesMinusSelf)

        elif len(reachableEnemies) == 0:
            target = Attacks.npcSelectAttackTarget(fighter, fightingEnemies, True)

        if target != "None": stationary = Movement.moveFighter(fighter, battleMap, target, closeRanks)
                
    if stationary:
        if "Empower" in posOptions: posOptions.remove(["Empower"])
        
        if len(posOptions) == 0:            
            if fighter.atrb["base_mar"] > 0: choice = "Set"
            else: choice = "Evade"
        else: choice = random.choice(posOptions)

    if choice in Area.areaAbilities: Area.execute(fighter, groups, choice, battleMap)
    elif choice in Moves.stationaryAbilities: Moves.execute(fighter, groups, choice, battleMap)