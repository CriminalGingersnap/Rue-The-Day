from . import Characters


# Totems cannot differentiate friend from foe and will randomly target fighters within range.

def setCommon(job) -> list:
    type = "totem"

    traits = Characters.setTraits()
    res = traits[1].update({"Pierce": "resistant", "Crush": "normal", "Dream": "immune",
                             "Burn": "vulnerable", "Freeze": "normal", "Venom": "immune",
                               "Holy": "normal", "Rot": "normal"})
    stats = {"avoidance": "min", "hp": "low", "resist": res, "speed": "min"}
    cndt = traits[0]
    cndt["lifeless"], cndt["reposed"] = True, True
    
    dice = {"martial": 0, "magic": 1}

    if job in ["Door", "Gate", "Totem", "Monument"]:
        if job in ["Gate", "Monument"]:
            cndt["massive"] = True
            stats["hp"] = "max"
            stats["resist"]["Burn"] = "normal"

        match job:
            case "Door": stats["hp"] = "mid"
            case "Gate": dice["magic"] = 2
            case "Totem":
                dice["magic"] = 3
                stats["hp"] = "high"
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

        abl = Characters.setAbilities(type, dice, {"areas": ["Hex"]})

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, "Hex")


class sentry:
    def __init__(self, element, job) -> None:        
        common = setCommon(job)
        stats, cndt, type, dice = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, dice, {"attacks": ["Bring"]})

        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, "Sentry")


class ward:
    def __init__(self, element, job) -> None:        
        common = setCommon(job)
        stats, cndt, type, dice,  = common[0], common[1], common[2], common[3]

        abl = Characters.setAbilities(type, dice, {"boons": ["Wreath"]})
        
        self.ch = Characters.character(abl, dice, cndt, stats, job, element, type, "Ward")

# Agents of the king have a chance to bring this with them.