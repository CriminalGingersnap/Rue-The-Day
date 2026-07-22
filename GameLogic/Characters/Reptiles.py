from . import Characters, Animals
import random


def setCommon(element, rank) -> list:
    type = "reptile"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    stats = {"hp": "mid", "resist": traits[1]}

    Animals.setAnimalResistance(element, rank, stats)
    stats["avoidance"] = "mid"
    stats["speed"] = "mid"

    return [stats, cndt, rank, type]


class crocodile:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"], cndt["aquatic"] = True, True, True
        stats["hp"], stats["speed"] = "max", "high"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Conceal"]})
        if rank != "Juvenile": abl["hindrances"] += ["Disorient"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Crocodile", element, type, rank)

class drake:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"], cndt["massive"] = True, True, True
        stats["hp"] = "max"

        dice = {"martial": 3, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Gore"]})
        if rank != "Juvenile": abl["areas"] += ["Breath"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Drake", element, type, rank)
        
class lizard:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["speed"] = "high"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"]})
        if rank != "Juvenile": abl["areas"] += ["Slip"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Lizard", element, type, rank)

class tortoise:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["massive"] = True, True
        stats["hp"], stats["speed"] = "max", "low"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard"]})

        if rank != "Juvenile": abl["boons"] += ["Wreath"]

        self.ch = Characters.character(abl, dice, cndt, stats, "tortoise", element, type, rank)

class turtle:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"], cndt["aquatic"] = True, True, True
        stats["hp"], stats["speed"] = "high", "low"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Guard"]})

        if rank != "Juvenile": abl["boons"] += ["Shroud"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Snapping Turtle", element, type, rank)

class wyrm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"], cndt["winged"] = True, True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Spray"]})
        if rank != "Juvenile": abl["hindrances"] += ["Focus"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Wyrm", element, type, rank)