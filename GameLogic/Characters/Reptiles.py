from . import Characters, Animals
import random


def setCommon(element, rank) -> list:
    type = "reptile"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["armored"] = True
    stats = {"hp": "mid", "resist": traits[1]}

    Animals.setAnimalResistance(element, rank, stats)
    stats["avoidance"] = "mid"
    stats["speed"] = "mid"

    return [stats, cndt, rank, type]


class crocodile:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True
        stats["hp"], stats["speed"] = "max", "high"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Conceal"]})
        if rank == "Elder": abl["hindrances"] += ["Confuse"]

        self.ch = Characters.character(abl, cndt, dice, element, "Crocodile", rank, stats, type)

class drake:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        stats["hp"] = "max"

        dice = {"martial": 3, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Gore"]})
        if rank == "Elder": abl["areas"] += ["Breath"]

        self.ch = Characters.character(abl, cndt, dice, element, "Drake", rank, stats, type)

class hydra:
    def __init__(self, element, rank) -> None:
        common = setCommon(element)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        stats["hp"] = "max"

        dice = {"martial": 1, "magic": 2}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Regenerate"]})
        if rank == "Elder": abl["areas"] += ["Breath"]

        self.ch = Characters.character(abl, cndt, dice, element, "Hydra", rank, stats, type)

class lizard:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["skittish"] = False, True
        stats["speed"] = "high"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"]})
        if rank == "Elder": abl["areas"] += ["Slip"]

        self.ch = Characters.character(abl, cndt, dice, element, "Lizard", rank, stats, type)

class tortoise:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["reposed"], cndt["skittish"] = True, True, True
        stats["hp"], stats["speed"] = "max", "low"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard"]})

        if rank == "Elder": abl["areas"] += ["Shroud"]

        self.ch = Characters.character(abl, cndt, dice, element, "Tortoise", rank, stats, type)

class turtle:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True
        stats["hp"], stats["speed"] = "high", "low"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Guard"]})

        if rank == "Elder": abl["boons"] += ["Wreath"]

        self.ch = Characters.character(abl, cndt, dice, element, "Snapping Turtle", rank, stats, type)

class wyrm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["winged"] = False, True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Spray"]})
        if rank == "Elder": abl["hindrances"] += ["Focus"]

        self.ch = Characters.character(abl, cndt, dice, element, "Wyrm", rank, stats, type)