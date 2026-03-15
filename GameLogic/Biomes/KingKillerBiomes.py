from . import RandomCreatures, RandomElementals, RandomHumans
from Systems import PlayerSelect as Select, Roll


# Soldiers, outlaws, and wildlife vie for space and resources.
def roadEncounters(roll, environment, rollNumber) -> list:
    members, element = [], "Basic"

    if rollNumber == 0:
        members = RandomHumans.soldiers(environment, element)
    else:
        match roll:
            case 1 | 2: members = RandomHumans.outlaws(environment, element)
            case 3: members = RandomCreatures.creatures("lion", environment, element)
            case 4: members = RandomCreatures.creatures("hound", environment, element)
            case 5: members = RandomCreatures.creatures("ant", environment, "Toxin")
            case 6: members = undeadEncounters("Road", environment)
            
    return members


def unsettledEncounters(roll, environment) -> list:
    members, element = [], "Basic"

    match roll:
        case 1: members = RandomHumans.soldiers(environment, element)
        case 2: members = RandomHumans.outlaws(environment, element)
        case 3: members = RandomCreatures.creatures("lion", environment, element)
        case 4: members = RandomCreatures.creatures("wyrm", environment, element)
        case 5: members = RandomCreatures.creatures("hound", environment, element)
        case 6: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 7: members = RandomCreatures.creatures("lizard", environment, element)
        case 8: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 9: members = RandomCreatures.creatures("sheep", environment, element)
        case 10: members = RandomCreatures.creatures("deer", environment, element)
        case 11: members = RandomCreatures.creatures("rabbit", environment, element)
        case 12: members = undeadEncounters("Unsettled", environment)

    return members


def undeadEncounters(biome, environment):
    members, element = [], "Corpse"
    Select.waitPrint("Rolling to determine undead encounter number.")
    Select.waitPrint("Group 2 roll:")
    roll = Roll.roll(None, 1, None, None)

    match biome:
        case "Unsettled" | "Road":
            match roll:
                case 1: members = members = RandomHumans.outlaws(environment, element)
                case 2: members = RandomCreatures.creatures("lion", environment, element)
                case 3: members = RandomCreatures.creatures("wyrm", environment, element)
                case 4: members = RandomCreatures.creatures("lizard", environment, element)
                case 5: members = RandomCreatures.creatures("sheep", environment, element)
                case 6: members = RandomCreatures.creatures("deer", environment, element)

    return members