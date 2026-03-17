# Mark dragon "shadow" with "_^^_" and leviathan with "_vv_" 

from . import Characters, Animals
from Systems import Inventory


def setCommon(element) -> list:
    rank, type = "Elder", "beast"

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["aggressive"], cndt["massive"] = True, True
    stats = {"hp": "mid", "resist": traits[1]}
    Animals.setAnimalResistance(element, rank, stats)   

    return [stats, cndt, type, rank]


class hydra:
    def __init__(self) -> None:
        element = "Toxin"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        abl = Characters.setAbilities(type, {"area": ["Breath"], "attacks": ["Bash", "Bite"], "boons": ["Regenerate"]})
        dice = {"martial": 4, "magic": 2}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Kraken", element, type, drop, rank)

class kraken:
    def __init__(self) -> None:
        element = "Basic"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Bite"], "hindrances": ["Bind", "Harry"]})
        dice = {"martial": 6, "magic": 0}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Kraken", element, type, drop, rank)

class deathShell:
    def __init__(self) -> None:
        element = "Corpse"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        abl = Characters.setAbilities(type, {"areas": ["Hex"], "attacks": ["Ram"], "boons": ["Guard", "Wreath"]})
        dice = {"martial": 2, "magic": 4}

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        drop = Inventory.beastInventory(stats["hp"], element, rank, type).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Death Shell", element, type, drop, rank)


class dreamGiant:
    def __init__(self) -> None:
        element = "Fey"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
                
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        abl = Characters.setAbilities(type, {"area": ["Breath"], "attacks": ["Bring"], "hindrances": ["Compel", "Shroud"]})
        dice = {"martial": 0, "magic": 6}

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Dream Giant", element, type, drop, rank)

class glacierWorm:
    def __init__(self) -> None:
        element = "Ice"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
                
        stats["avoidance"], stats["hp"], stats["speed"]  = "low", "boss", "low"

        abl = Characters.setAbilities(type, {"attacks": ["Ram", "Spit"], "boons": ["Wreath"], "reactions": ["Flare"]})
        dice = {"martial": 3, "magic": 3}

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Glacier Worm", element, type, drop, rank)

class volcanoStrider:
    def __init__(self) -> None:
        element = "Flame"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
                
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "high"

        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Kick", "Spray"], "boons": ["Guard"]})
        dice = {"martial": 6, "magic": 0}

        drop = Inventory.elementalInventory(element, rank).inventory
        self.ch = Characters.character(abl, dice, cndt, stats, "Volcano Strider", element, type, drop, rank)