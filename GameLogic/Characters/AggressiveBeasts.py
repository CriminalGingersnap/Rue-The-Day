import random
from . import Characters, Animals


def setCommon(element, rank) -> list:
    type = "beast"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Adult", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]

    stats = {"avoidance": "mid", "hp": "mid", "resist": traits[1], "speed": "high"}
    Animals.setAnimalResistance(element, rank, stats)   

    return [stats, cndt, rank, type]


class bear:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        dice = {"martial": 4, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Claw"], "hindrances": ["Bind"]})
        if rank == "Elder": abl["areas"] += ["Infuse"]

        self.ch = Characters.character(abl, cndt, dice, element, "Bear", rank, stats, type)

class ferret:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"] = "high"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Bite"], "hindrances": ["Harry"]})
        if rank == "Elder": abl["hindrances"] += ["Stun"]

        self.ch = Characters.character(abl, cndt, dice, element, "Ferret", rank, stats, type)

class hound:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["social"] = True
        
        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Bite"], "boons": ["Rally"]})
        if rank == "Elder": abl["boons"] += ["Focus"]

        self.ch = Characters.character(abl, cndt, dice, element, "Hound", rank, stats, type)

class lion:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"] = "high"
        cndt["social"] = True

        dice = {"martial": 4, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Claw"], "hindrances": ["Bind"]})
        if (rank == "Elder") and (element != "Basic"): abl["boons"] += ["Wreath"]

        self.ch = Characters.character(abl, cndt, dice, element, "Lion", rank, stats, type)

class moose:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        dice = {"martial": 3, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Kick", "Gore"]})
        if (rank == "Elder") and (element != "Basic"): abl["boons"] += ["Wreath"]

        self.ch = Characters.character(abl, cndt, dice, element, "Moose", rank, stats, type)

class sheep:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Ram"], "boons": ["Guard"]})
        if rank == "Elder": abl["hindrances"] += ["Confound"]

        self.ch = Characters.character(abl, cndt, dice, element, "Sheep", rank, stats, type)

class tiger:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"] = "high"
        cndt["social"] = True

        dice = {"martial": 4, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Claw"], "boons": ["Conceal"]})
        if (rank == "Elder") and (element != "Basic"): abl["areas"] += ["Slip"]

        self.ch = Characters.character(abl, cndt, dice, element, "Tiger", rank, stats, type)

class yeti:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"], cndt["social"] = "max", True, True

        dice = {"martial": 3, "magic": 1}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(rank, type, {"attacks": ["Sling"], "boons": ["Wreath"]})
        if rank == "Elder": abl["areas"] += ["Infuse"]

        self.ch = Characters.character(abl, cndt, dice, element, "Yeti", rank, stats, type)