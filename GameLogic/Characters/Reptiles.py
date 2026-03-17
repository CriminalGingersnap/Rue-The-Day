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
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "boons": ["Conceal"]})

        if rank != "Juvenile":
            if element == "Fey": abl["hindrances"] += ["Disorient"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Crocodile", element, type, drop, rank)

class drake:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"], cndt["massive"] = True, True, True
        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite", "Gore"]})

        if rank != "Juvenile": abl["area"] += ["Breath"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Drake", element, type, drop, rank)
        
class lizard:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["speed"] = "high"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "boons": ["Evade"]})

        if rank != "Juvenile":
            if element == "Fey": abl["areas"] += ["Slip"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Lizard", element, type, drop, rank)

class tortoise:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["massive"] = True, True
        stats["hp"], stats["speed"] = "max", "low"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Ram"], "boons": ["Guard"]})

        if rank != "Juvenile": abl["boons"] += ["Wreath"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "tortoise", element, type, drop, rank)

class turtle:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["aggressive"], cndt["aquatic"] = True, True, True
        stats["hp"], stats["speed"] = "high", "low"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "boons": ["Guard"]})

        if rank != "Juvenile": abl["boons"] += ["Shroud"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Snapping Turtle", element, type, drop, rank)

class wyrm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite", "Spray"]})

        if rank != "Juvenile":
            if element == "Fey": abl["hindrances"] += ["Disorient"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Wyrm", element, type, drop, rank)