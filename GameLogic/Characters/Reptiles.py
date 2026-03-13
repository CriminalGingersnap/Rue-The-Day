from . import Characters, Animals
import Systems.Inventory as Inventory
import random


def setCommon(element, rank) -> list:
    type = "reptile"
    if rank == "Random": rank = random.choice(["Juvenile", "Juvenile", "Juvenile", "Adult", "Adult", "Elder"])

    traits = Characters.setTraits()
    cndt = traits[0]
    stats = {"hp": "mid", "resist": traits[1]}

    Animals.setAnimalResistance(element, rank, stats)
    if stats["resist"]["Dream"] == "vulnerable":
        stats["resist"]["Dream"] = "normal"

    stats["avoidance"] = "mid"
    stats["speed"] = "mid"

    return [stats, cndt, rank, type]


class crocodile:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"] = True, True, True
        stats["hp"], stats["speed"] = "max", "high"

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Bind"]})
        dice = {"martial": 2, "magic": 0}

        if rank != "Juvenile":
            if element == "Fey": abl["boons"] += ["Shroud"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Crocodile", element, type, drop, rank)

class drake:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"], cndt["massive"] = True, True, True
        stats["hp"] = "max"

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Gore"]})
        dice = {"martial": 2, "magic": 0}

        if rank != "Juvenile": abl["area"] += ["Breath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Drake", element, type, drop, rank)
        
class lizard:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["speed"] = "high"

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Evade"]})
        dice = {"martial": 1, "magic": 0}

        if rank != "Juvenile":
            if element == "Fey": abl["boons"] += ["Slip"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Lizard", element, type, drop, rank)

class tortoise:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["massive"] = True, True
        stats["hp"], stats["speed"] = "max", "low"

        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard"]})
        dice = {"martial": 3, "magic": 0}

        if rank != "Juvenile": abl["boons"] += ["Wreath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "tortoise", element, type, drop, rank)

class turtle:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"] = True, True
        stats["hp"], stats["speed"] = "high", "low"

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "boons": ["Guard"]})
        dice = {"martial": 3, "magic": 0}

        if rank != "Juvenile": abl["boons"] += ["Wreath"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Snapping Turtle", element, type, drop, rank)

class wyrm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Spray"]})
        dice = {"martial": 2, "magic": 1}

        if rank != "Juvenile":
            if element == "Fey": abl["hindrances"] += ["Disorient"]

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Wyrm", element, type, drop, rank)