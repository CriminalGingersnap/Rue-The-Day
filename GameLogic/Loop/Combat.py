from . import CombatPhases as Phases
from Abilities import AttackAbilities as Attacks, Hindrances_Apply as Hinder
from Systems import Commitments, PlayerSelect as Select, Sort
from Maps import Map_Update as uMap


def engage(playerGroup, enemyGroups, battleMap, atmosphere) -> list:
    Select.pressEnter("begin combat")

    playerVictory, playerDefeat, result = False, False, []
    group1, group2, group3 = playerGroup, enemyGroups[0], enemyGroups[1]

    for fighter in group1: fighter.sightMap = Phases.setSight(fighter, group2 + group3, group1, battleMap, False)
    for fighter in group2: fighter.sightMap = Phases.setSight(fighter, group1 + group3, group2, battleMap, False)
    for fighter in group3: fighter.sightMap = Phases.setSight(fighter, group1 + group2, group3, battleMap, False)

    while not (playerVictory or playerDefeat):
        result = battle(group1, group2 + group3, battleMap, atmosphere)
        playerVictory = result[0]
        if not playerVictory:
            if not playerDefeat: playerDefeat = battle(group2, group1 + group3, battleMap, atmosphere)[0]
            if not playerDefeat: playerDefeat = battle(group3, group1 + group2, battleMap, atmosphere)[0]

    return result


def battle(offenseGroup, targetGroup, battleMap, atmosphere) -> bool:
    sortedOffense, sortedTarget = Sort.sortLiving(offenseGroup, battleMap), Sort.sortLiving(targetGroup, battleMap)
    validFighters, validTargets, downedFighters, downedTargets, pacifistTargets = sortedOffense[0], sortedTarget[0], sortedOffense[1], sortedTarget[1], sortedTarget[2]
    npcGroup = offenseGroup[0].props["rank"] != "player"

    if any(((fighter.props["rank"] == "player") and (fighter.props["type"] not in ["echo", "totem"])) for fighter in downedFighters):
        return [False, None]
    elif any(((target.props["rank"] == "player") and (target.props["type"] not in ["echo", "totem"])) for target in downedTargets):
        Select.clearPrint("Battle lost.")
        Select.pressEnter("resolve")
        return [True, None]
    elif len(validTargets) == 0:
        Select.quickPrint("Control established over fate-spring. Saving enabled.", "")
        Select.pressEnter("resolve")
        return [True, downedTargets]
    elif (not npcGroup) and (len(validTargets) == len(pacifistTargets)):
        Select.waitPrint("Remaining enemies will allow combat to end.")
        if Select.yesNo("Disengage?"): return  [True, downedTargets]
    
    if len(validFighters) > 0:
        friends, foes = validFighters, validTargets

        for fighter in validFighters:
            Phases.resetFighter(fighter)
            
            Hinder.applyCompel(fighter, "Compel")
            if fighter.effects["Compel"]["additional"]: friends, foes = validTargets, validFighters
            Hinder.applyCompel(fighter, "Seal")
            if fighter.effects["Seal"]["additional"]: fighter.atrb["cur_mar"], fighter.atrb["cur_mag"] = 0, 0

            uMap.activateHazards(fighter, battleMap)

        uMap.updateHazards(battleMap)
        uMap.addHazards(battleMap, atmosphere)

        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap, True)
            Phases.movementStage(fighter, foes, friends, battleMap)

        for target in validTargets:
            target.sightMap = Phases.setSight(target, friends, foes, battleMap, False)

        print()
        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap, True)
            Phases.abilityStage(fighter, foes, friends, battleMap)

        if npcGroup and any((len(fighter.attackQueue) > 0) for fighter in validFighters):
            Select.pressEnter("execute abilities")

        for fighter in validFighters:
            if len(fighter.attackQueue) > 0:
                Commitments.checkReach(fighter)
                Select.clearPrint("Executing " + fighter.props["name"] + "'s attacks:")

                for attack in fighter.attackQueue:
                    ability, target, dice = attack[0], attack[1], attack[2]
                    if target.cndt["dead"]: Select.waitPrint("Attack canceled against slain target.")
                    else:
                        Select.waitPrint(ability + " triggers against " + target.props["name"] + "!")
                        Attacks.execute(fighter, target, ability, dice)

            Phases.outro(fighter)
        Select.pressEnter("advance combat to the next round")
    return [False, None]