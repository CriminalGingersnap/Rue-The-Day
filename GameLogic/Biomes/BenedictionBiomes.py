from . import RandomCreatures, RandomElementals, RandomHumans
from Systems import PlayerSelect as Select, Roll


def encroachmentEncounter(roll, environment) -> list:
    members, element = [], "Corpse"

    match roll:
        case 1 | 2: members = RandomHumans.soldiers(environment, element)
        case 3: members = RandomHumans.outlaws(environment, element)
        case 4: members = RandomElementals.elementals("wisp", environment, element, False)
        case 5: members = RandomCreatures.creatures("lion", environment, element)
        case 6: members = RandomCreatures.creatures("hound", environment, element)
        case 7: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 8: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("lizard", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("beetle", environment, "Blessed")
        case 11 | 12: members = blessedEncounters(environment)

    return members

def locusEncounter(roll, environment) -> list:
    members, element = [], "Corpse"

    match roll:
        case 1: members = RandomElementals.elementals("grotesquery", environment, element, True)
        case 2 | 3: members = RandomHumans.soldiers(environment, element)
        case 4: members = RandomHumans.outlaws(environment, element)
        case 5: members = RandomElementals.elementals("wisp", environment, element, True)
        case 6: members = RandomCreatures.creatures("lion", environment, element)
        case 7: members = RandomCreatures.creatures("hound", environment, element)
        case 8: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("beetle", environment, "Blessed")
        case 11 | 12: members = blessedEncounters(environment)

    return members


def shorelineEncounters(roll, environment) -> list:
    members, element = [], "Basic"

    match roll:
        case 1: members = RandomCreatures.creatures("crocodile", environment, element)
        case 2: members = RandomCreatures.creatures("lion", environment, element)
        case 3: members = RandomCreatures.creatures("turtle", environment, element)
        case 4: members = RandomCreatures.creatures("octopus", environment, element)
        case 6: members = RandomCreatures.creatures("leech", environment, element)
        case 7: members = RandomCreatures.creatures("crab", environment, element)
        case 8: members = RandomCreatures.creatures("lizard", environment, element)
        case 9: members = RandomCreatures.creatures("isopod", environment, element)
        case 10: members = RandomCreatures.creatures("urchin", environment, "Toxin")
        case 11 | 12: members = undeadEncounters("Shoreline", environment)

    return members

def seaCaveEncounters(roll, environment) -> list:
    members, element = [], "Dream"

    match roll:
        case 1: members = RandomCreatures.creatures("crocodile", environment, element)
        case 2: members = RandomCreatures.creatures("wyrm", environment, element)
        case 3: members = RandomCreatures.creatures("turtle", environment, element)
        case 4: members = RandomCreatures.creatures("octopus", environment, element)
        case 5: members = RandomCreatures.creatures("leech", environment, 'Toxin')
        case 6: members = RandomCreatures.creatures("crab", environment, "Basic")
        case 7: members = RandomCreatures.creatures("lizard", environment, element)
        case 8: members = RandomCreatures.creatures("beetle", environment, "Blessed")
        case 9: members = RandomCreatures.creatures("isopod", environment, "Basic")
        case 10: members = RandomCreatures.creatures("urchin", environment, "Toxin")
        case 11 | 12: members = undeadEncounters("Sea Cave", environment)

    return members


def scrublandEncounters(roll, environment) -> list:
    members, element = [], "Blessed"

    match roll:
        case 1: members = RandomElementals.elementals("sphinx", environment, element, False)
        case 2: members = RandomElementals.elementals("bull", environment, element, False)
        case 3: members = RandomElementals.elementals("wisp", environment, element, False)
        case 4: members = RandomCreatures.creatures("lion", environment, element)
        case 5: members = RandomCreatures.creatures("hound", environment, element)
        case 6: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("sheep", environment, element)
        case 8: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("beetle", environment, element)
        case 10: members = RandomCreatures.creatures("camel", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        case 12: members = undeadEncounters("Scrubland", environment)

    return members

def desertEncounters(roll, environment) -> list:
    members, element = [], "Blessed"

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", environment, element, True)
        case 2: members = RandomElementals.elementals("sphinx", environment, element, True)
        case 3: members = RandomElementals.elementals("bull", environment, element, True)
        case 4: members = RandomElementals.elementals("wisp", environment, element, True)
        case 5: members = RandomCreatures.creatures("drake", environment, element)
        case 6: members = RandomCreatures.creatures("wyrm", environment, element)
        case 7: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 8: members = RandomCreatures.creatures("lizard", environment, element)
        case 9: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 10: members = RandomCreatures.creatures("beetle", environment, element)
        case 11: members = RandomCreatures.creatures("camel", environment, element)
        case 12: members = undeadEncounters("Desert", environment)

    return members


def undeadEncounters(biome, environment):
    members, element = [], "Corpse"
    Select.waitPrint("Rolling to determine undead encounter number.")
    Select.waitPrint("Group 2 roll:")
    roll = Roll.roll(None, 1, None, None)

    match biome:
        case "Shoreline" | "Sea Caves":
            match roll:
                case 1: members = RandomCreatures.creatures("crocodile", environment, element)
                case 2: members = RandomCreatures.creatures("wyrm", environment, element)
                case 3: members = RandomCreatures.creatures("turtle", environment, element)
                case 4: members = RandomCreatures.creatures("octopus", environment, element)
                case 5: members = RandomCreatures.creatures("crab", environment, element)
                case 6: members = RandomCreatures.creatures("leech", environment, element)
        case "Desert" | "Scrubland":
            match roll:
                case 1: members = RandomCreatures.creatures("drake", environment, element)
                case 2: members = RandomCreatures.creatures("lion", environment, element)
                case 2: members = RandomCreatures.creatures("wyrm", environment, element)
                case 3: members = RandomCreatures.creatures("lizard", environment, element)
                case 4: members = RandomCreatures.creatures("camel", environment, element)
                case 5: members = RandomCreatures.creatures("sheep", environment, element)

    return members


def blessedEncounters(environment):
    members, element = [], "Blessed"
    Select.waitPrint("Rolling to determine blessed encounter number.")
    Select.waitPrint("Group 2 roll:")
    roll = Roll.roll(None, 1, None, None)

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", environment, element, True)
        case 2: members = RandomElementals.elementals("sphinx", environment, element, True)
        case 3: members = RandomElementals.elementals("bull", environment, element, True)
        case 4: members = RandomElementals.elementals("wisp", environment, element, True)
        case 2: members = RandomElementals.elementals("sphinx", environment, element, False)
        case 3: members = RandomElementals.elementals("bull", environment, element, False)

    return members