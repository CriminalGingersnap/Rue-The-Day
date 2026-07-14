from . import CombatPhases as Phases, Loot
from Actions import Sort
from Abilities import AttackAbilities as Attacks, Hindrances_Apply as Hinder
from Systems import Commitments, PlayerSelect as Select
from Maps import Map_Update as uMap

# Add method to create phases in boss fights. Generate new maps for each phase.
# Add mist for the giant. Change tunnels for worm.


def engage(playerGroup, enemyGroups, battleMap) -> list:
    input("\nPress Enter to begin combat.")

    playerVictory, playerDefeat = False, False
    group1, group2, group3 = playerGroup, enemyGroups[0], enemyGroups[1]

    while not (playerVictory or playerDefeat):
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
    validFighters = Sort.sortLiving(offenseGroup)[0]
    if len(validFighters) > 0:
        for fighter in validFighters:
            validTargets = Sort.sortLiving(targetGroup)[0]

            if len(validTargets) == 0:
                Select.slowPrint("\nBattle Over.\n")
                input("Press Enter to resolve.")
                return True
            else: Phases.resetFighter(fighter)

        friends, foes = offenseGroup, validTargets
        for fighter in validFighters:
            Hinder.applyCompel(fighter, "Compel")
            if fighter.effects["Compel"]["additional"]: friends, foes = validTargets, offenseGroup
            Hinder.applyCompel(fighter, "Seal")
            if fighter.effects["Seal"]["additional"]: fighter.atrb["cur_mar"], fighter.atrb["cur_mag"] = 0, 0
            uMap.activateHazards(fighter, battleMap)
        
        uMap.updateHazards(battleMap)

        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap)
            Phases.movementStage(fighter, foes, friends, battleMap)
            
        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap)
            Phases.abilityStage(fighter, foes, friends, battleMap)
        
        for fighter in validFighters:
            if len(fighter.actionQueue) > 0:
                Commitments.checkReach(fighter)
                Select.waitPrint("\nExecuting " + fighter.props["name"] + "'s actions:")

                for action in fighter.actionQueue:
                    ability, target, dice = action[1], action[2], action[3]
                    match action[0]:
                        case "attack":
                            if target.cndt["dead"] == False:
                                Attacks.execute(fighter, target, ability, dice)
                            else: Select.waitPrint("Attack canceled against slain target.")
                                    
                    fighter.actionQueue.remove(action)
            Phases.outro(fighter, offenseGroup, validFighters, battleMap)
            
    return False


def restart():
    return # Let players quickly restart an encounter.
            # Also provide a quit and reload option to pick up from the last safe rest.
            # Only save game at rest sites. Require players to complete at least one encounter before resting.
            # Present the player with a rests-remaining counter after the old rival event? Choose a later event to start the countdown?