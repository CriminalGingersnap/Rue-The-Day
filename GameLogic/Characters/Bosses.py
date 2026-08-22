from . import Characters, Animals
import random


def setCommon(element) -> list:
    rank, type = "Ascendant", "beast"

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["massive"], cndt["insightful"], cndt["inviolable"] = True, True, True
    stats = {"avoidance": "low", "hp": "boss", "resist": traits[1], "speed": "mid"}
    Animals.setAnimalResistance(element, rank, stats)   

    return [stats, cndt, type, rank]


class angler:
    def __init__(self) -> None:
        element = "Dream"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["planted"] = True
        stats["avoidance"], stats["speed"] = "min", "min"
        stats["resist"]["Bash"], stats["resist"]["Dream"], stats["resist"]["Flame"] = "resistant", "immune", "resistant"

        dice = {"martial": 3, "magic": 5}
        abl = Characters.setAbilities(rank, type, {"boons": ["Conceal"], "hindrances": ["Bind", "Compel", "Intoxicate"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Angler Vine", rank, stats, type)

class dragon:
    def __init__(self) -> None:
        element = random.choice(["Flame", "Ice"])
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["winged"] = True, True
        stats["speed"] = "high"

        dice = {"martial": 6, "magic": 3}
        abl = Characters.setAbilities(rank, type, {"areas": ["Breath"], "attacks": ["Bash", "Bite"], "hindrances": ["Stun"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Dragon", rank, stats, type)


class leviathan:
    def __init__(self) -> None:
        element = "Toxic"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aquatic"] = True, True

        dice = {"martial": 7, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Ram", "Bite", "Spray"], "hindrances": ["Bind"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Leviathan", rank, stats, type)

class lich:
    def __init__(self, days) -> None:
        element = "Rot"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], "human", common[3]
        cndt["massive"], cndt["sapient"] = False, True
        stats["avoidance"] = "min"

        dice = {"martial": 0, "magic": 6}
        abl = Characters.setAbilities(rank, type, {"areas": ["Screen"], "attacks": ["Bring"], "boons": ["Wreath"], "hindrances": ["Seal"]})
        abl["mastery"] = ["Wreath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Lich", rank, stats, type)
        self.ch.atrb["base_hp"] = self.ch.atrb["cur_hp"] = min(50, days + 20)

class vampire:
    def __init__(self, days) -> None:
        element = "Bleed"
        common = setCommon(element)
        stats, cndt, type, rank = common[0], common[1], "human", common[3]
        cndt["massive"], cndt["sapient"] = False, True
        stats["avoidance"], stats["speed"] = "mid", "max"

        dice = {"martial": 3, "magic": 3}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Claw", "Bite"], "hindrances": ["Compel", "Drain", "Stun"]})
        abl["mastery"] = ["Drain"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Vampire", rank, stats, type)
        self.ch.atrb["base_hp"] = self.ch.atrb["cur_hp"] = min(50, days + 15)


class giant:
    def __init__(self) -> None:
        element = "Dream"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["sapient"], cndt["skittish"] = True, True

        dice = {"martial": 3, "magic": 4}
        abl = Characters.setAbilities(rank, type, {"areas": ["Breath"], "attacks": ["Bash"], "boons": ["Veil"], "hindrances": ["Confound"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Giant", rank, stats, type)

class worm:
    def __init__(self) -> None:
        element = "Ice"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3] 
        cndt["reposed"] = True  
        stats["avoidance"], stats["speed"]  = "min", "low"

        dice = {"martial": 4, "magic": 3}
        abl = Characters.setAbilities(rank, type, {"areas": ["Slip"], "attacks": ["Ram", "Spit"], "boons": ["Wreath"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Worm", rank, stats, type)

class strider:
    def __init__(self) -> None:
        element = "Flame"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["winged"] = True, True
        stats["speed"] = "high"

        dice = {"martial": 7, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bite", "Kick", "Sting"], "boons": ["Guard"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Strider", rank, stats, type)