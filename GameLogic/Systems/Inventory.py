import random, copy

# Martin crafts a blunt weapon after their first encounter with a pierce resistant enemy
# If he equips the blunt weapon, his damage type changes from pierce to blunt.
# Swapping weapons requires him to expend an attack die.

cores = {
    "Corpse": 0,
    "Flame": 0,
    "Fey": 0,
    "Ice": 0,
    "Blessed": 0
} 
pearls = {
    "Blessed": 0,
    "Corpse": 0,
    "Flame": 0,
    "Fey": 0,
    "Ice": 0,
    "Sanguine": 0,
    "Toxin": 0
}


def setInventory(type, rank, element, hp) -> dict:
    match type:
        case "human": return humanInventory(element, rank)
        case "beast": return beastInventory(hp, element, rank, type)
        case "elemental": return elementalInventory(element, rank)
        case "totem": return totemInventory(element, rank)


def humanInventory(element, rank) -> dict:
    global cores, pearls
    
    pillBox = {
        "Capacity": 10,
        "Cores": copy.deepcopy(cores),
        "Pearls": copy.deepcopy(pearls),
        "Shards": {
            "Fey": 0,
            "Flame": 0,
            "Ice": 0
        },
        "Echos": None
    }

    if element != "Corpse":
        budget = ""

        match rank:
            case "Novice": budget = 2
            case "Proficient": budget = 3
            case "Adept": budget = 4
            case "Elite": budget = 5
            case "Master": budget = 6
        
        vita, pearlCount, coreCount = random.randint(0, min(budget, 3)), 0, 0
        budget -= vita
        if budget > 0:
            pearlCount = random.randint(0, budget)
            budget -= pearlCount
        if budget > 1: coreCount = random.randint(1, (budget // 2))

        pillBox["Pearls"]["Sanguine"] = vita
        pillBox["Pearls"][random.choice(["Ice", "Flame", "Toxin"])] = pearlCount
        pillBox["Cores"][random.choice(["Ice", "Flame"])] = coreCount

    return pillBox


def beastInventory(hp, element, rank, type) -> dict:
    drop = {"Cores": {element: 0}, "Pearls": {element: 0}}
    vitaVolume = 0

    if element == "Corpse":
        match hp:
            case "mid": vitaVolume = 1
            case "high": vitaVolume = 2
            case "max": vitaVolume = 3      
    elif type in ["insect", "invertebrate"]:
        match hp:
            case "low": vitaVolume = 1
            case "mid": vitaVolume = 2
            case "high": vitaVolume = 3
            case "max": vitaVolume = 4
    else:
        match hp:
            case "min": vitaVolume = 1
            case "low": vitaVolume = 2
            case "mid": vitaVolume = 3
            case "high": vitaVolume = 4
            case "max": vitaVolume = 5
            
    drop["Pearls"]["Sanguine"] = vitaVolume

    if element != "Basic":
        match rank:
            case "Adult" | "Wizened": drop["Pearls"][element] = 1
            case "Elder" | "Ancient": drop["Pearls"][element] = 2
            case "Boss": drop["Shards"][element] = 1

    return drop


def elementalInventory(element, rank) -> dict:
    drop = {"Cores": {element: 0}, "Pearls": {element: 0}}

    if rank == "Lesser": drop["Cores"][element] = 1
    else: drop["Cores"][element] = 2

    return drop

def totemInventory(element, rank) -> dict:
    drop = {"Cores": {element: 0}, "Pearls": {element: 0}}

    match rank:
        case "Standard": drop["Pearls"][element] = 1
        case "Totem": drop["Pearls"][element] = 2
        case "Monument": drop["Cores"][element] = 1        

    return drop