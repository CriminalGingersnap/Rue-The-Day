def setAnimalResistance(element, rank, stats):
    stats["resist"]["Dream"] = "vulnerable"
    
    level, anti = "resistant", "resistant"
    if rank in ["Elder", "Master"]:
        level = "immune"
        anti = "normal"
    if element != "Basic":
        stats["resist"]["Holy"] = anti
        stats["resist"]["Venom"] = "resistant"
    
    match element:
        case "Blessed":
            stats["resist"]["Holy"] = level
            stats["resist"]["Rot"] = level
        case "Corpse":
            stats["resist"]["Rot"] = level
            stats["resist"]["Dream"] = "immune"
            stats["resist"]["Holy"] = "vulnerable"
        case "Fey":
            stats["resist"]["Dream"] = level
            stats["resist"]["Pierce"] = "resistant"
            stats["resist"]["Crush"] = "resistant"
            stats["resist"]["Rot"] = "vulnerable"
        case "Flame":
            stats["resist"]["Burn"] = level
            stats["resist"]["Freeze"] = "vulnerable"
        case "Ice":
            stats["resist"]["Freeze"] = level
            stats["resist"]["Burn"] = "vulnerable"
        case "Toxin":
            stats["resist"]["Venom"] = level
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