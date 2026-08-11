from . import Characters, Animals
import random


def setCommon(element, rank) -> list:
    type = "bird"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["winged"] = True
    
    stats = {"avoidance": "high", "hp": "min", "resist": traits[1], "speed": "high"}
    Animals.setAnimalResistance(element, rank, stats)

    return [stats, cndt, rank, type]


class crow:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["skittish"], cndt["social"] = True, True
        stats["avoidance"] = "high"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Peck"], "boons": ["Rally"]})
        if rank == "Elder": abl["boons"] += ["Veil"]

        self.ch = Characters.character(abl, cndt, dice, element, "Crow", rank, stats, type)

class eagle:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"] = "low"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Claw"], "hindrances": ["Bind"]})
        if rank == "Elder": abl["areas"] += ["Focus"]

        self.ch = Characters.character(abl, cndt, dice, element, "Eagle", rank, stats, type)

class hawk:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["speed"] = "max"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Kick", "Peck"]})
        if rank == "Elder": abl["hindrances"] += ["Stun"]

        self.ch = Characters.character(abl, cndt, dice, element, "Hawk", rank, stats, type)

class ostrich:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["winged"] = False
        stats["avoidance"], stats["hp"] = "low", "high"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Kick"], "boons": ["Guard"]})
        if rank == "Elder": abl["hindrances"] += ["Confound"]

        self.ch = Characters.character(abl, cndt, dice, element, "Ostrich", rank, stats, type)

class vulture:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["skittish"] = True
        stats["avoidance"], stats["hp"], stats["speed"] = "mid", "low", "mid"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)

        abl = Characters.setAbilities(type, {"attacks": ["Peck", "Spit"]})
        if rank == "Elder": abl["boons"] += ["Wreath"]

        self.ch = Characters.character(abl, cndt, dice, element, "Vulture", rank, stats, type)
