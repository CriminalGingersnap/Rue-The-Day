from . import Characters, Insects, Animals
from Systems import Inventory


def setCommon(element, rank) -> list:
    common = Insects.setCommon(element, rank)
    common[1]["armored"], common[1]["reposed"], common["skittish"] = False, True, True
    common[3] = "invertebrate"

    return common


class mussel:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"] = True
        stats["speed"] = "min"

        abl = Characters.setAbilities(type, {"boons": ["Guard", "Wreath"]})
        dice = {"martial": 1, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Mussel", element, type, drop, rank)
        
    
class urchin:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["speed"] = "min"

        abl = Characters.setAbilities(type, {"attacks": ["Sting"], "boons": ["Bristle"]})
        dice = {"martial": 1, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Urchin", element, type, drop, rank)

class worm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"boons": ["Wreath"]})
        dice = {"martial": 0, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Worm", element, type, drop, rank)