from . import Characters, Insects, Animals


def setCommon(element, rank) -> list:
    common = Insects.setCommon(element, rank)
    common[1]["armored"], common[1]["reposed"], common[1]["skittish"] = False, True, True
    common[3] = "invertebrate"

    return common


class crab:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["armored"] = True, True
        stats["hp"], stats["speed"] = "high", "min"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Pinch"], "boons": ["Guard"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Crab", rank, stats, type)

class leech:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["reposed"], cndt["skittish"] = True, False, False

        dice = {"martial": 1, "magic": 1}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bite"],"boons": ["Wreath"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Leech", rank, stats, type)

class mussel:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"] = True
        stats["speed"] = "min"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"boons": ["Guard"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Mussel", rank, stats, type)

class octopus:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["reposed"] = True, False
        stats["hp"], stats["speed"] = "mid", "mid"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Bite"], "hindrances": ["Bind"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Octopus", rank, stats, type)
    
class urchin:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["speed"] = "min"

        dice = {"martial": 1, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"attacks": ["Stab"], "boons": ["Guard"], "reactions": ["Riposte"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Urchin", rank, stats, type)

class worm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 0, "magic": 1}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(type, {"boons": ["Wreath"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Worm", rank, stats, type)