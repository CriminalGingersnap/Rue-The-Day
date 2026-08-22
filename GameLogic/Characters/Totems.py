from . import Characters


def setCommon(job) -> list:
    type = "totem"

    traits = Characters.setTraits()
    cndt = traits[0]
    cndt["lifeless"], cndt["planted"], cndt["reposed"], cndt["skittish"], cndt["social"] = True, True, True, True, True
    stats = {"avoidance": "min", "hp": "low", "resist": traits[1], "speed": "min"}
    stats["resist"]["Pierce"] = "resistant"

    dice = {"martial": 0, "magic": 2}

    if job in ["Gate", "Monument"]: cndt["massive"], stats["hp"] = True, "max"

    match job:
        case "Standard": stats["resist"]["Flame"] = "vulnerable"
        case "Door":
            dice["magic"] = 3
            stats["hp"] = "mid"
            stats["resist"]["Flame"] = "normal"
        case "Gate":
            dice["magic"] = 4
            stats["resist"]["Flame"] = "resistant"
        case "Monument":
            dice["magic"] = 5
            stats["resist"]["Flame"], stats["resist"]["Pierce"] = "immune", "immune"

    return [stats, cndt, type, dice]


class guidance:
    def __init__(self, element, job) -> None:
        common = setCommon(job)
        stats, cndt, type, dice, = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities("None", type, {"boons": ["Focus", "Veil"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Guidance", stats, type)

class impedance:
    def __init__(self, element, job) -> None:
        common = setCommon(job)
        stats, cndt, type, dice, = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities("None", type, {"hindrances": ["Confound", "Stun"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Impedance", stats, type)


class sentry:
    def __init__(self, element, job) -> None:
        common = setCommon(job)
        stats, cndt, type, dice = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities("None", type, {"areas": ["Slip"], "attacks": ["Bring"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Sentry", stats, type)

class ward:
    def __init__(self, element, job) -> None:
        common = setCommon(job)
        stats, cndt, type, dice,  = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities("None", type, {"areas": ["Infuse"], "boons": ["Wreath"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Ward", stats, type)