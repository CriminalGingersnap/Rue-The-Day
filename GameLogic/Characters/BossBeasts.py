# Mark dragon "shadow" with "_^^_" and leviathan with "_vv_" 

from . import Characters, Animals


def setCommon(element) -> list:
    rank, type = "Ascendant", "beast"

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["massive"], cndt["inviolable"] = True, True
    stats = {"avoidance": "mid", "hp": "boss", "resist": traits[1], "speed": "mid"}
    Animals.setAnimalResistance(element, rank, stats)   

    return [stats, cndt, type, rank]


class hydra:
    def __init__(self) -> None:
        element = "Toxic"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        dice = {"martial": 4, "magic": 2}
        abl = Characters.setAbilities(type, {"area": ["Breath"], "attacks": ["Claw", "Bite"], "boons": ["Regenerate"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Hydra", rank, stats, type)

class leviathan:
    def __init__(self) -> None:
        element = "Holy"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["social"] = True, True

        dice = {"martial": 6, "magic": 0}
        abl = Characters.setAbilities(type, {"attacks": ["Ram", "Bite"], "hindrances": ["Bind", "Harry"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Leviathan", rank, stats, type)

class deathShell:
    def __init__(self) -> None:
        element = "Rot"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["armored"], cndt["lifeless"], cndt["sapient"] = True, True, True, True

        dice = {"martial": 2, "magic": 4}
        abl = Characters.setAbilities(type, {"areas": ["Screen"], "attacks": ["Ram"], "boons": ["Guard", "Wreath"]})

        Animals.makeUpdates(element, cndt, rank, stats, dice)
        self.ch = Characters.character(abl, cndt, dice, element, "Shell", rank, stats, type)


class dreamGiant:
    def __init__(self) -> None:
        element = "Dream"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["sapient"], cndt["skittish"] = True, True

        dice = {"martial": 0, "magic": 6}
        abl = Characters.setAbilities(type, {"area": ["Breath"], "attacks": ["Bring"], "boons": ["Veil"], "hindrances": ["Compel"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Giant", rank, stats, type)

class glacierWorm:
    def __init__(self) -> None:
        element = "Ice"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3] 
        cndt["reposed"] = True  
        stats["avoidance"], stats["speed"]  = "low", "low"

        dice = {"martial": 3, "magic": 3}
        abl = Characters.setAbilities(type, {"attacks": ["Ram", "Spit"], "boons": ["Wreath"], "reactions": ["Flare"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Worm", rank, stats, type)

class volcanoStrider:
    def __init__(self) -> None:
        element = "Flame"
        common = setCommon(element)

        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["winged"] = True, True
        stats["speed"]  = "high"

        dice = {"martial": 6, "magic": 0}
        abl = Characters.setAbilities(type, {"attacks": ["Bite", "Kick", "Spray"], "boons": ["Guard"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Strider", rank, stats, type)