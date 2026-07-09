from Systems import PlayerSelect as Select, Conditions, Commitments
from GameState import SaveLoad as Save
from Biomes import Biomes
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat


def encounterLoop(playerGroup, biome):
    play, ace = True, "Clubs"
    players = playerGroup["members"]
    
    while play:
        mapConditions = Environment.randomEnvironment(biome)
        enemyGroups = Biomes.setFoes(biome, mapConditions["budget"], mapConditions["curse"])

        battleMap = None
        if mapConditions["slope"] == "ruin":
            battleMap = dMap.createMap(players, enemyGroups, mapConditions, ace)
        else: battleMap = iMap.createMap(players, enemyGroups, mapConditions, ace)

        playerVictory = Combat.engage(players, enemyGroups, battleMap)
        if playerVictory:
            takeRest = handleAftermath(players)
            if takeRest:
                takeRest(playerGroup)
                ace = Environment.updateAce(ace, biome)
        else:
            Select.waitPrint("Reload Save?")
            # force a reload or restart
        
        play = Select.yesNo("Continue?")


def handleAftermath(victorGroup) -> bool:
    takeRest = False

    for fighter in victorGroup:
        Commitments.clearCommitments(fighter)

        if fighter.props["type"] == "totem": fighter.cndt["reposed"] = True
        
        if fighter.atrb["cur_hp"] <= 0:
            Select.waitPrint(fighter.props["name"] + " requires immediate resuscitation!")
            takeRest = True
        elif fighter.atrb["fatigue"] >=  fighter.atrb["endurance"]:
            Select.waitPrint(fighter.props["name"] + " collapses from exhaustion!")
            takeRest = True
        elif fighter.atrb["corruption"] >=  Conditions.getTolerance(fighter):
            Select.waitPrint(fighter.props["name"] + " collapses from sickness!")
            takeRest = True

    if not takeRest: takeRest = Select.yesNo("Rest?")
    return takeRest


def takeRest(group):
    for fighter in group["members"]:
        fighter.atrb["stamina"] = fighter.atrb["endurance"]
        fighter.atrb["fatigue"] = 0

        fighter.atrb["tolerance"] = Conditions.getTolerance(fighter)
        fighter.atrb["corruption"] = 0

        fighter.dead = False
        fighter.atrb["cur_hp"] = fighter.atrb["base_hp"]
        fighter.atrb["injury"] = 0

        group["days"] += 1
        Save.saveGroup(group)