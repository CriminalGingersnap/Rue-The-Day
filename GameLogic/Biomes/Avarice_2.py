from . import RandomCreatures, RandomHumans


def strongholdEncounters(roll, rollNumber, type, budget) -> list:
    members, element = [], "Basic"

    if rollNumber == 0:
        match type:
            case "Range": members = RandomHumans.warriors("Outlaw", element, False, budget)
            case "Road": members = RandomHumans.warriors("Soldier", element, False, budget)
            case "Camp": members = RandomHumans.warriors("Outlaw", element, True, budget)
            case "Fort":members = RandomHumans.warriors("Soldier", element, True, budget)
    else: members = forestEncounters(roll, budget)
            
    return members


def forestEncounters(roll, budget) -> list:
    members, element, majorBiome = [], "Basic", False

    match roll:
        case 1: members = RandomHumans.warriors("Soldier", element, majorBiome, budget)
        case 2: members = RandomHumans.warriors("Outlaw", element, majorBiome, budget)
        case 3: members = RandomCreatures.creatures("terror bird", element, majorBiome, budget)
        case 4: members = RandomCreatures.creatures("wyrm", "Toxic", majorBiome, budget)
        case 5: members = RandomCreatures.creatures("hornet", "Toxic", majorBiome, budget)
        case 6: members = RandomCreatures.creatures("sheep", element, majorBiome, budget)
        case 7: members = RandomCreatures.creatures("isopod", element, majorBiome, budget)
        case 8: members = RandomCreatures.creatures("crow", element, majorBiome, budget)
        case 9: members = RandomCreatures.creatures("lizard", "Toxic", majorBiome, budget)
        case 10: members = RandomCreatures.creatures("deer", element, majorBiome, budget)
        case 11: members = RandomCreatures.creatures("bat", element, majorBiome, budget)        
        case 12: members = RandomCreatures.creatures("sheep", "Rot", majorBiome, budget)
        case 13: members = RandomCreatures.creatures("wyrm", "Rot", majorBiome, budget)
        case 14: members = RandomCreatures.creatures("terror bird", "Rot", majorBiome, budget)
        case 15: members = RandomHumans.warriors("Outlaw", "Rot", majorBiome, budget)

    return members