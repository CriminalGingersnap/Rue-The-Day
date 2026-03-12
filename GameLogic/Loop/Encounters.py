from Systems import PlayerSelect as Select, Conditions, Commitments
from Biomes import Biomes
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat, Crafting


def encounterLoop(playerGroup, biome):
    play = True
    faceCards = {"Clubs": "Jack", "Hearts": "Jack", "Diamonds": "Jack", "Spades": "Jack"}
    
    while play:
        mapContours = Environment.randomEnvironment(faceCards)
        enemyGroups = Biomes.setFoes(biome, faceCards)

        battleMap = None
        if mapContours[2] == "ruin":
            battleMap = dMap.createMap(playerGroup, enemyGroups, mapContours, faceCards)
        else: battleMap = iMap.createMap(playerGroup, enemyGroups, mapContours, faceCards)

        playerVictory = Combat.engage(playerGroup, enemyGroups, battleMap)
        if playerVictory: handleAftermath(playerGroup, enemyGroups)
        else:
            Select.waitPrint("Reload Save?")
            # force a reload or restart
        
        play = Select.yesNo("Continue?")


def handleAftermath(victorGroup, loserGroups):
    takeRest = False

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
        
    if not takeRest: takeRest = Select.yesNo("Rest?")
    if takeRest: takeRest(victorGroup["groups"])
    
    pool = []
    for loserGroup in loserGroups:
        for vanquished in loserGroups:
          pool += vanquished.drop.inventory

    Select.waitPrint(pool)

    # Let player examine inventory and take desired items if they have capacity.


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