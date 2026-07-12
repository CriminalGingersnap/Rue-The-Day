# Mark dragon "shadow" with "_^^_" and leviathan with "_vv_" 

from . import Characters, Animals


def setCommon(element) -> list:
    rank, type = "Boss", "beast"

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["aggressive"], cndt["massive"] = True, True
    stats = {"hp": "mid", "resist": traits[1]}
    Animals.setAnimalResistance(element, rank, stats)   

    return [stats, cndt, type, rank]


class hydra:
    def __init__(self) -> None:
        element = "Toxic"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        dice = {"martial": 4, "magic": 2}
        abl = Characters.setAbilities(type, dice, {"area": ["Breath"], "attacks": ["Bash", "Bite"], "boons": ["Regenerate"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, dice, cndt, stats, "Kraken", element, type, rank)

class kraken:
    def __init__(self) -> None:
        element = "Basic"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        dice = {"martial": 6, "magic": 0}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bash", "Bite"], "hindrances": ["Bind", "Harry"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, dice, cndt, stats, "Kraken", element, type, rank)

class deathShell:
    def __init__(self) -> None:
        element = "Rot"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        dice = {"martial": 2, "magic": 4}
        abl = Characters.setAbilities(type, dice, {"areas": ["Hex"], "attacks": ["Ram"], "boons": ["Guard", "Wreath"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, dice, cndt, stats, "Death Shell", element, type, rank)


class dreamGiant:
    def __init__(self) -> None:
        element = "Dream"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "mid"

        dice = {"martial": 0, "magic": 6}
        abl = Characters.setAbilities(type, dice, {"area": ["Breath"], "attacks": ["Bring"], "hindrances": ["Compel", "Shroud"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Dream Giant", element, type, rank)

class glacierWorm:
    def __init__(self) -> None:
        element = "Ice"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]   
        stats["avoidance"], stats["hp"], stats["speed"]  = "low", "boss", "low"

        dice = {"martial": 3, "magic": 3}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Ram", "Spit"], "boons": ["Wreath"], "reactions": ["Flare"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Glacier Worm", element, type, rank)

class volcanoStrider:
    def __init__(self) -> None:
        element = "Flame"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["hp"], stats["speed"]  = "mid", "boss", "high"

        dice = {"martial": 6, "magic": 0}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bite", "Kick", "Spray"], "boons": ["Guard"]})

        self.ch = Characters.character(abl, dice, cndt, stats, "Volcano Strider", element, type, rank)