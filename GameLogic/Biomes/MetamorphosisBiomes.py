from . import RandomCreatures, RandomElementals, RandomHumans
from Systems import PlayerSelect as Select, Roll


# the low pass is a valley between two mountains. It crosses from the dry starting prairie into a lush bay.
def passEncounters(roll, environment) -> list:
    members, element = [], "Basic"

    match roll:
        case 1: members = RandomHumans.soldiers(environment, element)
        case 2: members = RandomCreatures.creatures("wyrm", environment, element)
        case 3: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 4: members = RandomCreatures.creatures("hound", environment, element)
        case 5: members = RandomCreatures.creatures("lizard", environment, element)
        case 6: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("beetle", environment, element)
        case 8: members = RandomCreatures.creatures("isopod", environment, element)
        case 9: members = RandomCreatures.creatures("urchin", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("deer", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members

# Deep wild lowlands between the mountains and the fjord. Coniferous trees. Pervasive light mist.
def bayEncounters(roll, environment) -> list:
    members, element = [], "Basic"

    match roll:
        case 1: members = RandomHumans.soldiers(environment, element)
        case 2: members = RandomHumans.outlaws(environment, element)
        case 3: members = RandomCreatures.creatures("bear", environment, element)
        case 4: members = RandomCreatures.creatures("wyrm", environment, element)
        case 5: members = RandomCreatures.creatures("moose", environment, element)
        case 6: members = RandomCreatures.creatures("lizard", environment, element)
        case 7: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 8: members = RandomCreatures.creatures("isopod", environment, element)
        case 9: members = RandomCreatures.creatures("urchin", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("deer", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members


# The fjord cuts between the wilds and the Feywood. Players need to navigate around the water to reach that biome.
# Players can access the Feywood from the glacier.
def fjordEncounter(roll, environment) -> list:
    members, element = [], "Ice"

    match roll:
        case 1: members = RandomElementals.elementals("dancer", environment, element, False)
        case 2: members = RandomElementals.elementals("hulk", environment, element, False)
        case 3: members = RandomElementals.elementals("wisp", environment, element, False)
        case 4: members = RandomCreatures.creatures("bear", environment, element)
        case 5: members = RandomCreatures.creatures("hound", environment, "Flame")
        case 6: members = RandomCreatures.creatures("moose", environment, "Fey")
        case 7: members = RandomCreatures.creatures("sheep", environment, element)
        case 8: members = RandomCreatures.creatures("worm", environment, element)
        case 9: members = RandomCreatures.creatures("urchin", environment, element)
        case 10: members = RandomCreatures.creatures("deer", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        case 12: members = undeadEncounters("Fjord", environment)

    return members


# Glacier tube battleMaps have the highest obstruction count in the game. 17?
# Glacier boss map changes as the worm carves new tunnels
def glacierEncounters(roll, environment) -> list:
    members, element = [], "Ice"

    match roll:
        case 1: members = RandomElementals.elementals("wraith", environment, element, True)
        case 2: members = RandomElementals.elementals("dancer", environment, element, True)
        case 3: members = RandomElementals.elementals("hulk", environment, element, True)
        case 4: members = RandomElementals.elementals("wisp", environment, element, True)
        case 5: members = RandomCreatures.creatures("bear", environment, element)
        case 6: members = RandomCreatures.creatures("ferret", environment, "Flame")
        case 7: members = RandomCreatures.creatures("mole", environment, "Flame")
        case 8: members = RandomCreatures.creatures("gopher", environment, "Flame")
        case 9: members = RandomCreatures.creatures("sheep", environment, element)
        case 10: members = RandomCreatures.creatures("urchin", environment, element)
        case 11: members = RandomCreatures.creatures("worm", environment, "Flame")
        case 12: members = undeadEncounters("Glacier", environment)
    
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
        case 4: members = RandomCreatures.creatures("wyrm", environment, "Fey")
        case 5: members = RandomCreatures.creatures("ant", environment, element)
        case 6: members = RandomCreatures.creatures("hound", environment, "Ice")
        case 7: members = RandomCreatures.creatures("beetle", environment, element)
        case 8: members = RandomCreatures.creatures("isopod", environment, element)
        case 9: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("lizard", environment, element)
        case 11: members = RandomCreatures.creatures("tortoise", environment, element)
        case 12: members = undeadEncounters("Peninsula", environment)

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
        case 4: members = RandomCreatures.creatures("wyrm", environment, "Fey")
        case 5: members = RandomCreatures.creatures("lizard", environment, "Fey")
        case 6: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("beetle", environment, element)
        case 8: members = RandomCreatures.creatures("muscle", environment, element)
        case 9: members = RandomCreatures.creatures("centipede", environment, element)
        case 10: members = RandomCreatures.creatures("ant", environment, element)
        case 11: members = RandomCreatures.creatures("tortoise", environment, element)
        case 12: members = undeadEncounters("Volcano", environment)

    return members


def peripheryEncounters(roll, environment) -> list:
    members, element = [], "Fey"

    match roll:
        case 1: members = RandomElementals.elementals("satyr", environment, element, False)
        case 2: members = RandomElementals.elementals("nymph", environment, element, False)
        case 3: members = RandomElementals.elementals("wisp", environment, element, False)
        case 4: members = RandomCreatures.creatures("bear", environment, element)
        case 5: members = RandomCreatures.creatures("hound", environment, "Flame")
        case 6: members = RandomCreatures.creatures("ferret", environment, element)
        case 7: members = RandomCreatures.creatures("moose", environment, element)
        case 8: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("urchin", environment, "Ice")
        case 10: members = RandomCreatures.creatures("deer", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        case 12: members = undeadEncounters("Periphery", environment)

    return members

def depthsEncounters(roll, environment) -> list:
    members, element = [], "Fey"

    match roll:
        case 1: members = RandomElementals.elementals("ogre", environment, element, False)
        case 2: members = RandomElementals.elementals("satyr", environment, element, False)
        case 3: members = RandomElementals.elementals("nymph", environment, element, False)
        case 4: members = RandomElementals.elementals("wisp", environment, element, False)
        case 5: members = RandomCreatures.creatures("bear", environment, element)
        case 6: members = RandomCreatures.creatures("hound", environment, element)
        case 7: members = RandomCreatures.creatures("ferret", environment, element)
        case 8: members = RandomCreatures.creatures("moose", environment, element)
        case 9: members = RandomCreatures.creatures("urchin", environment, "Ice")
        case 10: members = RandomCreatures.creatures("deer", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        case 12: members = undeadEncounters("Depths", environment)


    return members


def undeadEncounters(biome, environment):
    members, element = [], "Corpse"
    Select.waitPrint("Rolling dice to determine undead encounter number.")
    Select.waitPrint("Group 2 roll:")
    roll = Roll.roll(None, 1, None, None)

    match biome:
        case "Depths" | "Periphery":
            match roll:
                case 1: members = RandomCreatures.creatures("bear", environment, element)
                case 2: members = RandomCreatures.creatures("hound", environment, element)
                case 3: members = RandomCreatures.creatures("ferret", environment, element)
                case 4: members = RandomCreatures.creatures("moose", environment, element)
                case 5: members = RandomCreatures.creatures("deer", environment, element)
                case 6: members = RandomCreatures.creatures("rabbit", environment, element)
        case "Peninsula" | "Volcano":
            match roll:
                    case 1: members = RandomCreatures.creatures("drake", environment, element)
                    case 2: members = RandomCreatures.creatures("wyrm", environment, element)
                    case 3: members = RandomCreatures.creatures("lizard", environment, element)
                    case 4: members = RandomCreatures.creatures("hound", environment, element)
                    case 5: members = RandomCreatures.creatures("tortoise", environment, element)
                    case 6: members = RandomCreatures.creatures("centipede", environment, element)
        case "Fjord" | "Glacier":
            match roll:
                case 1: members = RandomCreatures.creatures("bear", environment, element)
                case 2: members = RandomCreatures.creatures("hound", environment, element)
                case 3: members = RandomCreatures.creatures("ferret", environment, element)
                case 4: members = RandomCreatures.creatures("mole", environment, element)
                case 5: members = RandomCreatures.creatures("sheep", environment, element)
                case 6: members = RandomCreatures.creatures("worm", environment, element)

    return members