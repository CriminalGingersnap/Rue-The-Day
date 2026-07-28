from . import RandomCreatures, RandomElementals, RandomHumans


def nestEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", True

    match roll:
        case 1: members = RandomCreatures.creatures("hydra", "Toxic", majorBiome, budget)
        case 2: members = RandomCreatures.creatures("crocodile", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("wyrm", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("crab", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("seal", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("hawk", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("urchin", "Toxic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("worm", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("turtle", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("wyrm", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("crocodile", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("hydra", "Rot", majorBiome, budget)

    return members


def lowlandEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Flame", False

    match roll:
        case 1: members = RandomElementals.elementals("ooze", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("puffer", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("centipede", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("ant", "Toxic", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("hornet", "Toxic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("tortoise", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("tortoise", "Rot", majorBiome, budget)        
        case 13: members = RandomCreatures.creatures("camel", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("lion", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("drake", "Rot", majorBiome, budget)

    return members


def highlandEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Ice", False

    match roll:
        case 1: members = RandomElementals.elementals("dancer", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("hulk", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("ferret", "Flame", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("hawk", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("bat", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("urchin", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("sheep", "Rot", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("ferret", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("camel", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("lion", "Rot", majorBiome, budget)

    return members