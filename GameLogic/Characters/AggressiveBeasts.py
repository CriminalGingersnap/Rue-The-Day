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

        if rank == "Elder": abl["boons"] += ["Shroud"]
        
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Bear", element, type, drop, rank)

class hound:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["social"] = True
        stats["speed"] = "max"
        
        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Guard"], "hindrances": ["Harry"]})
        dice = {"martial": 1, "magic": 0}

        if rank == "Elder": abl["boons"] += ["Focus"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Hound", element, type, drop, rank)

class ferret:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"] = "max"

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"], "boons": ["Evade"]})
        dice = {"martial": 1, "magic": 0}

        if rank == "Elder": abl["hindrances"] += ["Disorient"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Ferret", element, type, drop, rank)

class mole:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["speed"] = "low", "low"
        stats["hp"] = "high"

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"], "boons": ["Wreath"]})
        dice = {"martial": 1, "magic": 1}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Mole", element, type, drop, rank)

class moose:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        abl = Characters.setAbilities(type, {"attacks": ["Kick", "Gore"]})
        dice = {"martial": 2, "magic": 0}

        if rank == "Elder":
            if element == "Fey": abl["hindrances"] += ["Misdirect"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Moose", element, type, drop, rank)