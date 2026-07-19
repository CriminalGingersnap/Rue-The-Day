from . import Characters, Animals
import random


def setCommon(element, rank) -> list:
    type = "beast"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["reposed"] = True
    
    stats = {"hp": "mid", "resist": traits[1], "speed": "max"}
    Animals.setAnimalResistance(element, rank, stats)

    stats["avoidance"] = "high"
    stats["speed"] = "high"

    return [stats, cndt, rank, type]


class camel:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["hp"] = "mid", "max"
        cndt["social"], cndt["massive"] = True, True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Spit", "Kick"]})
        if rank == "Elder": abl["boons"] += ["Shroud"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Camel", element, type, rank)

class deer:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["skittish"] = True

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": [random.choice(["Kick", "Gore"])], "boons": ["Conceal"]})
        if rank == "Elder": abl["boons"] += ["Focus"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Deer", element, type, rank)

class mole:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["speed"] = "low", "low"
        stats["hp"] = "high"

        dice = {"martial": 1, "magic": 1}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"], "boons": ["Wreath"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Mole", element, type, rank)

class rabbit:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["skittish"] = True
        stats["avoidance"], stats["hp"] = "max", "min"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"boons": ["Conceal"]})
        if rank == "Elder": abl["areas"] += ["Slip"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Rabbit", element, type, rank)

class seal:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["skittish"] = True, True

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Harry"]})
        if rank == "Elder": abl["boons"] += ["Disorient"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Seal", element, type, rank)