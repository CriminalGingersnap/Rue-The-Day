from . import Characters


def setCommon(job) -> list:
    type = "totem"

    traits = Characters.setTraits()
    traits[1].update({"Pierce": "resistant", "Flame": "vulnerable"})
    stats = {"avoidance": "min", "hp": "low", "resist": traits[1], "speed": "min"}
    cndt = traits[0]
    cndt["lifeless"], cndt["planted"], cndt["reposed"], cndt["skittish"], cndt["social"] = True, True, True, True, True
    
    dice = {"martial": 0, "magic": 1}

    if job in ["Door", "Gate", "Monument"]:
        if job in ["Gate", "Monument"]:
            cndt["massive"] = True
            stats["hp"] = "max"
            stats["resist"]["Flame"] = "normal"

        match job:
            case "Door":
                dice["magic"] = 2
                stats["hp"] = "mid"
            case "Gate":
                dice["magic"] = 3
            case "Monument":
                dice["magic"] = 5
                stats["resist"]["Pierce"] = "immune"

    return [stats, cndt, type, dice]


class guidance:
    def __init__(self, element, job) -> None:
        common = setCommon(job)
        stats, cndt, type, dice, = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"boons": ["Focus", "Veil"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Guidance", stats, type)

class impedance:
    def __init__(self, element, job) -> None:
        common = setCommon(job)
        stats, cndt, type, dice, = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"hindrances": ["Confound", "Stun"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Impedance", stats, type)


class sentry:
    def __init__(self, element, job) -> None:        
        common = setCommon(job)
        stats, cndt, type, dice = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"areas": ["Screen"], "attacks": ["Bring"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Sentry", stats, type)

class ward:
    def __init__(self, element, job) -> None:        
        common = setCommon(job)
        stats, cndt, type, dice,  = common[0], common[1], common[2], common[3]
        abl = Characters.setAbilities(type, {"areas": ["Shroud"], "boons": ["Wreath"]})
        self.ch = Characters.character(abl, cndt, dice, element, job, "Ward", stats, type)