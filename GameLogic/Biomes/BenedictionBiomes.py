from . import RandomCreatures, RandomElementals, RandomHumans
from Systems import PlayerSelect as Select, Roll


def encroachmentEncounter(roll, budget) -> list:
    members, element, majorBiome = [], "Corpse", False

    match roll:
        case 1 | 2: members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        case 3: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("ant", "Toxin", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("wasp", "Toxin", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("lizard", "Toxin", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("beetle", "Blessed", majorBiome, budget)
        case 11 | 12: members = blessedEncounters(majorBiome, budget)

    return members

def locusEncounter(roll, budget) -> list:
    members, element, majorBiome = [], "Corpse", True

    match roll:
        case 1: members = RandomElementals.elementals("grotesquery", element, majorBiome, budget)
        case 2 | 3: members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        case 4: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 5: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("ant", "Toxin", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("wasp", "Toxin", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("beetle", "Blessed", majorBiome, budget)
        case 11 | 12: members = blessedEncounters(majorBiome, budget)

    return members


def shoreEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    match roll:
        case 1: members = RandomCreatures.creatures("crocodile", element, majorBiome, budget)
        case 2: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("leech", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("crab", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("urchin", "Toxin", majorBiome, budget)
        case 11 | 12: members = undeadEncounters("Shoreline", majorBiome, budget)

    return members

def seaCaveEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Dream", False

    match roll:
        case 1: members = RandomCreatures.creatures("crocodile", element, majorBiome, budget)
        case 2: members = RandomCreatures.creatures("wyrm", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("leech", "Toxin", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("crab", "Basic", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("beetle", "Blessed", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("isopod", "Basic", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("urchin", "Toxin", majorBiome, budget)
        case 11 | 12: members = undeadEncounters("Sea Cave", majorBiome, budget)

    return members


def scrublandEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Blessed", False

    match roll:
        case 1: members = RandomElementals.elementals("sphinx", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("bull", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("hound", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("ant", "Toxin", majorBiome, budget)
        case 7: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("wasp", "Toxin", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("rabbit", element, majorBiome, budget)
        case 12: members = undeadEncounters("Scrubland", majorBiome, budget)

    return members

def desertEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Blessed", True

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("sphinx", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("bull", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
        case 6: members = RandomCreatures.creatures("wyrm", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("ant", "Toxin", majorBiome, budget)
        case 8: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("wasp", "Toxin", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("beetle", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
        case 12: members = undeadEncounters("Desert", majorBiome, budget)

    return members


def undeadEncounters(biome, majorBiome, budget):
    members, element = [], "Corpse"
    Select.waitPrint("Rolling to determine undead encounter number.")
    Select.waitPrint("Group 2 roll:")
    roll = Roll.roll(None, 1, None, None)

    match biome:
        case "Shoreline" | "Sea Caves":
            match roll:
                case 1: members = RandomCreatures.creatures("crocodile", element, majorBiome, budget)
                case 2: members = RandomCreatures.creatures("wyrm", element, majorBiome, budget)
                case 3: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
                case 4: members = RandomCreatures.creatures("octopus", element, majorBiome, budget)
                case 5: members = RandomCreatures.creatures("crab", element, majorBiome, budget)
                case 6: members = RandomCreatures.creatures("leech", element, majorBiome, budget)
        case "Desert" | "Scrubland":
            match roll:
                case 1: members = RandomCreatures.creatures("drake", element, majorBiome, budget)
                case 2: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
                case 2: members = RandomCreatures.creatures("wyrm", element, majorBiome, budget)
                case 3: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
                case 4: members = RandomCreatures.creatures("camel", element, majorBiome, budget)
                case 5: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)

    return members


def blessedEncounters(majorBiome, budget):
    members, element = [], "Blessed"
    Select.waitPrint("Rolling to determine blessed encounter number.")
    Select.waitPrint("Group 2 roll:")
    roll = Roll.roll(None, 1, None, None)

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", element, majorBiome, budget)
        case 2: members = RandomElementals.elementals("sphinx", element, majorBiome, budget)
        case 3: members = RandomElementals.elementals("bull", element, majorBiome, budget)
        case 4: members = RandomElementals.elementals("wisp", element, majorBiome, budget)
        case 5: members = RandomElementals.elementals("hive", element, majorBiome, budget)
        case 6: members = RandomElementals.elementals("puffer", element, majorBiome, budget)

    return members