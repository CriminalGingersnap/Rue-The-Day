from . import RandomCreatures, RandomElementals, RandomHumans


# Soldiers, outlaws, and wildlife vie for space and resources.
def kingdomEncounters(roll, environment) -> list:
    members = []

    match roll:
        case 1: members = RandomHumans.soldiers("Elite", environment)
        case 2: members = RandomHumans.soldiers("Elite", environment)
        case 3: members = RandomHumans.soldiers("Adept", environment)
        case 4: members = RandomHumans.soldiers("Adept", environment)
        case 5: members = RandomHumans.soldiers("Proficient", environment)
        case 6: members = RandomHumans.soldiers("Proficient", environment)
        case 7: members = RandomCreatures.creatures("ant", environment, "Toxin")
        case 8: members = RandomCreatures.creatures("hound", environment, "Basic")
        case 9: members = RandomCreatures.creatures("lizard", environment, "Basic")
        case 10: members = RandomCreatures.creatures("wasp", environment, "Toxin")
        case 11: members = RandomCreatures.creatures("wyrm", environment, "Toxin")
        # case 12: members = RandomCreatures.creatures()

    return members