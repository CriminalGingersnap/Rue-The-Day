from . import Characters, Animals
import random


def setCommon(element, rank) -> list:
    type = "beast"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["skittish"] = True
    
    stats = {"avoidance": "high", "hp": "mid", "resist": traits[1], "speed": "high"}
    Animals.setAnimalResistance(element, rank, stats)

    return [stats, cndt, rank, type]


class bat:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["winged"] = True
        stats["avoidance"], stats["hp"] = "max", "min"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Conceal"]})
        if rank == "Elder": abl["areas"] += ["Slip"]

        self.ch = Characters.character(abl, cndt, dice, element, "Bat", rank, stats, type)

class camel:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["hp"] = "mid", "max"
        cndt["social"], cndt["massive"] = True, True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Spit", "Kick"]})
        if rank == "Elder": abl["boons"] += ["Veil"]

        self.ch = Characters.character(abl, cndt, dice, element, "Camel", rank, stats, type)

class deer:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": [random.choice(["Kick", "Gore"])], "boons": ["Conceal"]})
        if rank == "Elder": abl["hindrances"] += ["Confound"]

        self.ch = Characters.character(abl, cndt, dice, element, "Deer", rank, stats, type)

class mole:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["speed"] = "low", "low"
        stats["hp"] = "high"

        dice = {"martial": 1, "magic": 1}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"], "boons": ["Wreath"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Mole", rank, stats, type)

class seal:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Harry"]})
        if rank == "Elder": abl["boons"] += ["Focus"]

        self.ch = Characters.character(abl, cndt, dice, element, "Seal", rank, stats, type)