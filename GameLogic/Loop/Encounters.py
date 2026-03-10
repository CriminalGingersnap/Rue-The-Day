from Characters import Humans, AvoidantBeasts as Avoidant
from Systems import PlayerSelect as Select, Conditions, Commitments
import Biomes.Wild1_ValleyPass as LowPass
from Maps import Map_Instantiate as iMap, Dungeon_Instantiate as dMap
from . import Environment, Combat, Crafting
import random


def encounterLoop(playerGroup, biome):
    play = True
    faceCards = {"Clubs": random.choice(["Jack", "Queen", "King"]),
                  "Hearts": random.choice(["Jack", "Queen", "King"]),
                   "Diamonds": random.choice(["Jack", "Queen", "King"]),
                    "Spades": random.choice(["Jack", "Queen", "King"])}
    
    while play:
        results = Environment.randomEnvironment(faceCards)
        obstructions, atmosphere, slope = results[0], results[1], results[2]

        enemyGroup = setFoes(biome, faceCards)

        battleMap = None
        if slope == "ruin":
            battleMap = dMap.createMap(playerGroup["members"], enemyGroup["members"], [obstructions, atmosphere], faceCards)
        else: battleMap = iMap.createMap(playerGroup["members"], enemyGroup["members"], [obstructions, atmosphere], faceCards, slope)

        survivors = Combat.engage(enemyGroup, playerGroup, battleMap)
        handleAftermath(survivors[0], survivors[1])
        for deserter in survivors[2]: Select.waitPrint(deserter.name) # let players hunt them down
        
        play = Select.yesNo("Continue?")


def setFoes(biome, faceCards) -> dict:
    members = []

    match biome:
        case "Wild": members = LowPass.randomForestEncounters(faceCards)

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