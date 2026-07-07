from . import RandomCreatures, RandomElementals, RandomHumans
from Systems import PlayerSelect as Select, Roll


def shoreEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    match roll:
        case 1: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 2: members = RandomCreatures.creatures("crocodile", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("worm", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("urchin", "Toxin", majorBiome, budget)
        case 5: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("beetle", "Blessed", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("crab", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("leech", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("octopus", "Corpse", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("turtle", "Corpse", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("crocodile", "Corpse", majorBiome, budget)
        case 15: members = RandomHumans.warriors("Outlaw", "Corpse", majorBiome, budget)

    return members

def seaCaveEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Dream", False

    match roll:
        case 1: members = RandomElementals.elementals("ogre", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("nymph", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("urchin", "Toxin", majorBiome, budget)
        case 5: members = RandomCreatures.creatures("isopod", "Basic", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("beetle", "Blessed", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("crab", "Basic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("leech", "Toxin", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("crocodile", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("octopus", "Corpse", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("turtle", "Corpse", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("crocodile", "Corpse", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("wisp", "Corpse", majorBiome, budget)

    return members


def scrublandEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Blessed", False

    match roll:
        case 1: members = RandomElementals.elementals("sphinx", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("bull", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("rabbit", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("wasp", "Toxin", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("ant", "Toxin", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("camel", "Corpse", majorBiome, budget)        
        case 13: members = RandomCreatures.creatures("sheep", "Corpse", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("hound", "Corpse", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("lion", "Corpse", majorBiome, budget)

    return members

def desertEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Blessed", True

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("sphinx", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("bull", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("wasp", "Toxin", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("ant", "Toxin", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("wyrm", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("camel", "Corpse", majorBiome, budget)        
        case 13: members = RandomCreatures.creatures("lizard", "Corpse", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("wyrm", "Corpse", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("drake", "Corpse", majorBiome, budget)

    return members


def encroachmentEncounter(roll, budget) -> list:
    members, element, majorBiome = [], "Corpse", False

    match roll:
        case 1: members = RandomElementals.elementals("shadow", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("slime", element, majorBiome, budget)
        case 3: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("isopod", "Toxin", majorBiome, budget)
        case 5: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("beetle", "Toxin", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("wasp", "Toxin", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("ant", "Toxin", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 12: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 13: members = RandomElementals.elementals("wisp", "Blessed", majorBiome, budget)
        case 14: members = RandomElementals.elementals("bull", "Blessed", majorBiome, budget)
        case 15: members = RandomElementals.elementals("sphinx", "Blessed", majorBiome, budget)

    return members

def locusEncounter(roll, budget) -> list:
    members, element, majorBiome = [], "Corpse", True

    match roll:
        case 1: members = RandomElementals.elementals("grotesquery", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("shadow", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("slime", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("camel", element, majorBiome, budget) 
        case 6: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("wyrm", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
        case 10: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 11: members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("drake", "Blessed", majorBiome, budget)
        case 13: members = RandomElementals.elementals("wisp", "Blessed", majorBiome, budget)
        case 14: members = RandomElementals.elementals("bull", "Blessed", majorBiome, budget)
        case 15: members = RandomElementals.elementals("sphinx", "Blessed", majorBiome, budget)

    return members