from . import Characters, Animals
import random


def setCommon(element, rank) -> list:
    type = "insect"
    if rank == "Random": rank = random.choice(["Small", "Large"])

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["armored"] = True
    stats = {"avoidance": "low", "hp": "low", "resist": traits[1], "speed": "low"}

    Animals.setAnimalResistance(element, rank, stats)
    stats["resist"]["Dream"] = "resistant"

    return [stats, cndt, rank, type]


class ant:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["social"] = True

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Harry"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Ant", rank, stats, type)

class beetle:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["winged"] = True
        stats["hp"] = "mid"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Ram", "Spray"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Beetle", rank, stats, type)

class centipede:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Bind"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Centipede", rank, stats, type)

class hornet:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["social"], cndt["winged"] = True, True
        stats["avoidance"], stats["hp"], stats["speed"] = "max", "min", "mid"
        
        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Sting"], "hindrances": ["Harry"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Hornet", rank, stats, type)

class isopod:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["reposed"] = True, True
        stats["hp"]= "max"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Isopod", rank, stats, type)