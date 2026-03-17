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

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite", "Claw"]})

        if rank == "Elder":
            if element == "Fey": abl["areas"] += ["Slip"]
        
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Bear", element, type, drop, rank)

class hound:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["social"] = True
        stats["speed"] = "max"
        
        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "hindrances": ["Harry"]})

        if rank == "Elder":
            if element == "Fey": abl["boons"] += ["Focus"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Hound", element, type, drop, rank)

class ferret:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"] = "max"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "hindrances": ["Bind"]})

        if rank == "Elder":
            if element == "Fey": abl["hindrances"] += ["Disorient"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Ferret", element, type, drop, rank)

class lion:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], stats["speed"] = "high", "max"
        cndt["social"] = True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite", "Claw"]})

        if (rank == "Elder") and (element != "Basic"): abl["boons"] += ["Wreath"]
        
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Bear", element, type, drop, rank)

class moose:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Kick", "Gore"]})
        
        if rank == "Elder":
            if element == "Fey": abl["hindrances"] += ["Misdirect"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Moose", element, type, drop, rank)

class sheep:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Ram"], "boons": ["Guard"]})
        
        if (rank == "Elder") and (element != "Basic"): abl["boons"] += ["Wreath"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Sheep", element, type, drop, rank)