from . import Characters, Animals
import Systems.Inventory as Inventory
import random


def setCommon(job, rank, element) -> list:
    type, dice = "human", {"martial": 0, "magic": 0}

    traits = Characters.setTraits()
    cndt = traits[0]
    stats = {"avoidance": "mid", "hp": "mid", "resist": traits[1], "speed": "mid"}
    Animals.setAnimalResistance(element, rank, stats)
    cndt["sapient"] = True

    if rank == "Random": rank = random.choice(["Proficient", "Adept", "Elite"])

    match rank:
        case "Adept": stats["resist"]["Dream"] = "normal"
        case "Elite": stats["resist"]["Dream"] = "resistant"
        case "Master": stats["resist"]["Dream"] = "immune"

    if job == "Knight": stats["speed"] = "high"

    if job in ["Archer", "Knight"]:
        match rank:
            case "Novice": dice["martial"] = 1
            case "Proficient" | "Adept": dice["martial"] = 2
            case "Elite": dice["martial"] = 3
            case "Master": dice["martial"] = 4
    elif job == "Mage":
        match rank:
            case "Novice": dice["magic"] = 1
            case "Proficient" | "Adept": dice["magic"] = 2
            case "Elite": dice["magic"] = 3
            case "Master": dice["magic"] = 4
    elif job in ["Dragonslayer", "Paladin"]:
        match rank:
            case "Novice": dice["martial"] = 1
            case "Proficient" | "Adept": dice["martial"], dice["magic"] = 1, 1
            case "Elite": dice["martial"], dice["magic"] = 2, 1
            case "Master": 
                if job == "Dragonslayer": dice["martial"], dice["magic"] = 3, 1
                else: dice["martial"], dice["magic"] = 2, 2

    return [stats, cndt, dice, type]

def correctSpecialties(abl, secondSpecialty):
    if secondSpecialty == abl["specialty"]:
        abl["mastery"] = [secondSpecialty]
        abl["specialty"].remove(secondSpecialty[0])
    else: abl["specialty"] += [secondSpecialty]  


class archer:
    def __init__(self, rank) -> None:
        job, element = "Archer", "Basic"
        common = setCommon(job, rank, element)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"attacks": ["Broadhead"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bodkin"]
            
            if rank in ["Adept", "Elite", "Master"]:
                abl["areas"] += ["Mark"]
                abl["specialty"] = [random.choice(["Bodkin", "Broadhead"])]
                
                if rank in ["Elite", "Master"]:
                    abl["boons"] += ["Quick Inventory"]
                
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bodkin", "Broadhead"])]
                        correctSpecialties(abl, secondSpecialty)

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        inv = Inventory.humanInventory(rank, element, job).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, inv, rank)

class knight:
    def __init__(self, rank) -> None:
        job, element = "Knight", "Basic"
        common = setCommon(job, rank, element)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Stab"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Guard"]

            if rank in ["Adept", "Elite", "Master"]:
                abl["reactions"] += ["Riposte"]
                abl["specialty"] = [random.choice(["Bash", "Guard", "Stab"])]
                
                if rank in ["Elite", "Master"]:
                    abl["areas"] += ["Ready"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bash", "Guard", "Stab"])]
                        correctSpecialties(abl, secondSpecialty)
        
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        inv = Inventory.humanInventory(rank, element, job).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, inv, rank)

class mage:
    def __init__(self, rank, element) -> None:
        job = "Mage"
        common = setCommon(job, rank, element)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"boons": ["Wreath"]})
                
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            if element == "Dream": abl["boons"] += ["Focus"]
            else: abl["attacks"] += ["Bring"]
            
            if rank in ["Adept", "Elite", "Master"]:
                if rank == "Dream":
                    abl["hindrances"] += ["Disorient"]
                    abl["specialty"] = [random.choice(["Disorient", "Focus", "Wreath"])]
                else:
                    abl["areas"] += ["Hex"]
                    abl["specialty"] = [random.choice(["Bring", "Wreath"])]
                
                if rank in ["Elite", "Master"]:
                    if rank == "Dream": abl["hindrance"] += ["Misdirect"]
                    else: abl["reactions"] += ["Flare"]

                    if rank == "Master":
                        secondSpecialty = [random.choice("Bring", "Wreath")]
                        if rank == "Dream": secondSpecialty = [random.choice("Disorient", "Focus", "Misdirect", "Wreath")]
                        correctSpecialties(abl, secondSpecialty)

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        inv = Inventory.humanInventory(rank, element, job).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, inv, rank)

class dragonslayer:
    def __init__(self, rank, element) -> None:
        job = "Dragonslayer"
        common = setCommon(job, rank, element)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"attacks": ["Bodkin"]})

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Wreath"]
            
            if rank in ["Adept", "Elite", "Master"]:
                abl["areas"] += ["Mark"]
                abl["specialty"] = [random.choice(["Bodkin", "Wreath"])]
                
                if rank in ["Elite", "Master"]:
                    abl["hindrances"] += ["Misdirect"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bodkin", "Misdirect", "Wreath"])]
                        correctSpecialties(abl, secondSpecialty)

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        inv = Inventory.humanInventory(rank, element, job).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, inv, rank)
        
class paladin:
    def __init__(self, rank) -> None:
        job, element = "Paladin", "Blessed"
        common = setCommon(job, rank, element)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"attacks": ["Sling"]})

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Wreath"]
            
            if rank in ["Adept", "Elite", "Master"]:
                abl["areas"] += ["Bless"]
                abl["specialty"] = [random.choice(["Sling", "Wreath"])]
                
                if rank in ["Elite", "Master"]:
                    abl["boons"] += ["Compel"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Compel", "Sling", "Wreath"])]
                        correctSpecialties(abl, secondSpecialty)

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        inv = Inventory.humanInventory(rank, element, job).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, inv, rank)