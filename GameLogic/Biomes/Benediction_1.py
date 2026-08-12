from . import RandomCreatures, RandomElementals, RandomHumans


def duneEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    match roll:
        case 1: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 2: members = RandomCreatures.creatures("anemone", "Toxic", majorBiome, budget)
        case 3: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("crab", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("leech", "Toxic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("seal", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("hawk", "Ice", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("urchin", "Toxic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("worm", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("seal", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("octopus", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("turtle", "Rot", majorBiome, budget)
        case 15: members = RandomHumans.warriors("Outlaw", "Rot", majorBiome, budget)

    return members

def seaCaveEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Dream", False

    match roll:
        case 1: members = RandomElementals.elementals("ogre", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("nymph", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("crab", "Basic", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("centipede", "Toxic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("isopod", "Basic", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("leech", "Toxic", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("urchin", "Toxic", majorBiome, budget)        
        case 11: members = RandomCreatures.creatures("muscle", "Basic", majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("seal", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("octopus", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("turtle", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("wisp", "Rot", majorBiome, budget)

    return members


def scrublandEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Holy", False

    match roll:
        case 1: members = RandomElementals.elementals("sphinx", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("bull", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("centipede", "Toxic", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("ostrich", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("vulture", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("ant", "Toxic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("bat", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("vulture", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("camel", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("ostrich", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("lion", "Rot", majorBiome, budget)

    return members

def desertEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Holy", True

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("sphinx", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("bull", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("spider", "Toxic", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("ostrich", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("vulture", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("ant", "Toxic", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("vulture", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("camel", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("ostrich", "Rot", majorBiome, budget)
        case 15: members = RandomCreatures.creatures("drake", "Rot", majorBiome, budget)

    return members


def encroachmentEncounter(roll, budget) -> list:
    members, element, majorBiome = [], "Rot", False

    match roll:
        case 1: members = RandomElementals.elementals("shadow", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("slime", element, majorBiome, budget)
        case 3: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("hound", "Basic", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("centipede", "Toxic", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("ant", "Toxic", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("lizard", "Toxic", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("vulture", "Basic", majorBiome, budget)
        case 11: members = RandomCreatures.creatures("crow", "Basic", majorBiome, budget)
        case 12: members = RandomCreatures.creatures("beetle", "Holy", majorBiome, budget)
        case 13: members = RandomElementals.elementals("wisp", "Holy", majorBiome, budget)
        case 14: members = RandomElementals.elementals("bull", "Holy", majorBiome, budget)
        case 15: members = RandomElementals.elementals("sphinx", "Holy", majorBiome, budget)

    return members

def locusEncounter(roll, budget) -> list:
    members, element, majorBiome = [], "Rot", True

    match roll:
        case 1: members = RandomElementals.elementals("grotesquery", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("shadow", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("slime", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        case 6: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("spider", "Toxic", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("centipede", "Toxic", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("beetle", "Holy", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("vulture", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("crow", element, majorBiome, budget)
        case 12: members = RandomCreatures.creatures("drake", "Holy", majorBiome, budget)
        case 13: members = RandomElementals.elementals("wisp", "Holy", majorBiome, budget)
        case 14: members = RandomElementals.elementals("bull", "Holy", majorBiome, budget)
        case 15: members = RandomElementals.elementals("sphinx", "Holy", majorBiome, budget)

    return members