from . import CombatPhases as Phases, Loot
from Abilities import AttackAbilities as Attacks, Hindrances_Apply as Hinder
from Systems import Commitments, PlayerSelect as Select, Sort
from Maps import Map_Update as uMap

# Add method to create phases in boss fights. Generate new maps for each phase.
# Add mist for the giant. Change tunnels for worm.


def engage(playerGroup, enemyGroups, battleMap) -> list:
    input("\nPress Enter to begin combat.")

    playerVictory, playerDefeat = False, False
    group1, group2, group3 = playerGroup, enemyGroups[0], enemyGroups[1]

    for fighter in group1: fighter.sightMap = Phases.setSight(fighter, group2 + group3, group1, battleMap, False)
    for fighter in group2: fighter.sightMap = Phases.setSight(fighter, group1 + group3, group2, battleMap, False)
    for fighter in group3: fighter.sightMap = Phases.setSight(fighter, group1 + group2, group3, battleMap, False)

    while not (playerVictory or playerDefeat):
        Select.waitPrint("\nNew round beginning.\n")
        uMap.updateHazards(battleMap)

        playerVictory = battle(group1, group2 + group3, battleMap)
        if not (playerVictory or playerDefeat):
            playerDefeat = battle(group2, group1 + group3, battleMap)
        if not (playerVictory or playerDefeat):
            playerDefeat = battle(group3, group1 + group2, battleMap)
        
    if playerVictory:
        Loot.searchAll(group1, group2 + group3)
        return True
    else:
        return False


def battle(offenseGroup, targetGroup, battleMap) -> bool:
    validFighters, validTargets = Sort.sortLiving(offenseGroup, battleMap)[0], Sort.sortLiving(targetGroup, battleMap)[0]

    if len(validTargets) == 0:
        Select.slowPrint("\nBattle Over.\n")
        input("Press Enter to resolve.")
        return True
    
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
            
        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap, True)
            Phases.abilityStage(fighter, foes, friends)
        
        for fighter in validFighters:
            if len(fighter.attackQueue) > 0:
                Commitments.checkReach(fighter)
                Select.waitPrint("\nExecuting " + fighter.props["name"] + "'s attacks:")

                for attack in fighter.attackQueue:
                    ability, target, dice = attack[0], attack[1], attack[2]
                    if target.cndt["dead"]: Select.waitPrint("Attack canceled against slain target.")
                    else: Attacks.execute(fighter, target, ability, dice)

                    fighter.attackQueue.remove(attack)
            Phases.outro(fighter, offenseGroup, battleMap)
    
    input("\nPress Enter to advance combat to the next round.\n")
    return False


def restart():
    return # Let players quickly restart an encounter.
            # Also provide a quit and reload option to pick up from the last safe rest.
            # Only save game at rest sites. Require players to complete at least one encounter before resting.
            # Present the player with a rests-remaining counter after the old rival event? Choose a later event to start the countdown?