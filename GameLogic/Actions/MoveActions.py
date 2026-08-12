from Systems import PlayerSelect as Select
from . import ItemActions, ItemActions_NPC, BoonActions as Boons, AttackActions as Attacks
from Abilities import Move_Apply as Moves, Area_Set as Area
from Maps import Movement
import random, copy


def moveAction(fighter, groups, battleMap) -> None:
    posOptions = copy.deepcopy(fighter.abl["areas"])

    if fighter.atrb["cur_sp"] > 0: posOptions += ["Evade"]

    if ("Inventory -> Access" in posOptions) and not ItemActions.hasItems(fighter): posOptions.remove("Inventory -> Access")
    if "spares" in fighter.inv:
        if (fighter.inv["spares"]["weapon"]["name"] != "None"): posOptions += ["Swap Weapon"]
        if (fighter.inv["spares"]["shield"]["name"] != "None"): posOptions += ["Swap Shield"]

    if fighter.props["rank"] == "player":
        reachable = groups["reachable"]
        visibleTargets = reachable["visibleAllies"] + reachable["visibleEnemies"]
        if len(visibleTargets) > 1: posOptions += ["Examine"]
        else: posOptions += ["Examine -> " + visibleTargets[0].props["name"]]

        if fighter.atrb["cur_sp"] > 0: posOptions += ["Blitz", "Move"]
        if ("Inventory -> Access" in posOptions) and (ItemActions.getInventory(fighter)["Total"] > 1):
            posOptions += ["Inventory -> Rummage"]

        posOptions.sort()
        movePlayer(fighter, groups, posOptions, battleMap)

    else: moveNPC(fighter, groups, posOptions, battleMap)
    

def movePlayer(fighter, groups, posOptions, battleMap) -> None:
    answer = Select.pickOption(posOptions, fighter.props["name"] + "'s positional action")
    if "Examine" in answer: answer = "Examine"

    if answer in ["Blitz", "Move"]:
        stationary = True
        if answer == "Move": stationary = Movement.moveFighter(fighter, battleMap, None)
        if stationary: fighter.cndt["blitzing"] = True
    elif answer in Moves.stationaryAbilities:
        Moves.execute(fighter, groups, answer, battleMap)
    elif answer in Area.areaAbilities:
        Area.execute(fighter, groups, answer, battleMap)


def moveNPC(fighter, groups, posOptions, battleMap) -> bool:
    reachable, fightingAllies, fightingEnemies = groups["reachable"], groups["fightingAllies"], groups["fightingEnemies"]
    reachableAllies, reachableEnemies = reachable["boonReachable"], reachable["attackReachable"] + reachable["hinderReachable"]
    stationary, target, choice = True, "None", ""

    if fighter.atrb["cur_sp"] > 0:
        if (len(reachableEnemies) == 0) and ((len(fighter.abl["attacks"]) + len(fighter.abl["hindrances"])) > 0):
            target = Attacks.npcSelectAttackTarget(fighter, fightingEnemies, True)

        elif (len(reachableAllies) == 1) and (len(fightingAllies) > 1):
            fightingAlliesMinusSelf = []
            for ally in fightingAllies:
                if ally != fighter: fightingAlliesMinusSelf += [ally]

            boonChoice = Boons.npcSelectBoon(fighter, fightingEnemies)
            if boonChoice != "None": target = Boons.npcSelectBoonTarget(fighter, fightingAlliesMinusSelf, boonChoice)
            else: target = random.choice(fightingAlliesMinusSelf)

        if target != "None": stationary = Movement.moveFighter(fighter, battleMap, target)

    if stationary:
        itemSelection = "None"
        if "Inventory -> Access" in posOptions:
            inventory = ItemActions.getInventory(fighter)
            del inventory["Total"]
            itemSelection = ItemActions_NPC.npcSelectItem(fighter, groups, inventory)
            if itemSelection == "None": posOptions.remove("Inventory -> Access")

        if len(posOptions) == 0:
            Select.waitPrint(fighter.props["name"] + " sets in place and may use two abilities.")
            fighter.cndt["blitzing"] = True
        else: choice = random.choice(posOptions)

        if choice in Area.areaAbilities: Area.execute(fighter, groups, choice, battleMap)
        elif choice in Moves.stationaryAbilities: Moves.execute(fighter, groups, choice, battleMap, itemSelection)