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

class humanInventory:
    def __init__(self, rank, element) -> None:
        pillBox = {
            "Capacity": 10,
            "Cores": copy.deepcopy(cores),
            "Pearls": copy.deepcopy(pearls),
            "Shards": {
                "Fey": 0,
                "Flame": 0,
                "Ice": 0
            },
            "Echos": {
                None
            }
        }

        setHumanDrop(rank, element, pillBox)            
        self.inventory = pillBox

def setHumanDrop(rank, element, pillBox):
    if element != "Corpse":
        budget = ""

        match rank:
            case "Novice": budget = 2
            case "Proficient": budget = 3
            case "Adept": budget = 4
            case "Elite": budget = 5
            case "Master": budget = 6
        
        vita, pearls, cores = random.randint(0, min(budget, 3)), 0, 0
        budget -= vita
        if budget > 0:
            pearls = random.randint(0, budget)
            budget -= pearls
        if budget > 1: cores = random.randint(1, (budget // 2))

        pillBox["Pearls"]["Sanguine"] = vita
        pillBox["Pearls"][random.choice(["Ice", "Flame", "Toxin"])] = pearls
        pillBox["Cores"][random.choice(["Ice", "Flame"])] = cores


class beastInventory:
    def __init__(self, hp, alignment, rank, type) -> None:
        drop = {"Cores": {alignment: 0}, "Pearls": {alignment: 0}}
        vitaVolume = 0

        if alignment == "Corpse":
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

        if alignment != "Basic":
            match rank:
                case "Adult" | "Wizened": drop["Pearls"][alignment] = 1
                case "Elder" | "Ancient": drop["Pearls"][alignment] = 2
                case "Boss": drop["Shards"][alignment] = 1

        self.inventory = drop


class elementalInventory:
    def __init__(self, alignment, rank) -> None:
        drop = {"Cores": {alignment: 0}, "Pearls": {alignment: 0}}

        if rank == "Lesser": drop["Cores"][alignment] = 1
        else: drop["Cores"][alignment] = 2

        self.inventory = drop

class totemInventory:
    def __init__(self, alignment, rank) -> None:
        drop = {"Cores": {alignment: 0}, "Pearls": {alignment: 0}}

        match rank:
            case "Standard": drop["Pearls"][alignment] = 1
            case "Totem": drop["Pearls"][alignment] = 2
            case "Monument": drop["Cores"][alignment] = 1        

        self.inventory = drop