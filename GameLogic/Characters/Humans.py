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
        case "Dragonslayer" | "Paladin" | "Warlock":
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
    else: abl["specialty"] += secondSpecialty 


class archer:
    def __init__(self, element, rank) -> None:
        job = "Archer"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        
        abl = Characters.setAbilities(type, dice, {"attacks": ["Broadhead"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bodkin"]
            
            if rank in ["Adept", "Elite", "Master"]:
                abl["specialty"] = [random.choice(["Bodkin", "Broadhead"])]
                
                if rank in ["Elite", "Master"]:
                    abl["boons"] += ["Conceal"]
                
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bodkin", "Broadhead", "Conceal"])]
                        correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, rank)

class brute:
    def __init__(self, element, rank) -> None:
        job = "Brute"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, dice, {"attacks": ["Bash", "Stab"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["hindrances"] += ["Harry"]

            if rank in ["Adept", "Elite", "Master"]:
                abl["specialty"] = [random.choice(["Bash", "Guard", "Stab"])]
                
                if rank in ["Elite", "Master"]:
                    abl["hindrances"] += ["Bind"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bash", "Bind", "Harry", "Stab"])]
                        correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, rank)

class dragonslayer:
    def __init__(self, element, rank) -> None:
        job = "Dragonslayer"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, dice, {"attacks": ["Bodkin"]})

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Wreath"]
            
            if rank in ["Adept", "Elite", "Master"]:
                abl["specialty"] = [random.choice(["Bodkin", "Wreath"])]
                
                if rank in ["Elite", "Master"]:
                    abl["boons"] += ["Conceal"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bodkin", "Conceal", "Wreath"])]
                        correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, rank)

class knight:
    def __init__(self, element, rank) -> None:
        job = "Knight"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, dice, {"attacks": ["Bash", "Stab"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Guard"]

            if rank in ["Adept", "Elite", "Master"]:
                abl["specialty"] = [random.choice(["Bash", "Guard", "Stab"])]
                
                if rank in ["Elite", "Master"]:
                    abl["reactions"] += ["Riposte"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bash", "Guard", "Stab"])]
                        correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, rank)

class mage:
    def __init__(self, element, rank) -> None:
        job = "Mage"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, dice, {"attacks": ["Bash", "Stab"], "boons": ["Wreath"]})
                
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            if element == "Fey": abl["boons"] += ["Focus"]
            else: abl["attacks"] += ["Bring"]
            
            if rank in ["Adept", "Elite", "Master"]:
                if element == "Fey": abl["specialty"] = [random.choice(["Focus", "Wreath"])]
                else: abl["specialty"] = [random.choice(["Bring", "Wreath"])]
                
                if rank in ["Elite", "Master"]:
                    if element == "Fey": abl["hindrance"] += ["Disorient"]
                    else: abl["reactions"] += ["Flare"]

                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bring", "Wreath"])]
                        if element == "Fey": secondSpecialty = [random.choice(["Disorient", "Focus", "Wreath"])]
                        correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, rank)

class paladin:
    def __init__(self, rank) -> None:
        job, element = "Paladin", "Blessed"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, dice, {"attacks": ["Sling"]})

        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["boons"] += ["Wreath"]
            
            if rank in ["Adept", "Elite", "Master"]:
                abl["specialty"] = [random.choice(["Sling", "Wreath"])]
                
                if rank in ["Elite", "Master"]:
                    abl["areas"] += ["Bless"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Sling", "Wreath"])]
                        correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, rank)

class warlock:
    def __init__(self, element, rank) -> None:
        job = "Warlock"
        common = setCommon(job, element, rank)
        stats, cndt, dice, type = common[0], common[1], common[2], common[3]
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, dice, {"attacks": ["Bash", "Stab"]})
        
        if rank in ["Proficient", "Adept", "Elite", "Master"]:
            abl["attacks"] += ["Bring"]

            if rank in ["Adept", "Elite", "Master"]:
                abl["specialty"] = [random.choice(["Bash", "Bring", "Stab"])]
                
                if rank in ["Elite", "Master"]:
                    abl["areas"] += ["Hex"]
                    
                    if rank == "Master":
                        secondSpecialty = [random.choice(["Bash", "Bring", "Stab"])]
                        correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, rank)