from . import Characters
from Systems import Inventory
import random


def setElementalResistance(element, stats):
    if element == "Random":
        element = random.choice(["Fey", "Flame", "Ice"])
    
    elif element == "Blessed":
        stats["resist"]["Holy"] = "immune"
    if element == "Corpse":
        stats["resist"]["Holy"] = "vulnerable"
        stats["resist"]["Rot"] = "immune"
    if element == "Fey":
        stats["resist"]["Crush"], stats["resist"]["Pierce"] = "resistant", "resistant"
        stats["resist"]["Rot"] = "vulnerable"
    elif element == "Flame":
        stats["resist"]["Burn"] = "immune"
        stats["resist"]["Freeze"] = "vulnerable"
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
        dice = {"martial": 3, "magic": 0}
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

        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard", "Wreath"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater":
            dice["martial"] += 1
            dice["magic"] += 1
        
        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Hulk", element, type, drop, rank)

class wraith:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"attacks": ["Bring"], "boons": ["Heal"]})
        dice = {"martial": 0, "magic": 3}
        if rank == "Greater": dice["magic"] += 2

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Hex"]

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Wraith", element, type, drop, rank)
        

class hive:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        abl = Characters.setAbilities(type, {"attacks": ["Bodkin", "Sting"], "boons": ["Wreath"]})
        dice = {"martial": 1, "magic": 2}
        if rank == "Greater": dice["martial"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Sprite Hive", element, type, drop, rank)

class ooze:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "low"
        stats["speed"] = "low"

        abl = Characters.setAbilities(type, {"attacks": ["Pinch"], "boons": ["Regenerate"], "hindrances": ["Harry"]})
        dice = {"martial": 1, "magic": 2}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Ooze", element, type, drop, rank)

class puffer:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["resist"]["Pierce"] = "vulnerable"

        abl = Characters.setAbilities(type, {"attacks": ["Bring"], "boons": ["Bristle"], "hindrances": ["Bind"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Puffer Fish", element, type, drop, rank)


class satyr:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "high"
        stats["speed"] = "high"

        abl = Characters.setAbilities(type, {"attacks": ["Broadhead", "Sling"], "boons": ["Shroud"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Satyr", element, type, drop, rank)

class ogre:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        
        stats["avoidance"] = "low"
        stats["hp"] = "max"

        abl = Characters.setAbilities(type, {"attacks": ["Bash"], "boons": ["Slip"], "hindrances": ["Disorient"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater": dice["martial"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Ogre", element, type, drop, rank)

class nymph:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"boons": ["Wreath"], "hindrances": ["Compel", "Misdirect"]})
        dice = {"martial": 0, "magic": 3}
        if rank == "Greater": dice["magic"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Nymph", element, type, drop, rank)


class bull:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"attacks": ["Gore", "Kick"], "hindrances": ["Bind"]})
        dice = {"martial": 3, "magic": 0}
        if rank == "Greater":
            dice["martial"] += 2

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Bull", element, type, drop, rank)

class obelisk:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        abl = Characters.setAbilities(type, {"attacks": ["Bring"], "boons": ["Shroud"]})
        dice = {"martial": 0, "magic": 3}
        if rank == "Greater": dice["magic"] += 2

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Hex"]

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Obelisk", element, type, drop, rank)

class sphinx:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["hp"] = "max"

        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Claw"], "boons": ["Wreath"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Sphinx", element, type, drop, rank)


class wisp:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["sapient"] = False
        stats["avoidance"], stats["hp"], stats["speed"] = "max", "low", "max"

        abl = Characters.setAbilities(type, {"hindrances": ["Compel", "Misdirect", "Seal"]})
        dice = {"martial": 0, "magic": 1}
        if rank == "Greater": dice["magic"] += 3

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Wisp", element, type, drop, rank)



class grotesquery:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True        
        stats["avoidance"], stats["hp"], stats["speed"]  = "low", "max", "low"

        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Bring"], "boons": ["Guard", "Wreath"]})
        dice = {"martial": 2, "magic": 1}
        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Grotesquery", element, type, drop, rank)