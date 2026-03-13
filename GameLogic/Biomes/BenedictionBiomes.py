from . import RandomCreatures, RandomElementals, RandomHumans


# the low pass is a valley between two mountains. It crosses from the dry starting prairie into a lush bay.
def scrublandEncounters(roll, environment) -> list:
    members, element = [], "Blessed"

    match roll:
        case 1: members = RandomElementals.elementals("sphinx", environment, element, False)
        case 2: members = RandomElementals.elementals("hulk", environment, element, False)
        case 3: members = RandomElementals.elementals("wisp", environment, element, False)
        case 4: members = RandomCreatures.creatures("lion", environment, "Toxin")
        case 5: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 6: members = RandomCreatures.creatures("hound", environment, element)
        case 7: members = RandomCreatures.creatures("lizard", environment, element)
        case 8: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("beetle", environment, element)
        case 10: members = RandomCreatures.creatures("sheep", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members