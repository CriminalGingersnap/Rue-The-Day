def setAnimalResistance(element, rank, stats):    
    mainRes, holyRes = "resistant", "resistant"
    if rank in ["Elder", "Master"]: mainRes, holyRes = "immune", "normal"
    if element != "Basic":
        stats["resist"]["Holy"] = holyRes
        stats["resist"]["Venom"] = "resistant"
    
    match element:
        case "Blessed":
            stats["resist"]["Holy"] = mainRes
            stats["resist"]["Rot"] = mainRes
        case "Corpse":
            stats["resist"]["Rot"] = mainRes
            stats["resist"]["Holy"] = "vulnerable"
        case "Fey":
            stats["resist"]["Dream"] = mainRes
            stats["resist"]["Pierce"] = "resistant"
            stats["resist"]["Crush"] = "resistant"
            stats["resist"]["Rot"] = "vulnerable"
        case "Flame":
            stats["resist"]["Burn"] = mainRes
            stats["resist"]["Freeze"] = "vulnerable"
        case "Ice":
            stats["resist"]["Freeze"] = mainRes
            stats["resist"]["Burn"] = "vulnerable"
        case "Toxin":
            stats["resist"]["Venom"] = mainRes
            stats["resist"]["Rot"] = "resistant"

def incrementDice(dice, rank) -> list:
    if rank in ["Large", "Adult", "Elder"]:
        dice["martial"] += 1
        if rank == "Elder": dice["magic"] += 1

def updateRank(cndt, element, rank):
    if element == "Corpse":
        cndt["lifeless"] = True
        match rank:
            case "Juvenile" | "Small" | "Novice": rank = "Fresh"
            case "Adult" | "Large" | "Adept": rank = "Wizened"
            case "Elder" | "Elite" | "Master": rank = "Ancient"

def downgradeStats(cndt, rank, stats):
    attributes = []

    match rank:
        case "Juvenile" | "Small":
            attributes = ["hp"]
            cndt["massive"] = False
        case "Elder": attributes = ["avoidance", "speed"]
        case "Fresh": attributes = ["hp", "avoidance", "speed"]
        case "Wizened": attributes = ["avoidance", "speed"]
        case "Ancient": attributes = ["speed"]
        
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