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
        case "Archer" | "Brute" | "Doctor" | "Knight":
            match rank:
                case "Novice": dice["martial"] = 1
                case "Proficient" | "Adept": dice["martial"] = 2
                case "Elite": dice["martial"] = 3
                case "Master": dice["martial"] = 4
        case "Mage" | "Witch":
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

    return [cndt, dice, stats, type]

def setSpecialty(abl, specialtyLevel):
    abilityList = abl["areas"] + abl["attacks"] + abl["boons"] + abl["hindrances"]
    if specialtyLevel != "None": abl[specialtyLevel] = [random.choice(abilityList)]


class archer:
    def __init__(self, element, rank) -> None:
        job = "Archer"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        
        abl = Characters.setAbilities(type, {"attacks": ["Broadhead"]})
        specialtyLevel = "None"
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bodkin"]
            
            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["boons"] += ["Conceal"]
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class brute:
    def __init__(self, element, rank) -> None:
        job = "Brute"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Stab"]})
        specialtyLevel = "None"
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["hindrances"] += ["Harry"]

            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["hindrances"] += ["Bind"]
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class dragonslayer:
    def __init__(self, element, rank) -> None:
        job = "Dragonslayer"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bodkin"]})
        specialtyLevel = "None"

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Wreath"]

            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["boons"] += ["Conceal"]
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class doctor:
    def __init__(self, element, rank) -> None:
        job = "Doctor"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"boons": ["Bandage"]})
        specialtyLevel = "None"

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Rally"]

            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["boons"] += ["Fortify"]
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class knight:
    def __init__(self, element, rank) -> None:
        job = "Knight"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"boons": ["Guard"]})
        specialtyLevel = "None"
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bash", "Stab"]

            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["reactions"] += ["Riposte"]
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class mage:
    def __init__(self, element, rank) -> None:
        job = "Mage"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"boons": ["Wreath"]})
        specialtyLevel = "None"

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bring"]
            
            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["areas"] += ["Infuse"]
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class paladin:
    def __init__(self, element, rank) -> None:
        job = "Paladin"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Sling"]})
        specialtyLevel = "None"

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Heal"]
            
            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["areas"] += ["Bless"]                
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)

class witch:
    def __init__(self, element, rank) -> None:
        job = "Witch"
        common = setCommon(job, element, rank)
        cndt, dice, stats, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"boons": ["Focus"]})
        specialtyLevel = "None"

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["areas"] += ["Slip"]
            
            if rank in ["Adept", "Elite"]: specialtyLevel = "specialty"
            if rank in ["Elite", "Master"]:
                abl["hindrances"] += ["Compel"]
                if rank == "Master": specialtyLevel = "mastery"

        setSpecialty(abl, specialtyLevel)
        self.ch = Characters.character(abl, cndt, dice, element, job, rank, stats, type)