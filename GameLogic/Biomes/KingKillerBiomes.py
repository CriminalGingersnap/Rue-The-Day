from . import RandomCreatures, RandomElementals, RandomHumans


# Soldiers, outlaws, and wildlife vie for space and resources.
def roadEncounters(roll, environment) -> list:
    members, element = [], "Basic"

    match roll:
        case 1 | 2 | 3 | 4 | 5 | 6: members = RandomHumans.soldiers(environment, element)
        case 7: members = RandomHumans.outlaws(environment, element)
        # case 12: members = RandomCreatures.creatures()

    return members