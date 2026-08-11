import random, copy
from . import Equipment
from Biomes import RandomCreatures


cores = {
    "Dream": 0,
    "Flame": 0,
    "Holy": 0,
    "Ice": 0,
    "Rot": 0
}
pearls = {
    "Bleed": 0,
    "Dream": 0,
    "Flame": 0,
    "Holy": 0,
    "Ice": 0,
    "Rot": 0,
}


def setInventory(element, hp, job, rank, type) -> dict:
    match type:
        case "human": return humanInventory(element, rank)
        case "beast" | "bird" | "invertebrate" | "insect" | "reptile": return beastInventory(hp, element, rank, type)
        case "elemental": return elementalInventory(element, rank)
        case "totem": return totemInventory(element, job)


def humanInventory(element, rank) -> dict:
    global cores, pearls
    
    inventory = {
        "Capacity": 10,
        "cores": copy.deepcopy(cores),
        "pearls": copy.deepcopy(pearls),
        "shards": {
            "Dream": 0,
            "Flame": 0,
            "Ice": 0
        },
        "spares": {
            "shield": copy.deepcopy(Equipment.nullKit),
            "weapon": copy.deepcopy(Equipment.nullWeapon)
        },
        "echo": "None",
        "standard": "None"
    }

    if element != "Rot":
        budget, pearlCount, coreCount, echo = "", 0, 0, "None"

        match rank:
            case "Novice": budget = 0
            case "Proficient": budget = 1
            case "Adept": budget = 2
            case "Elite": budget = 4
            case "Master": budget = 8
        
        vita = random.randint(1, 2)
        budget -= vita
        if budget > 0:
            pearlCount = random.randint(0, budget)
            budget -= pearlCount
        if budget > 1:
            coreCount = random.randint(1, (budget // 2))
            budget -= coreCount * 2
        if budget > 1:
            echo = RandomCreatures.creatures("random", "Basic", "False", budget)[0]
            setLifeless(echo)

        inventory["pearls"]["Bleed"] = vita
        inventory["pearls"][random.choice(["Dream", "Flame", "Ice",  "Rot"])] = pearlCount
        inventory["cores"][random.choice(["Dream", "Flame", "Ice",  "Rot"])] = coreCount
        inventory["echo"] = echo

    return inventory


def setLifeless(echo):
    echo.atrb["cur_hp"] = echo.atrb["base_hp"] = echo.atrb["half_hp"]
    echo.atrb["nat_res"].update({"Bleed": "immune", "Dream": "immune", "Holy": "normal", "Toxic": "immune"})
    echo.atrb["cur_res"] = copy.deepcopy(echo.atrb["nat_res"])

    echo.cndt.update({"lifeless": True, "social": False, "skittish": False})
    echo.props["type"] = "echo"


def beastInventory(hp, element, rank, type) -> dict:
    drop = {"cores": {element: 0}, "pearls": {element: 0}, "shards": {element: 0}}
    vitaVolume = 0

    if element == "Rot":
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
        drop["pearls"]["Dream"] = random.choice([1, 0, 0])
        match hp:
            case "min": vitaVolume = 1
            case "low": vitaVolume = 2
            case "mid": vitaVolume = 3
            case "high": vitaVolume = 4
            case "max": vitaVolume = 5
            
    drop["pearls"]["Bleed"] = vitaVolume

    if element != "Basic":
        match rank:
            case "Adult" | "Wizened": drop["pearls"][element] += 1
            case "Elder" | "Ancient": drop["pearls"][element] += 2
            case "Ascendant": drop["shards"][element] = 1

    return drop


def elementalInventory(element, rank) -> dict:
    drop = {"cores": {element: 0}, "pearls": {element: 0}}

    match rank:
        case "Lesser": drop["cores"][element] = 1        
        case "Greater": drop["cores"][element] = 2       

    return drop


def totemInventory(element, job) -> dict:
    drop = {"cores": {element: 0}, "pearls": {element: 0}}

    match job:
        case "Standard": drop["pearls"][element] = 1
        case "Door": drop["pearls"][element] = 2
        case "Gate": drop["cores"][element] = 1
        case "Monument": drop["cores"][element] = 2

    return drop