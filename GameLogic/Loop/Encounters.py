from Systems import PlayerSelect as Select, Conditions, Commitments, Roll
from Biomes import Wild1_Pass as Pass, Wild2_Bay as Bay
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat, Crafting
import random


def encounterLoop(playerGroup, biome):
    play = True
    faceCards = {"Clubs": "Jack", "Hearts": "Jack", "Diamonds": "Jack", "Spades": "Jack"}
    
    while play:
        mapContours = Environment.randomEnvironment(faceCards)
        enemyGroup = setFoes(biome, faceCards)

        battleMap = None
        if mapContours[2] == "ruin":
            battleMap = dMap.createMap(playerGroup["members"], enemyGroup["members"], mapContours, faceCards)
        else: battleMap = iMap.createMap(playerGroup["members"], enemyGroup["members"], mapContours, faceCards)

        survivors = Combat.engage(enemyGroup, playerGroup, battleMap)
        handleAftermath(survivors[0], survivors[1])
        for deserter in survivors[2]: Select.waitPrint(deserter.name) # let players hunt them down
        
        play = Select.yesNo("Continue?")


def setFoes(biome, faceCards) -> dict:
    Select.waitPrint("Rolling dice to determine encounter number.")
    encounterRoll = Roll.castDice(2)
    members = []

    match biome:
        case "Pass": members = Pass.randomEncounters(encounterRoll, faceCards)
        case "Bay": members = Bay.randomEncounters(encounterRoll, faceCards)
        # case "Fjord": members = Fjord.randomEncounters(encounterRoll, faceCards)
        # case "Glacier": members = Glacier.randomEncounters(encounterRoll, faceCards)
        # case "Ghostwood": members = Ghostwood.randomEncounters(encounterRoll, faceCards)
        # case "Peninsula": members = Peninsula.randomEncounters(encounterRoll, faceCards)
        # case "Volcano": members = Volcano.randomEncounters(encounterRoll, faceCards)

    enemyGroup = {"members": [members], "name": "assassins"}
    return enemyGroup



def handleAftermath(victorGroup, loserGroup):
    if victorGroup["name"] == "questors":
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

    # daysRemaining -= 1
    # If players fail to meet the deadline, Willem dies. They can skip one of the bosses and the fort battle.

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