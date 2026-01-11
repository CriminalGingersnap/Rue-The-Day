from . import Characters, Animals
import Systems.Inventory as Inventory
import random


def setCommon(element, rank) -> list:
    type = "reptile"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    stats = {"hp": "mid", "resist": traits[1]}
    cndt["armored"] = True

    Animals.setAnimalResistance(element, rank, stats)
    stats["resist"]["Dream"] = "normal"

    stats["avoidance"] = "mid"
    stats["speed"] = "mid"

    return [stats, cndt, rank, type]


class drake:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["hp"], cndt["massive"] = "max",  True

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Claw"]})
        dice = {"martial": 2, "magic": 0}

        if rank != "Juvenile":
            abl["boons"] += ["Breath"]
            abl["hindrances"] += ["Disorient"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Drake", element, type, drop, rank)
        
class lizard:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["speed"] = "high"

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Evade"]})
        dice = {"martial": 1, "magic": 0}

        if rank == "Elder": abl["boons"] += ["Shroud"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Lizard", element, type, drop, rank)

class turtle:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max",  True
        stats["speed"] = "low"

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Ram"], "boons": ["Guard"]})
        dice = {"martial": 3, "magic": 0}

        if rank == "Elder": abl["boons"] += ["Wreath"]


        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Turtle", element, type, drop, rank)

class wyrm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Spray"], "hindrances": ["Disorient"]})
        dice = {"martial": 2, "magic": 1}

        if rank == "Elder": abl["attacks"] += ["Breath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(props, "Wyrm", element, type, drop, rank)