import random
from . import Characters, Animals
import Systems.Inventory as Inventory


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

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"]})
        dice = {"martial": 2, "magic": 0}

        if rank == "Elder":
            if element == "Fey": abl["boons"] += ["Slip"]
            else: abl["boons"] += ["Wreath"]
        
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Bear", element, type, drop, rank)

class hound:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["social"] = True
        stats["speed"] = "max"
        
        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Harry"]})
        dice = {"martial": 1, "magic": 0}

        if rank == "Elder":
            if element == "Fey": abl["boons"] += ["Focus"]
            else: abl["boons"] += ["Wreath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Hound", element, type, drop, rank)

class ferret:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"] = "max"

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Bind"]})
        dice = {"martial": 1, "magic": 0}

        if rank == "Elder":
            if element == "Fey": abl["hindrances"] += ["Disorient"]
            else: abl["boons"] += ["Wreath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Ferret", element, type, drop, rank)

class lion:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], stats["speed"] = "high", "max"
        cndt["social"] = True

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"]})
        dice = {"martial": 2, "magic": 0}

        if rank == "Elder": abl["boons"] += ["Wreath"]
        
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Bear", element, type, drop, rank)

class moose:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        abl = Characters.setAbilities(type, {"attacks": ["Kick", "Gore"]})
        dice = {"martial": 2, "magic": 0}

        if rank == "Elder":
            if element == "Fey": abl["hindrances"] += ["Misdirect"]
            else: abl["boons"] += ["Wreath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Moose", element, type, drop, rank)

class sheep:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard"]})
        dice = {"martial": 1, "magic": 0}

        if rank == "Elder": abl["boons"] += ["Wreath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Sheep", element, type, drop, rank)