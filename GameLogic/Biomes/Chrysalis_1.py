from . import RandomCreatures, RandomElementals
import random


def ashShoreEncounters(roll, budget) -> list:
    members, element, majorBiome = [], random.choice(["Flame", "Rot"]), False

    match roll:
        case 1: members = RandomElementals.elementals("rakshasa", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("ooze", "Flame", majorBiome, budget)
        case 3: members = RandomElementals.elementals("balloon", "Flame", majorBiome, budget)
        case 4: members = RandomElementals.elementals("shadow", "Rot", majorBiome, budget)
        case 5: members = RandomElementals.elementals("slime", "Rot", majorBiome, budget)
        case 6: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("komodo", "Toxic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("crab", "Basic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("starfish", "Basic", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("vulture", "Basic", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("leech", "Toxic", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("macaw", element, majorBiome, budget)
        case 15: members = RandomCreatures.creatures("worm", element, majorBiome, budget)        

    return members

def ashWoodEncounters(roll, budget) -> list:
    members, element, majorBiome = [], random.choice(["Flame", "Rot"]), True

    match roll:
        case 1: members = RandomElementals.elementals("rakshasa", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("hive", "Flame", majorBiome, budget)
        case 3: members = RandomElementals.elementals("ooze", "Flame", majorBiome, budget)
        case 4: members = RandomElementals.elementals("balloon", "Flame", majorBiome, budget)
        case 5: members = RandomElementals.elementals("grotesquery", "Rot", majorBiome, budget)
        case 6: members = RandomElementals.elementals("shadow", "Rot", majorBiome, budget)
        case 7: members = RandomElementals.elementals("slime", "Rot", majorBiome, budget)
        case 8: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("tiger", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("komodo", "Toxic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("ape", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("centipede", "Toxic", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("slug", "Toxic", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("macaw", element, majorBiome, budget)
        case 15: members = RandomCreatures.creatures("muscle", "Flame", majorBiome, budget)

    return members


def holyShoreEncounters(roll, budget) -> list:
    members, element, majorBiome = [], random.choice(["Dream", "Holy"]), False

    match roll:
        case 1: members = RandomElementals.elementals("naga", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("sphinx", "Holy", majorBiome, budget)
        case 3: members = RandomElementals.elementals("bull", "Holy", majorBiome, budget)        
        case 4: members = RandomElementals.elementals("satyr", "Dream", majorBiome, budget)
        case 5: members = RandomElementals.elementals("nymph", "Dream", majorBiome, budget)
        case 6: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("komodo", "Toxic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("crab", "Basic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("starfish", "Basic", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("hawk", element, majorBiome, budget)
        case 13: members = RandomCreatures.creatures("seal", element, majorBiome, budget)
        case 14: members = RandomCreatures.creatures("macaw", element, majorBiome, budget)
        case 15: members = RandomCreatures.creatures("urchin", "Toxic", majorBiome, budget)        

    return members

def holyForestEncounters(roll, budget) -> list:
    members, element, majorBiome = [], random.choice(["Dream", "Holy"]), True

    match roll:
        case 1: members = RandomElementals.elementals("naga", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("obelisk", "Holy", majorBiome, budget)
        case 3: members = RandomElementals.elementals("sphinx", "Holy", majorBiome, budget)
        case 4: members = RandomElementals.elementals("bull", "Holy", majorBiome, budget)        
        case 5: members = RandomElementals.elementals("ogre", "Dream", majorBiome, budget)
        case 6: members = RandomElementals.elementals("satyr", "Dream", majorBiome, budget)
        case 7: members = RandomElementals.elementals("nymph", "Dream", majorBiome, budget)
        case 8: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("terror bird", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("tiger", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("slug", "Toxic", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("ape", element, majorBiome, budget)
        case 13: members = RandomCreatures.creatures("macaw", element, majorBiome, budget)
        case 14: members = RandomCreatures.creatures("hornet", "Toxic", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("deer", element, majorBiome, budget)

    return members


def highlandEncounters(roll, budget) -> list:
    members, element, majorBiome = [], random.choice(["Holy", "Ice"]), False

    match roll:
        case 1: members = RandomElementals.elementals("yogi", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("sphinx", "Holy", majorBiome, budget)
        case 3: members = RandomElementals.elementals("bull", "Holy", majorBiome, budget)        
        case 4: members = RandomElementals.elementals("dancer", "Ice", majorBiome, budget)
        case 5: members = RandomElementals.elementals("tripod", "Ice", majorBiome, budget)
        case 6: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("tiger", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("yeti", "Ice", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("ape", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("ferret", "Flame", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("hawk", element, majorBiome, budget)
        case 13: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 14: members = RandomCreatures.creatures("vulture", element, majorBiome, budget)
        case 15: members = RandomCreatures.creatures("urchin", "Ice", majorBiome, budget)        

    return members

def peakEncounters(roll, budget) -> list:
    members, element, majorBiome = [], random.choice(["Holy", "Ice"]), True

    match roll:
        case 1: members = RandomElementals.elementals("yogi", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("obelisk", "Holy", majorBiome, budget)
        case 3: members = RandomElementals.elementals("sphinx", "Holy", majorBiome, budget)
        case 4: members = RandomElementals.elementals("bull", "Holy", majorBiome, budget)
        case 5: members = RandomElementals.elementals("wraith", "Ice", majorBiome, budget)
        case 6: members = RandomElementals.elementals("dancer", "Ice", majorBiome, budget)
        case 7: members = RandomElementals.elementals("tripod", "Ice", majorBiome, budget)
        case 8: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("yeti", "Ice", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("mole", "Flame", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("ferret", "Flame", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 13: members = RandomCreatures.creatures("hawk", element, majorBiome, budget)
        case 14: members = RandomCreatures.creatures("urchin", "Ice", majorBiome, budget)        
        case 15: members = RandomCreatures.creatures("worm", "Flame", majorBiome, budget)        

    return members


def dormantEncounters(roll, budget) -> list:
    members, element, majorBiome = [], random.choice(["Flame", "Ice"]), True

    match roll:
        case 1: members = RandomElementals.elementals("mask", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("hive", "Flame", majorBiome, budget)
        case 3: members = RandomElementals.elementals("ooze", "Flame", majorBiome, budget)
        case 4: members = RandomElementals.elementals("balloon", "Flame", majorBiome, budget)
        case 5: members = RandomElementals.elementals("wraith", "Ice", majorBiome, budget)
        case 6: members = RandomElementals.elementals("dancer", "Ice", majorBiome, budget)
        case 7: members = RandomElementals.elementals("tripod", "Ice", majorBiome, budget)
        case 8: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("tiger", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("yeti", "Ice", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("ferret", "Flame", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 13: members = RandomCreatures.creatures("hawk", element, majorBiome, budget)
        case 14: members = RandomCreatures.creatures("urchin", "Ice", majorBiome, budget)        
        case 15: members = RandomCreatures.creatures("muscle", "Flame", majorBiome, budget)        

    return members