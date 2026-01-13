from . import Characters, Animals
import Systems.Inventory as Inventory
import random


def setCommon(element, rank) -> list:
    type = "insect"

    traits = Characters.setTraits()
    stats = {"avoidance": "low", "hp": "low", "resist": traits[1], "speed": "low"}
    if rank == "Random": rank = random.choice(["Small", "Large"])
    if rank == "Small": stats["hp"] = "min"

    Animals.setAnimalResistance(element, rank, stats)
    stats["resist"]["Dream"] = "resistant"

    cndt = traits[0]
    cndt["armored"] = True

    return [stats, cndt, rank, type]

class ant:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"], cndt["social"] = True, True

        abl = Characters.setAbilities(type, {"attacks": ["Bite"], "hindrances": ["Harry"]})
        dice = {"martial": 1, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Ant", element, type, drop, rank)

class beetle:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["hp"], stats["speed"] = "mid", "mid"

        abl = Characters.setAbilities(type, {"attacks": ["Ram", "Spray"]})
        dice = {"martial": 2, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Beetle", element, type, drop, rank)
        
class isopod:
    def __init__(self, element, rank) -> None:                
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["hp"], cndt["massive"] = "max", True

        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard"]})
        dice = {"martial": 3, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Isopod", element, type, drop, rank)

class centipede:
    def __init__(self, element, rank) -> None:                
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["speed"] = "high"

        abl = Characters.setAbilities(type, {"attacks": ["Bite"]})
        dice = {"martial": 2, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Centipede", element, type, drop, rank)

class waspNest:
    def __init__(self, element, rank) -> None:                
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aggressive"] = True
        stats["avoidance"], stats["speed"] = "min", "min"
        
        abl = Characters.setAbilities(type, {"attacks": ["Sting"]})
        dice = {"martial": 1, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Wasp Nest", element, type, drop, rank)