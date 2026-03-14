from . import RandomCreatures, RandomElementals, RandomHumans


def encroachmentEncounter(roll, environment) -> list:
    members, element = [], "Corpse"

    match roll:
        case 1 | 2: members = RandomHumans.soldiers(environment, element)
        case 3 | 4: members = RandomHumans.outlaws(environment, element)
        case 5: members = RandomElementals.elementals("wisp", environment, element, False)
        case 6: members = RandomCreatures.creatures("hound", environment, element)
        case 7: members = RandomCreatures.creatures("ant", environment, "Toxin")
        # case 12: members = RandomCreatures.creatures()

    return members

def locusEncounter(roll, environment) -> list:
    members, element = [], "Corpse"

    match roll:
        # case 1: members = RandomHumans.soldiers(environment, element) Vampire?
        case 2 | 3: members = RandomHumans.soldiers(environment, element)
        case 4 | 5: members = RandomHumans.outlaws(environment, element)
        case 6: members = RandomElementals.elementals("wisp", environment, element, False)
        case 7: members = RandomCreatures.creatures("hound", environment, element)
        case 8: members = RandomCreatures.creatures("ant", environment, "Toxin")
        # case 12: members = RandomCreatures.creatures()

    return members


def scrublandEncounters(roll, environment) -> list:
    members, element = [], "Blessed"

    match roll:
        case 1: members = RandomElementals.elementals("sphinx", environment, element, False)
        case 2: members = RandomElementals.elementals("bull", environment, element, False)
        case 3: members = RandomElementals.elementals("wisp", environment, element, False)
        case 4: members = RandomCreatures.creatures("lion", environment, element)
        case 5: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 6: members = RandomCreatures.creatures("lizard", environment, element)
        case 7: members = RandomCreatures.creatures("sheep", environment, element)
        case 8: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("beetle", environment, element)
        case 10: members = RandomCreatures.creatures("camel", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members

def desertEncounters(roll, environment) -> list:
    members, element = [], "Blessed"

    match roll:
        case 1: members = RandomElementals.elementals("obelisk", environment, element, True)
        case 2: members = RandomElementals.elementals("sphinx", environment, element, True)
        case 3: members = RandomElementals.elementals("bull", environment, element, True)
        case 4: members = RandomElementals.elementals("wisp", environment, element, True)
        case 5: members = RandomCreatures.creatures("drake", environment, element)
        case 6: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("lizard", environment, element)
        case 8: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("beetle", environment, element)
        case 10: members = RandomCreatures.creatures("camel", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members