from . import CombatPhases as Phases
from Abilities import AttackAbilities as Attacks, Hindrances_Apply as Hinder
from Systems import Commitments, PlayerSelect as Select, Sort
from Maps import Map_Update as uMap


def engage(playerGroup, enemyGroups, battleMap) -> list:
    input("\nPress Enter to begin combat.")

    playerVictory, playerDefeat, result = False, False, []
    group1, group2, group3 = playerGroup, enemyGroups[0], enemyGroups[1]

    for fighter in group1: fighter.sightMap = Phases.setSight(fighter, group2 + group3, group1, battleMap, False)
    for fighter in group2: fighter.sightMap = Phases.setSight(fighter, group1 + group3, group2, battleMap, False)
    for fighter in group3: fighter.sightMap = Phases.setSight(fighter, group1 + group2, group3, battleMap, False)

    while not (playerVictory or playerDefeat):
        uMap.updateHazards(battleMap)

        result = battle(group1, group2 + group3, battleMap)
        playerVictory = result[0]
        if not playerVictory:
            Select.waitPrint("\nCombat advances to the next round.\n")
            if not playerDefeat: playerDefeat = battle(group2, group1 + group3, battleMap)[0]
            if not playerDefeat: playerDefeat = battle(group3, group1 + group2, battleMap)[0]

    return result


def battle(offenseGroup, targetGroup, battleMap) -> bool:
    sortedOffense, sortedTarget = Sort.sortLiving(offenseGroup, battleMap), Sort.sortLiving(targetGroup, battleMap)
    validFighters, validTargets = sortedOffense[0], sortedTarget[0]
    downedFighters, downedTargets = sortedOffense[1], sortedTarget[1]
    pacifistTargets = sortedTarget[2]
    npcGroup = offenseGroup[0].props["rank"] != "player"

    if any(((fighter.props["rank"] == "player") and (fighter.props["type"] not in ["echo", "totem"])) for fighter in downedFighters):
        return [False, None]
    elif any(((target.props["rank"] == "player") and (target.props["type"] not in ["echo", "totem"])) for target in downedTargets):
        Select.slowPrint("\nPlayer defeat.\n")
        input("Press Enter to resolve.")
        return [True, None]
    elif len(validTargets) == 0:
        Select.slowPrint("\nBattle won!\n")
        input("Press Enter to resolve.")
        return [True, downedTargets]
    elif (not npcGroup) and (len(validTargets) == len(pacifistTargets)):
        Select.waitPrint("Remaining enemies will allow combat to end.")
        disengage = Select.yesNo("Disengage?")
        if disengage: return  [True, downedTargets]
    
    elif len(validFighters) > 0:
        for fighter in validFighters: Phases.resetFighter(fighter)

        friends, foes = validFighters, validTargets
        for fighter in validFighters:
            Hinder.applyCompel(fighter, "Compel")
            if fighter.effects["Compel"]["additional"]: friends, foes = validTargets, validFighters
            Hinder.applyCompel(fighter, "Seal")
            if fighter.effects["Seal"]["additional"]: fighter.atrb["cur_mar"], fighter.atrb["cur_mag"] = 0, 0
            uMap.activateHazards(fighter, battleMap)

        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap, True)
            Phases.movementStage(fighter, foes, friends, battleMap)

        print()
        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap, True)
            Phases.abilityStage(fighter, foes, friends)

        if npcGroup: input("\nPress Enter to execute attacks.")

        for fighter in validFighters:
            if len(fighter.attackQueue) > 0:
                Commitments.checkReach(fighter)
                Select.waitPrint("\n\nExecuting " + fighter.props["name"] + "'s attacks:")

                for attack in fighter.attackQueue:
                    ability, target, dice = attack[0], attack[1], attack[2]
                    if target.cndt["dead"]: Select.waitPrint("Attack canceled against slain target.")
                    else: Attacks.execute(fighter, target, ability, dice)

            Phases.outro(fighter)

        if npcGroup: input("\nPress Enter to advance combat to the next round.\n")

    return [False, None]