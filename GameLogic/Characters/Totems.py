from . import Characters
import Systems.Inventory as Inventory


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
        common, hex = setCommon(job), ""
        stats, cndt, type, dice, = common[0], common[1], common[2], common[3]

        match element:
            case "Flame": hex = "Hex"
            case "Ice": hex = "Hex"
            case "Fey": hex = "Hex"
            case "Blessed": hex = "Hex"
            case "Corpse": hex = "Hex"

        abl = Characters.setAbilities(type, {"areas": [hex]})

        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.totemInventory(element, job).inventory
        self.ch = Characters.character(props, job, element, type, drop, "Hex")


class sentry:
    def __init__(self, element, job) -> None:        
        common, attack = setCommon(job), ""
        stats, cndt, type, dice = common[0], common[1], common[2], common[3]

        match element:
            case "Flame": attack = "Burn"
            case "Ice": attack = "Freeze"
            case "Fey": attack = "Dream"
            case "Blessed": attack = "Holy"
            case "Corpse": attack = "Rot"

        abl = Characters.setAbilities(type, {"attacks": [attack]})

        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.totemInventory(element, job).inventory
        self.ch = Characters.character(props, job, element, type, drop, "Sentry")


class ward:
    def __init__(self, element, job) -> None:        
        common, wreath = setCommon(job), ""
        stats, cndt, type, dice,  = common[0], common[1], common[2], common[3]

        match element:
            case "Flame": wreath = "Wreath"
            case "Ice": wreath = "Wreath"
            case "Fey": wreath = "Wreath"
            case "Blessed": wreath = "Wreath"
            case "Corpse": wreath = "Wreath"

        abl = Characters.setAbilities(type, {"boons": [wreath]})
        
        props = {"abl": abl, "cndt": cndt, "dice": dice, "stats": stats}
        drop = Inventory.totemInventory(element, job).inventory
        self.ch = Characters.character(props, job, element, type, drop, "Ward")

# Agents of the king have a chance to bring this with them.