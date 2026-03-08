from . import CombatPhases as Phases
from Actions import Sort
from Abilities import AttackAbilities as Attacks, Boons_Apply as Boons, Hindrances_Apply as Hinder
from Systems import Commitments, PlayerSelect as Select
from Maps import Map_Update as uMap

# Add method to create phases in boss fights. Generate new maps for each phase.
# Add mist for the giant. Change tunnels for worm.


def engage(firstActingGroup, secondActingGroup, battleMap) -> list:
    input("Press Enter to begin combat.")

    group1Victory, group2Victory, victor = False, False, None
    group1, group2 = firstActingGroup["members"], secondActingGroup["members"]
    deserters = None

    # for fighter in group1 + group2: Items.invigorate(fighter, "Tinctures", "")

    while not (group1Victory or group2Victory):
        outcome1 = battle(group1, group2, deserters, battleMap)
        group1Victory, group1 = outcome1[0], outcome1[1]
        deserters = outcome1[2]
        outcome2 = battle(group2, group1, deserters, battleMap)
        group2Victory, group2 = outcome2[0], outcome2[1]
        deserters = outcome2[2]

    victors, losers = None, None
    if group1Victory:
        victors = firstActingGroup
        losers = secondActingGroup
    elif group2Victory:
        victors = secondActingGroup
        losers = firstActingGroup

    return [victors, losers, deserters]


def battle(offenseGroup, targetGroup, deserters, battleMap) -> bool:    
    validFighters = Sort.sortLiving(offenseGroup)[0]
    if len(validFighters) > 0:
        for fighter in validFighters:
            validTargets = Sort.sortLiving(targetGroup)[0]

            if len(validTargets) == 0:
                Select.slowPrint("\nBattle Over.")
                input("Press Enter to resolve.")
                return [True, offenseGroup]
            else: Phases.resetFighter(fighter)
                    
    if len(validFighters) > 0:
        friends, foes = offenseGroup, validTargets
        for fighter in validFighters:
            Hinder.applyCompel(fighter, "Compel")
            if fighter.effects["Compel"]["additional"]: friends, foes = validTargets, offenseGroup
            Hinder.applyCompel(fighter, "Seal")
            if fighter.effects["Seal"]["additional"]: fighter.atrb["cur_mar"], fighter.atrb["cur_mag"] = 0, 0
        
        for fighter in validFighters:
            uMap.activateHazards(fighter, battleMap)
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap)
            Phases.movementStage(fighter, foes, friends, battleMap)
        uMap.updateHazards(battleMap)

        for fighter in validFighters:
            if fighter.itemUse > 0:
                fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap)
                Phases.inventoryStage(fighter, foes, friends, battleMap)
            
        for fighter in validFighters:
            fighter.sightMap = Phases.setSight(fighter, foes, friends, battleMap)
            Phases.abilityStage(fighter, foes, friends, battleMap)

        validFighters = Sort.sortLiving(offenseGroup)[0]   
        
        for fighter in validFighters:
            if len(fighter.actionQueue) > 0:
                Commitments.checkReach(fighter)
                Select.waitPrint("\nExecuting " + fighter.name + "'s actions:")

                for action in fighter.actionQueue:
                    ability, target, dice = action[1], action[2], action[3]
                    match action[0]:
                        case "attack":
                            if target.cndt["dead"] == False:
                                Attacks.execute(fighter, target, ability, dice)
                            else: Select.waitPrint("Attack canceled against slain target.")
                        case "boon":
                            match ability:
                                case "Shroud":
                                    Boons.applyShroud(target)
                                    Commitments.checkReach(fighter)
                                    
                    fighter.actionQueue.remove(action)
            Phases.outro(fighter, validFighters, battleMap)
            

    return [False, offenseGroup, deserters]


def restart():
    return # Let players quickly restart an encounter.
            # Also provide a quit and reload option to pick up from the last safe rest.
            # Only save game at rest sites. Require players to complete at least one encounter before resting.
            # Present the player with a rests-remaining counter after the old rival event? Choose a later event to start the countdown?