from . import Characters


# Totems cannot differentiate friend from foe and will randomly target fighters within range.

def setCommon(job) -> list:
    type = "totem"

    traits = Characters.setTraits()
    traits[1].update({"Pierce": "resistant", "Flame": "vulnerable"})
    stats = {"avoidance": "min", "hp": "low", "resist": traits[1], "speed": "min"}
    cndt = traits[0]
    cndt["lifeless"], cndt["planted"], cndt["reposed"] = True, True, True
    
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


# add holy monument to the throne room
# add rot totem to ziggurat


class hex:
    def __init__(self, element, job) -> None:
        common = setCommon(job)
        stats, cndt, type, dice, = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"areas": ["Hex"]})

        self.ch = Characters.character(abl, cndt, dice, element, job, "Hex", stats, type)


class sentry:
    def __init__(self, element, job) -> None:        
        common = setCommon(job)
        stats, cndt, type, dice = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"attacks": ["Bring"]})

        self.ch = Characters.character(abl, cndt, dice, element, job, "Sentry", stats, type)


class ward:
    def __init__(self, element, job) -> None:        
        common = setCommon(job)
        stats, cndt, type, dice,  = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, {"boons": ["Wreath"]})
        
        self.ch = Characters.character(abl, cndt, dice, element, job, "Ward", stats, type)

# Agents of the king have a chance to bring this with them.