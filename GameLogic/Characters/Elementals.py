from . import Characters
from Systems import Inventory
import random


def setElementalResistance(element, stats):
    if element == "Fey":
        stats["resist"]["Dream"] = "immune"
        stats["resist"]["Rot"] = "resistant"
    elif element == "Flame":
        stats["resist"]["Burn"] = "immune"
        stats["resist"]["Freeze"] = "vulnerable"
    elif element == "Blessed":
        stats["resist"]["Holy"] = "resistant"
    elif element == "Ice":
        stats["resist"]["Freeze"] = "immune"
        stats["resist"]["Burn"] = "vulnerable"

def setCommon(element, rank) -> list:
    type = "elemental"
    if rank == "Random": rank = random.choice(["Lesser", "Greater"])

    traits = Characters.setTraits()
    res = traits[1].update({"Pierce": "immune", "Crush": "normal", "Dream": "resistant",
                             "Burn": "normal", "Freeze": "normal", "Venom": "immune",
                               "Holy": "normal", "Rot": "immune"})
    stats = {"avoidance": "mid", "hp": "high", "resist": res, "speed": "mid"}
    cndt = traits[0]
    cndt["lifeless"], cndt["sapient"] = True, True

    setElementalResistance(element, stats) 

    return [stats, cndt, type, rank]


class dancer:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        
        stats["avoidance"] = "high"
        stats["resist"]["Crush"] = "vulnerable"
        stats["speed"] = "max"

        abl = Characters.setAbilities(type, {"attacks": ["Stab"], "hindrances": ["Bind"], "reactions": ["Riposte"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater": dice["martial"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Dancer", element, type, drop, rank)
        
class hulk: # it walks on three legs like a strand beast
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "low"
        stats["hp"] = "max"

        abl = Characters.setAbilities(type, {"attacks": ["Bash"], "boons": ["Guard", "Wreath"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater":
            dice["martial"] += 1
            dice["magic"] += 1
        
        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Hulk", element, type, drop, rank)
        
class obelisk:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        abl = Characters.setAbilities(type, {"areas": ["Hex"], "attacks": ["Bring"], "boons": ["Shroud"], "hindrances": ["Compel", ""]})
        dice = {"martial": 0, "magic": 3}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Obelisk", element, type, drop, rank)
        

class hive:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        abl = Characters.setAbilities(type, {"attacks": ["Bodkin", "Broadhead"], "boons": ["Wreath"], "hindrance": ["Disorient"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Sprite Hive", element, type, drop, rank)

class ooze:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "low"
        stats["speed"] = "low"

        abl = Characters.setAbilities(type, {"attacks": ["Bash"], "boons": ["Regenerate", "Wreath"]})
        dice = {"martial": 1, "magic": 2}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Ooze", element, type, drop, rank)

class puffer:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["resist"]["Pierce"] = "vulnerable"

        abl = Characters.setAbilities(type, {"attacks": ["Bring", "Stab"], "boons": ["Bristle", "Wreath"]})
        dice = {"martial": 3, "magic": 2}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Puffer Fish", element, type, drop, rank)


class satyr:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "high"
        stats["speed"] = "high"

        abl = Characters.setAbilities(type, {"attacks": ["Broadhead"], "boons": ["Shroud", "Wreath"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Satyr", element, type, drop, rank)

class ogre:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        
        stats["avoidance"] = "low"
        stats["hp"] = "max"
        stats["resist"]["Crush"], stats["resist"]["Pierce"] = "resistant", "resistant"

        abl = Characters.setAbilities(type, {"attacks": ["Bash"], "boons": ["Slip", "Wreath"], "hindrances": ["Disorient"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater": dice["martial"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Ogre", element, type, drop, rank)

class nymph:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"boons": ["Breath", "Wreath"], "hindrances": ["Compel"]})
        dice = {"martial": 0, "magic": 3}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Nymph", element, type, drop, rank)


class sphinx:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"attacks": ["Claw"], "boons": ["Wreath"], "hindrances": ["Compel"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater": dice["martial"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Sphinx", element, type, drop, rank)


class wisp:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["sapient"] = False
        stats["avoidance"], stats["hp"], stats["speed"] = "max", "low", "max"

        abl = Characters.setAbilities(type, {"hindrances": ["Disorient", "Misdirect", "Seal"]})
        dice = {"martial": 0, "magic": 1}
        if rank == "Greater": dice["magic"] += 3

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Wisp", element, type, drop, rank)