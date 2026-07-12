from . import RandomCreatures, RandomElementals, RandomHumans
from Systems import PlayerSelect as Select, Roll
import random


# Soldiers, outlaws, and wildlife vie for space and resources.
def outlierEncounters(roll, rollNumber, type, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    if rollNumber == 0:
        match type:
            case "Road": members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
            case "Camp": members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
    else: members = unsettledEncounters(roll, budget)
            
    return members

def strongholdEncounters(roll, rollNumber, budget) -> list:
    members, element, majorBiome = [], "Basic", True

    if rollNumber == 0:
        members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        members += RandomHumans.warriors("Soldier", element, majorBiome, budget)
    else: members = unsettledEncounters(roll, budget)
            
    return members


def marshEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    match roll:
        case 1: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 2: members = RandomCreatures.creatures("crocodile", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("wyrm", "Toxic", majorBiome, budget)
        case 4: members = RandomCreatures.creatures("turtle", element, majorBiome, budget)
        case 5: members = RandomCreatures.creatures("leech", "Toxic", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("crab", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("wasp", "Toxic", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("tortoise", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("worm", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("turtle", "Corpse", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("wyrm", "Corpse", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("crocodile", "Corpse", majorBiome, budget)
        case 15: members = members = RandomHumans.warriors("Outlaw", "Corpse", majorBiome, budget)

    return members


def unsettledEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    match roll:
        case 1: members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        case 2: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("lion", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("wyrm", "Toxic", majorBiome, budget)
        case 5: members = RandomCreatures.creatures("ant", "Toxic", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("lizard", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("wasp", "Toxic", majorBiome, budget)
        case 9: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 10: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("rabbit", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("lizard", "Corpse", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("wyrm", "Corpse", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("lion", "Corpse", majorBiome, budget)
        case 15: members = members = RandomHumans.warriors("Outlaw", "Corpse", majorBiome, budget)

    return members