import random, copy
from . import Equipment


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
    "Toxic": 0
}


def setInventory(type, rank, element, hp) -> dict:
    match type:
        case "human": return humanInventory(element, rank)
        case "beast": return beastInventory(hp, element, rank, type)
        case "elemental": return elementalInventory(element, rank)
        case "totem": return totemInventory(element, rank)


def humanInventory(element, rank) -> dict:
    global cores, pearls
    
    inventory = {
        "Capacity": 10,
        "cores": copy.deepcopy(cores),
        "pearls": copy.deepcopy(pearls),
        "shards": {
            "Fey": 0,
            "Flame": 0,
            "Ice": 0
        },
        "spares": {
            "shield": copy.deepcopy(Equipment.nullKit),
            "weapon": copy.deepcopy(Equipment.nullWeapon)
        },
        "echos": None
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

        inventory["pearls"]["Sanguine"] = vita
        inventory["pearls"][random.choice(["Ice", "Flame", "Toxic"])] = pearlCount
        inventory["cores"][random.choice(["Ice", "Flame"])] = coreCount

    return inventory


def beastInventory(hp, element, rank, type) -> dict:
    drop = {"cores": {element: 0}, "pearls": {element: 0}}
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
            
    drop["pearls"]["Sanguine"] = vitaVolume

    if element != "Basic":
        match rank:
            case "Adult" | "Wizened": drop["pearls"][element] = 1
            case "Elder" | "Ancient": drop["pearls"][element] = 2
            case "Boss": drop["shards"][element] = 1

    return drop


def elementalInventory(element, rank) -> dict:
    drop = {"cores": {element: 0}, "pearls": {element: 0}}

    if rank == "Lesser": drop["cores"][element] = 1
    else: drop["cores"][element] = 2

    return drop

def totemInventory(element, rank) -> dict:
    drop = {"cores": {element: 0}, "pearls": {element: 0}}

    match rank:
        case "Standard": drop["pearls"][element] = 1
        case "Totem": drop["pearls"][element] = 2
        case "Monument": drop["cores"][element] = 1        

    return drop