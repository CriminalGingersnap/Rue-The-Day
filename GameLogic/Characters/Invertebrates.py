from . import Characters, Insects, Animals


def setCommon(element, rank) -> list:
    common = Insects.setCommon(element, rank)
    common[1]["armored"], common[1]["reposed"], common[1]["skittish"] = False, True, True
    common[3] = "invertebrate"

    return common


class anemone:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["planted"] = True, True
        stats["hp"], stats["speed"] = "max", "min"

        dice = {"martial": 2, "magic": 2}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"attacks": ["Sting"], "areas": ["Infuse"], "hindrances": ["Bind"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Anemone", rank, stats, type)

class crab:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["armored"], cndt["reposed"] = True, True, False
        stats["hp"] = "high"

        dice = {"martial": 3, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"attacks": ["Pinch"], "boons": ["Guard"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Crab", rank, stats, type)

class leech:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["reposed"], cndt["skittish"] = True, False, False

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bite"], "hindrances": ["Drain"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Leech", rank, stats, type)

class mussel:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["armored"], cndt["planted"] = True, True
        stats["speed"] = "min"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"boons": ["Guard"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Mussel", rank, stats, type)

class octopus:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["aquatic"], cndt["reposed"] = True, False
        stats["hp"], stats["speed"] = "mid", "mid"

        dice = {"martial": 3, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bash", "Peck"], "hindrances": ["Bind"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Octopus", rank, stats, type)

class slug:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 1, "magic": 1}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"attacks": ["Spray"], "boons": ["Wreath"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Slug", rank, stats, type)

class starfish:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        stats["hp"]= "max"

        dice = {"martial": 3, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"attacks": ["Spit"], "boons": ["Guard"], "reactions": ["Riposte"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Starfish", rank, stats, type)

class urchin:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]
        stats["speed"] = "min"

        dice = {"martial": 2, "magic": 0}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"attacks": ["Stab"], "boons": ["Guard"], "reactions": ["Riposte"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Urchin", rank, stats, type)

class worm:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, rank, type = common[0], common[1], common[2], common[3]

        dice = {"martial": 0, "magic": 2}
        Animals.makeUpdates(element, cndt, rank, stats, dice)
        abl = Characters.setAbilities(rank, type, {"boons": ["Wreath"]})

        self.ch = Characters.character(abl, cndt, dice, element, "Worm", rank, stats, type)