from Characters import Elementals
from . import RandomCreatures, RandomElementals, RandomHumans
from Systems import Roll, PlayerSelect as Select
import random


def setFoes(biome, faceCards) -> list:
    Select.waitPrint("Rolling dice to determine encounter number.")
    Select.waitPrint("Group 1 roll:")
    roll1 = Roll.roll(None, 1, None, None)
    Select.waitPrint("Group 2 roll:")
    roll2 = Roll.roll(None, 2, None, None)

    rolls = [roll1, roll2]
    index, groups = 0, [[], []]
    
    for roll in rolls:
        members = []
        match biome:
            case "Pass": members = passEncounters(roll, faceCards)
            case "Bay": members = bayEncounters(roll, faceCards)
            case "Fjord": members = fjordEncounter(roll, faceCards)
            case "Glacier": members = glacierEncounters(roll, faceCards)
            # case "GhostWood": members = ghostWoodEncounters(roll, faceCards)
            case "Peninsula": members = peninsulaEncounters(roll, faceCards)
            case "Volcano": members = volcanoEncounters(roll, faceCards)

            # case "Kingdom": members = kingdomEncounters(roll, faceCards)
            # case "Outlaw": members = outlawEncounters(roll, faceCards)
            # case "Shoreline": members = shorelineEncounters(roll, faceCards)

            # case "SeaCave": members = seaCaveEncounters(roll, faceCards)
            # case "DeadTown": members = deadTownEncounters(roll, faceCards)
            # case "BlessedScrubland": members = sacredDesertEncounters(roll, faceCards)
            # case "SacredDesert": members = sacredDesertEncounters(roll, faceCards)
            # case "BurialValley": members = burialValleyEncounters(roll, faceCards)

        match faceCards["Diamonds"]:
            case "King":
                if () and random.choice([False, False, True]):
                    members += [Elementals.wisp(faceCards, "Random").ch]
            case "Queen":
                if () and random.choice([False, False, False, False, False, True]):
                    members += [Elementals.wisp(faceCards, "Random").ch]

        for i in len(members): members[i].name += "[" + str(i) + "]"
        groups[index] = members
        index += 1

    return groups


# the low pass is a valley between two mountains. It crosses from the dry starting prairie into a lush bay.
def passEncounters(roll, environment) -> list:
    members = []

    match roll:
        case 1: members = RandomHumans.soldiers("Elite", environment)
        case 2: members = RandomHumans.soldiers("Adept", environment)
        case 3: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 4: members = RandomCreatures.creatures("hound", environment, "Basic")
        case 5: members = RandomCreatures.creatures("lizard", environment, "Basic")
        case 6: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("beetle", environment, "Basic")
        case 8: members = RandomCreatures.creatures("isopod", environment, "Basic")
        case 9: members = RandomCreatures.creatures("urchin", environment, "Basic")
        case 10: members = RandomCreatures.creatures("deer", environment, "Basic")
        case 11: members = RandomCreatures.creatures("rabbit", environment, "Basic")
        # case 12: members = RandomCreatures.creatures()

    return members

# Deep wild lowlands between the mountains and the fjord. Coniferous trees. Pervasive light mist.
def bayEncounters(roll, environment) -> list:
    members, element = [], "Basic"

    match roll:
        case 1: members = RandomHumans.soldiers("elite", environment)
        case 2: members = RandomCreatures.creatures("bear", environment, element)
        case 3: members = RandomCreatures.creatures("moose", environment, element)
        case 4: members = RandomCreatures.creatures("wyrm", environment, "Toxin")
        case 5: members = RandomCreatures.creatures("lizard", environment, "Basic")
        case 6: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("beetle", environment, "Basic")
        case 8: members = RandomCreatures.creatures("isopod", environment, "Basic")
        case 9: members = RandomCreatures.creatures("urchin", environment, "Basic")
        case 10: members = RandomCreatures.creatures("deer", environment, "Basic")
        case 11: members = RandomCreatures.creatures("rabbit", environment, "Basic")
        # case 12: members = RandomCreatures.creatures()

    return members


# The fjord cuts between the wilds and the Feywood. Players need to navigate around the water to reach that biome.
# Players can access the Feywood from the glacier.
def fjordEncounter(roll, environment) -> list:
    members, element = [], "Ice"

    match roll:
        case 1: members = RandomElementals.elementals("dancer", environment, element, False)
        case 2: members = RandomElementals.elementals("hulk", environment, element, False)
        case 3: members = RandomElementals.elementals("wisps", environment, element, False)
        case 4: members = RandomCreatures.creatures("bear", environment, element)
        case 5: members = RandomCreatures.creatures("hound", environment, "Flame")
        case 6: members = RandomCreatures.creatures("hound", environment, element)
        case 7: members = RandomCreatures.creatures("moose", environment, "Fey")
        case 8: members = RandomCreatures.creatures("moose", environment, element)
        case 9: members = RandomCreatures.creatures("urchin", environment, element)
        case 10: members = RandomCreatures.creatures("deer", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members


# Glacier tube battleMaps have the highest obstruction count in the game. 17?
# Glacier boss map changes as the worm carves new tunnels
def glacierEncounters(roll, environment) -> list:
    members, element = [], "Ice"

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", environment, element, True)
        case 2: members = RandomElementals.elementals("dancer", environment, element, True)
        case 3: members = RandomElementals.elementals("hulk", environment, element, True)
        case 4: members = RandomElementals.elementals("wisps", environment, element, True)
        case 5: members = RandomCreatures.creatures("bear", environment, element)
        case 6: members = RandomCreatures.creatures("ferret", environment, element)
        case 7: members = RandomCreatures.creatures("mole", environment, element)
        case 8: members = RandomCreatures.creatures("gopher", environment, "Flame")
        case 9: members = RandomCreatures.creatures("sheep", environment, element)
        case 10: members = RandomCreatures.creatures("urchin", environment, element)
        case 11: members = RandomCreatures.creatures("worm", environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members


# The peninsula is a humid jungle. The volcano's magic warms the area, and the humid sea breeze carries frequent rain.
# These factors create a biome that feels wholly out of place in its environment. To Laura and Martin, it looks like another world.

# Slow rivers of lava flow down the mountain side, impeding their hike.
# They observe some of the native animals dashing across the narrowest sections.
def peninsulaEncounters(roll, environment) -> list:
    members, element = [], "Flame"

    match roll:
        case 1: members = RandomElementals.elementals("ooze", environment, element, False)
        case 2: members = RandomElementals.elementals("puffer", environment, element, False)
        case 3: members = RandomCreatures.creatures("drake", environment, element)
        case 4: members = RandomCreatures.creatures("wyrm", environment, "Toxin")
        case 5: members = RandomCreatures.creatures("lizard", environment, "Basic")
        case 6: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("beetle", environment, element)
        case 8: members = RandomCreatures.creatures("isopod", environment, "Basic")
        case 9: members = RandomCreatures.creatures("centipede", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("ant", environment, element)
        case 11: members = RandomCreatures.creatures("turtle", environment, "Basic")
        # case 12: members = RandomCreatures.creatures()

    return members


# post boss fight, players catch a view of the ocean on the volcano's far side

# The volcano boss fight has an expanded map with rivers of lava it can dash across
# It ambushes the players when they try to initiate its fight
def volcanoEncounters(roll, environment) -> list:
    members, element = [], "Flame"

    match roll:
        case 1: members = RandomElementals.elementals("hive", environment, element, True)
        case 1: members = RandomElementals.elementals("ooze", environment, element, True)
        case 2: members = RandomElementals.elementals("puffer", environment, element, True)
        case 3: members = RandomCreatures.creatures("drake", environment, element)
        case 4: members = RandomCreatures.creatures("wyrm", environment, "Toxin")
        case 5: members = RandomCreatures.creatures("lizard", environment, "Basic")
        case 6: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("beetle", environment, element)
        case 8: members = RandomCreatures.creatures("isopod", environment, "Basic")
        case 9: members = RandomCreatures.creatures("centipede", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("ant", environment, element)
        case 11: members = RandomCreatures.creatures("turtle", environment, "Basic")
        # case 12: members = RandomCreatures.creatures()

    return members