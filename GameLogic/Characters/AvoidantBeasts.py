from . import Characters, Animals
import Systems.Inventory as Inventory
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

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Spit", "Kick"]})

        if rank == "Elder":
            if element == "Fey": abl["boons"] += ["Focus"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Camel", element, type, drop, rank)

class deer:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["skittish"] = True

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": [random.choice(["Kick", "Gore"])], "boons": ["Conceal"]})

        if rank == "Elder":
            if element == "Fey": abl["boons"] += ["Misdirect"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Deer", element, type, drop, rank)

class mole:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["speed"] = "low", "low"
        stats["hp"] = "high"

        dice = {"martial": 1, "magic": 1}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite", "Claw"], "boons": ["Wreath"]})

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Mole", element, type, drop, rank)

class rabbit:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["skittish"] = True
        stats["avoidance"], stats["hp"] = "max", "min"

        dice = {"martial": 0, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"boons": ["Conceal", "Evade"]})

        if rank == "Elder":
            if element == "Fey": abl["areas"] += ["Slip"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Rabbit", element, type, drop, rank)

class seal:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["skittish"] = True, True

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite"], "boons": ["Harry"]})

        if rank == "Elder":
            if element == "Fey": abl["boons"] += ["Disorient"]

        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Seal", element, type, drop, rank)