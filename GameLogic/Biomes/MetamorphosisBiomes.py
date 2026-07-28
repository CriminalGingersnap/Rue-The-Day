from . import RandomCreatures, RandomElementals, RandomHumans


# the low pass is a valley between two mountains. It crosses from the dry starting prairie into a lush bay.
def passEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    match roll:
        case 1: members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        case 2: members = RandomCreatures.creatures("wyrm", "Toxic", majorBiome, budget)
        case 3: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("eagle", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("crow", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("hornet", "Toxic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("beetle", "Toxic", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("bat", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("lizard", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("eagle", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("hound", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("wyrm", "Rot", majorBiome, budget)

    return members

# Deep wild lowlands between the mountains and the fjord. Coniferous trees. Pervasive light mist.
def bayEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", True

    match roll:
        case 1: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 2: members = RandomCreatures.creatures("bear", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("wyrm", "Toxic", majorBiome, budget)
        case 4: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("moose", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("eagle", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("hornet", "Toxic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("urchin", "Toxic", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("bat", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("hound", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("wyrm", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("bear", "Rot", majorBiome, budget)
        case 15: members = RandomHumans.warriors("Outlaw", "Rot", majorBiome, budget)

    return members


# The peninsula is a humid jungle. The volcano's magic warms the area, and the humid sea breeze carries frequent rain.
# These factors create a biome that feels wholly out of place in its environment. To Laura and Martin, it looks like another world.

# Slow rivers of lava flow down the mountain side, impeding their hike.
# They observe some of the native animals dashing across the narrowest sections.
def peninsulaEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Flame", False

    match roll:
        case 1: members = RandomElementals.elementals("ooze", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("puffer", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("wyrm", "Toxic", majorBiome, budget)
        case 5: members = RandomCreatures.creatures("centipede", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("ant", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("hornet", "Toxic", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("tortoise", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("tortoise", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("lizard", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("wyrm", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("drake", "Rot", majorBiome, budget)

    return members


# The volcano boss fight has an expanded map with rivers of lava it can dash across
# It ambushes the players when they try to initiate its fight
def volcanoEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Flame", True

    match roll:
        case 1: members = RandomElementals.elementals("hive", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("ooze", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("puffer", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("drake", element, majorBiome, budget)      
        case 5: members = RandomCreatures.creatures("wyrm", "Dream", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("centipede", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("ant", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("lizard", "Dream", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("tortoise", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("muscle", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("tortoise", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("lizard", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("wyrm", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("drake", "Rot", majorBiome, budget)

    return members


def fjordEncounter(roll, budget) -> list:
    members, element, majorBiome = [], "Ice", False

    match roll:
        case 1: members = RandomElementals.elementals("dancer", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("hulk", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", "Dream", majorBiome, budget)
        case 4: members = RandomCreatures.creatures("bear", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("moose", "Dream", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("eagle", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("seal", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("urchin", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("bat", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("worm", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("sheep", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("eagle", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("moose", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("bear", "Rot", majorBiome, budget)

    return members

# Glacier tube battleMaps have the highest obstruction count in the game. 17?
# Glacier boss map changes as the worm carves new tunnels
def glacierEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Ice", True

    match roll:
        case 1: members = RandomElementals.elementals("wraith", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("dancer", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("hulk", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("bear", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("ferret", "Flame", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("mole", "Flame", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("seal", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("urchin", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("worm", "Flame", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("sheep", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("mole", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("ferret", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("bear", "Rot", majorBiome, budget)
    
    return members


def peripheryEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Dream", False

    match roll:
        case 1: members = RandomElementals.elementals("satyr", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("nymph", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("bear", "Ice", majorBiome, budget)
        case 5: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("moose", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("eagle", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("seal", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("urchin", "Ice", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("bat", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("moose", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("ferret", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("hound", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("bear", "Rot", majorBiome, budget)

    return members

def depthsEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Dream", True

    match roll:
        case 1: members = RandomElementals.elementals("ogre", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("satyr", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("nymph", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("ferret", "Flame", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("moose", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("eagle", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("bat", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("moose", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("hound", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("ferret", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("drake", "Rot", majorBiome, budget)

    return members