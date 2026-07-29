import random


def setAnimalResistance(element, rank, stats):    
    mainRes, holyRes = "resistant", "resistant"
    if rank in ["Elder", "Master", "Ascendant"]: mainRes, holyRes = "immune", "normal"
    if element not in ["Basic", "Toxic"]: stats["resist"]["Holy"] = holyRes
    
    match element:
        case "Holy":
            stats["resist"]["Holy"] = mainRes
            stats["resist"]["Rot"] = mainRes
        case "Rot":
            stats["resist"]["Rot"] = mainRes
            stats["resist"]["Holy"] = "vulnerable"
        case "Dream":
            stats["resist"]["Pierce"] = mainRes
            stats["resist"]["Crush"] = mainRes
            stats["resist"]["Dream"] = "vulnerable"
            stats["resist"]["Rot"] = "vulnerable"
        case "Flame":
            stats["resist"]["Flame"] = mainRes
            stats["resist"]["Ice"] = "vulnerable"
        case "Ice":
            stats["resist"]["Ice"] = mainRes
            stats["resist"]["Flame"] = "vulnerable"
        case "Toxic":
            stats["resist"]["Toxic"] = mainRes
            stats["resist"]["Rot"] = "resistant"


def incrementDice(dice, rank) -> list:
    if rank in ["Large", "Adult", "Elder"]:
        dice["martial"] += 1
        if rank == "Elder": dice["magic"] += 1

def updateRank(cndt, element, rank):
    if element == "Rot":
        cndt["lifeless"] = True
        match rank:
            case "Juvenile" | "Small" | "Novice" | "Proficient": rank = "Fresh"
            case "Adult" | "Large" | "Adept": rank = "Wizened"
            case "Elder" | "Elite" | "Master": rank = "Ancient"

def downgradeStats(cndt, rank, stats):
    attributes = []

    match rank:
        case "Juvenile" | "Small":
            attributes = ["hp"]
            cndt["massive"] = False
        case "Ancient" | "Elder" | "Wizened":
            attributes = ["avoidance", "speed"]
            if rank == "Ancient": cndt["reposed"] = random.choice([True, True, False])
            elif rank == "Wizened": cndt["reposed"] = random.choice([True, False])
        case "Fresh": attributes = ["hp", "avoidance", "speed"]
        
    for attribute in attributes:
        match stats[attribute]:
            case "low": stats[attribute] = "min"
            case "mid": stats[attribute] = "low"
            case "high": stats[attribute] = "mid"
            case "max": stats[attribute] = "high"


def makeUpdates(element, cndt, rank, stats, dice):
    incrementDice(dice, rank)
    updateRank(cndt, element, rank)
    downgradeStats(cndt, rank, stats)