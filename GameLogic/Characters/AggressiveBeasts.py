import random
from . import Characters, Animals


def setCommon(element, rank) -> list:
    type = "beast"
    if rank == "Random": rank = random.choice(["Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["aggressive"] = True
    stats = {"hp": "mid", "resist": traits[1]}
    Animals.setAnimalResistance(element, rank, stats)   

    stats["avoidance"] = "mid"
    stats["speed"] = "high"

    return [stats, cndt, rank, type]


class bear:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"]})
        if rank == "Elder": abl["areas"] += ["Shroud"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Bear", element, type, rank)

class hound:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["social"] = True
        
        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Harry"]})
        if rank == "Elder": abl["boons"] += ["Focus"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Hound", element, type, rank)

class ferret:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"] = "high"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Bind"]})
        if rank == "Elder": abl["hindrances"] += ["Disorient"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Ferret", element, type, rank)

class lion:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"] = "high"
        cndt["social"] = True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"]})
        if (rank == "Elder") and (element != "Basic"): abl["boons"] += ["Wreath"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Bear", element, type, rank)

class moose:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Kick", "Gore"]})
        if (rank == "Elder") and (element != "Basic"): abl["boons"] += ["Wreath"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Moose", element, type, rank)

class sheep:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard"]})
        if rank == "Elder": abl["hindrances"] += ["Misdirect"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Sheep", element, type, rank)