from . import CombatPhases as Phases, Crafting
from Actions import Sort
from Abilities import AttackAbilities as Attacks, Boons_Apply as Boons, Hindrances_Apply as Hinder
from Systems import Conditions, Commitments, PlayerSelect as Select
from Maps import Map_Update as uMap

# Add method to create phases in boss fights. Generate new maps for each phase.
# Add mist for the giant. Change tunnels for worm.

def challenge(playerGroup, enemyGroup, battleMap) -> None:
    playerAlacrity, enemyAlacrity = 0,0

    for player in playerGroup["members"]:
        mar, mag, fat = player.atrb["base_mar"], player.atrb["base_mag"], player.atrb["fatigue"]
        playerAlacrity += ((mar + mag) - fat)
    for enemy in enemyGroup["members"]:
        mar, mag, fat = enemy.atrb["base_mar"], enemy.atrb["base_mag"], enemy.atrb["fatigue"]
        enemyAlacrity += ((mar + mag) - fat)

    if playerAlacrity >= enemyAlacrity:
        firstActingGroup = playerGroup
        secondActingGroup = enemyGroup
    else:
        firstActingGroup = enemyGroup
        secondActingGroup = playerGroup
    
    Select.waitPrint("Contact!")
    Select.waitPrint("The " + firstActingGroup["name"] + " act first!")

    deserters = engage(firstActingGroup, secondActingGroup, battleMap)
    return deserters


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

    if group1Victory:
        victor = firstActingGroup
        loser = secondActingGroup
    elif group2Victory:
        victor = secondActingGroup
        loser = firstActingGroup

    handleAftermath(victor, loser)
    return deserters


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


def handleAftermath(victorGroup, loserGroup):
    if victorGroup["name"] == "questors":
        takeRest, cumWorth = False, 0

        for loser in loserGroup:
            cumWorth += loser.atrb["base_mar"]
            cumWorth += loser.atrb["base_mag"]

        for fighter in victorGroup["members"]:
            Commitments.clearCommitments(fighter)

            if fighter.type == "totem": fighter.cndt["reposed"] = True
            
            if fighter.atrb["cur_hp"] <= 0:
                Select.waitPrint(fighter.name + " requires immediate resuscitation!")
                takeRest = True
            elif fighter.atrb["fatigue"] >=  fighter.atrb["endurance"]:
                Select.waitPrint(fighter.name + " collapses from exhaustion!")
                takeRest = True
            elif fighter.atrb["corruption"] >=  Conditions.getTolerance(fighter):
                Select.waitPrint(fighter.name + " collapses from sickness!")
                takeRest = True
            
        if not takeRest:
            takeRest = Select.yesNo("Rest?")
        if takeRest: takeRest(victorGroup["members"])
        
        pool = []
        for enemy in loserGroup:
            pool += enemy.drop.inventory

        Select.waitPrint(pool)

        # Let player examine inventory and take desired items if they have capacity.
    else:
        Select.waitPrint("Reload Save?")
        return # force a reload or restart


def takeRest(group):
    for fighter in group:
        fighter.atrb["stamina"] = fighter.atrb["endurance"]
        fighter.atrb["fatigue"] = 0

        fighter.atrb["tolerance"] = Conditions.getTolerance(fighter)
        fighter.atrb["corruption"] = 0

        fighter.dead = False
        fighter.atrb["cur_hp"] = fighter.atrb["base_hp"]
        fighter.atrb["injury"] = 0

    if Select.yesNo("Craft?"): Crafting.craftLoop(group)

    # daysRemaining -= 1
    # If players fail to meet the deadline, Willem dies. They can skip one of the bosses and the fort battle.