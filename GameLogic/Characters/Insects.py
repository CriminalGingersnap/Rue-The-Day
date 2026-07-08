from . import Characters, Animals
import random


def setCommon(element, rank) -> list:
    type = "insect"
    if rank == "Random": rank = random.choice(["Small", "Large"])

    traits = Characters.setTraits()
    cndt = traits[0]
    stats = {"avoidance": "low", "hp": "low", "resist": traits[1], "speed": "low"}

    Animals.setAnimalResistance(element, rank, stats)
    stats["resist"]["Dream"] = "resistant"

    cndt["armored"] = True

    return [stats, cndt, rank, type]


class ant:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"], cndt["social"] = True, True

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "hindrances": ["Harry"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Ant", element, type, rank)

class beetle:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["hp"], stats["speed"] = "mid", "mid"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Ram", "Spray"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Beetle", element, type, rank)
        
class isopod:
    def __init__(self, element, rank) -> None:                
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        dice = {"martial": 3, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Ram"], "boons": ["Guard"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Isopod", element, type, rank)

class centipede:
    def __init__(self, element, rank) -> None:                
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["speed"] = "high"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "hindrances": ["Bind"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Centipede", element, type, rank)

class waspNest:
    def __init__(self, element, rank) -> None:                
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["avoidance"], stats["speed"] = "min", "min"
        
        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Sting"], "hindrances": ["Harry"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Wasp Nest", element, type, rank)