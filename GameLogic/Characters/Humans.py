from . import Characters, Animals
import random


def setCommon(job, element, rank) -> list:
    type, dice = "human", {"martial": 0, "magic": 0}

    traits = Characters.setTraits()
    cndt = traits[0]
    stats = {"avoidance": "mid", "hp": "mid", "resist": traits[1], "speed": "mid"}
    Animals.setAnimalResistance(element, rank, stats)
    cndt["sapient"] = True

    if rank == "Random": rank = random.choice(["Proficient", "Adept", "Elite"])
    if rank in ["Elite", "Master"]: stats["resist"]["Dream"] = "resistant"

    if job in ["Brute", "Knight"]: stats["speed"] = "high"

    match job:
        case "Archer" | "Brute" | "Knight":
            match rank:
                case "Novice": dice["martial"] = 1
                case "Proficient" | "Adept": dice["martial"] = 2
                case "Elite": dice["martial"] = 3
                case "Master": dice["martial"] = 4
        case "Mage":
            match rank:
                case "Novice": dice["magic"] = 1
                case "Proficient" | "Adept": dice["magic"] = 2
                case "Elite": dice["magic"] = 3
                case "Master": dice["magic"] = 4
        case "Dragonslayer" | "Paladin":
            match rank:
                case "Novice": dice["martial"] = 1
                case "Proficient" | "Adept": dice["martial"], dice["magic"] = 1, 1
                case "Elite": dice["martial"], dice["magic"] = 2, 1
                case "Master": 
                    if job == "Dragonslayer": dice["martial"], dice["magic"] = 3, 1
                    else: dice["martial"], dice["magic"] = 2, 2

    return [stats, cndt, dice, type]


class archer:
    def __init__(self, element, rank) -> None:
        job = "Archer"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        
        abl = Characters.setAbilities(type, {"attacks": ["Broadhead"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bodkin"]
            
            if rank == "Adept":
                abl["specialty"] = [random.choice(["Bodkin", "Broadhead"])]
                
            if rank in ["Elite", "Master"]:
                abl["boons"] += ["Conceal"]
            
                if rank == "Master":
                    abl["mastery"] = [random.choice(["Bodkin", "Broadhead", "Conceal"])]

        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class brute:
    def __init__(self, element, rank) -> None:
        job = "Brute"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Stab"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["hindrances"] += ["Harry"]

            if rank == "Adept":
                abl["specialty"] = [random.choice(["Bash", "Harry", "Stab"])]
                
            if rank in ["Elite", "Master"]:
                abl["hindrances"] += ["Bind"]
                if rank == "Elite":  abl["specialty"] = [random.choice(["Bash", "Bind", "Harry", "Stab"])]
                else: abl["mastery"] = [random.choice(["Bash", "Bind", "Harry", "Stab"])]

        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class dragonslayer:
    def __init__(self, element, rank) -> None:
        job = "Dragonslayer"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bodkin"]})

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Wreath"]
            
            if rank == "Adept": abl["specialty"] = [random.choice(["Bodkin", "Wreath"])]
                
            if rank in ["Elite", "Master"]:
                abl["boons"] += ["Conceal"]
                if rank == "Elite": abl["specialty"] = [random.choice(["Bodkin", "Conceal", "Wreath"])]
                else: abl["mastery"] = [random.choice(["Bodkin", "Conceal", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class knight:
    def __init__(self, element, rank) -> None:
        job = "Knight"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"boons": ["Guard"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bash", "Stab"]

            if rank in ["Adept", "Elite"]: abl["specialty"] = [random.choice(["Bash", "Guard", "Stab"])]
                
            if rank in ["Elite", "Master"]:
                abl["reactions"] += ["Riposte"]
                if rank == "Master": abl["mastery"] = [random.choice(["Bash", "Guard", "Stab"])]

        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class mage:
    def __init__(self, element, rank) -> None:
        job = "Mage"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"boons": ["Wreath"]})
                
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            if element == "Dream": abl["boons"] += ["Focus"]
            else: abl["attacks"] += ["Bring"]
            
            if rank in ["Adept", "Elite"]:
                if element == "Dream": abl["specialty"] = [random.choice(["Focus", "Wreath"])]
                else: abl["specialty"] = [random.choice(["Bring", "Wreath"])]
                
            if rank in ["Elite", "Master"]:
                if element == "Dream": abl["hindrances"] += ["Compel"]
                else: abl["areas"] += ["Shroud"]

                if rank == "Master":
                    abl["mastery"] = [random.choice(["Bring", "Wreath"])]
                    if element == "Dream": abl["mastery"] = [random.choice(["Compel", "Focus", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class paladin:
    def __init__(self, rank) -> None:
        job, element = "Paladin", "Holy"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Sling"]})

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Wreath"]
            
            if rank in ["Adept", "Elite"]: abl["specialty"] = [random.choice(["Sling", "Wreath"])]
                
            if rank in ["Elite", "Master"]:
                abl["areas"] += ["Bless"]                
                if rank == "Master": abl["mastery"] = [random.choice(["Sling", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)