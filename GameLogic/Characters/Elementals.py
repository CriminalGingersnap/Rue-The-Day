from . import Characters
import random


def setElementalResistance(element, stats):
    if element == "Random": element = random.choice(["Dream", "Flame", "Holy", "Ice", "Rot"])
    
    match element:
        case "Holy": stats["resist"]["Holy"] = "immune"
        case "Rot": stats["resist"]["Holy"] = "vulnerable"
        case "Flame":
            stats["resist"]["Flame"] = "immune"
            stats["resist"]["Ice"] = "vulnerable"
        case "Ice":
            stats["resist"]["Ice"] = "immune"
            stats["resist"]["Flame"] = "vulnerable"

def setCommon(element, rank) -> list:
    type = "elemental"
    if rank == "Random": rank = random.choice(["Lesser", "Greater"])

    traits = Characters.setTraits()
    traits[1].update({"Pierce": "resistant", "Rot": "immune"})

    cndt = traits[0]
    cndt["armored"], cndt["lifeless"], cndt["sapient"] = True, True, True
    stats = {"avoidance": "mid", "hp": "high", "resist": traits[1], "speed": "mid"}

    if rank == "Greater": cndt["reposed"] = random.choice([True, False, False])
    else: cndt["reposed"] = random.choice([True, False, False, False, False, False])

    setElementalResistance(element, stats) 

    return [stats, cndt, type, rank]


class dancer:
    def __init__(self, rank, element="Ice") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["resist"]["Crush"], stats["speed"] = "high", "vulnerable", "max"

        dice = {"martial": 4, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Stab"], "hindrances": ["Bind"], "reactions": ["Riposte"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bind", "Stab"])]
        else: abl["specialty"] = [random.choice(["Bind", "Stab"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Dancer", rank, stats, type)
        
class tripod:
    def __init__(self, rank, element="Ice") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        stats["avoidance"], stats["hp"], stats["speed"] = "low", "max", "low"

        dice = {"martial": 3, "magic": 1}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Ram"], "boons": ["Guard", "Wreath"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Guard", "Ram", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Guard", "Ram", "Wreath"])]
        
        self.ch = Characters.character(abl, cndt, dice, element, "Tripod", rank, stats, type)

class wraith:
    def __init__(self, rank, element="Ice") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["winged"] = True

        dice = {"martial": 0, "magic": 4}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bring"], "boons": ["Heal"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Heal"])]
        else: abl["specialty"] = [random.choice(["Bring", "Heal"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Screen"]

        self.ch = Characters.character(abl, cndt, dice, element, "Wraith", rank, stats, type)
        

class balloon:
    def __init__(self, rank, element="Flame") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["winged"] = True
        stats["resist"]["Pierce"] = "vulnerable"

        dice = {"martial": 4, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"boons": ["Guard"], "hindrances": ["Bind"], "reactions": ["Riposte"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bind", "Guard"])]
        else: abl["specialty"] = [random.choice(["Bind", "Guard"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Balloon", rank, stats, type)

class hive:
    def __init__(self, rank, element="Flame") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["planted"] = True, True
        stats["avoidance"], stats["hp"], stats["speed"] = "min", "max", "min"

        dice = {"martial": 3, "magic": 1}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bodkin", "Broadhead"], "boons": ["Wreath"]})

        if rank == "Greater":
            dice["martial"] += 1
            dice["magic"] += 1
            abl["mastery"] = [random.choice(["Bodkin", "Broadhead", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Bodkin", "Broadhead", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Sprite Hive", rank, stats, type)

class ooze:
    def __init__(self, rank, element="Flame") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["speed"] = "low", "low"

        dice = {"martial": 2, "magic": 2}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Pinch"], "boons": ["Regenerate"], "hindrances": ["Harry"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Harry", "Pinch", "Regenerate"])]
        else: abl["specialty"] = [random.choice(["Harry", "Pinch", "Regenerate"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Ooze", rank, stats, type)


class satyr:
    def __init__(self, rank, element="Dream") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["speed"] = "high", "high"

        dice = {"martial": 4, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Broadhead", "Sling"], "boons": ["Conceal"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Broadhead", "Conceal", "Sling"])]
        else: abl["specialty"] = [random.choice(["Broadhead", "Conceal", "Sling"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Satyr", rank, stats, type)

class ogre:
    def __init__(self, rank, element="Dream") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        stats["avoidance"], stats["hp"] = "low", "max"

        dice = {"martial": 3, "magic": 1}
        abl = Characters.setAbilities(rank, type, {"areas": ["Slip"], "attacks": ["Bash"], "boons": ["Regenerate"]})

        if rank == "Greater": 
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bash", "Slip", "Stun"])]
        else: abl["specialty"] = [random.choice(["Bash", "Slip", "Stun"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Ogre", rank, stats, type)

class nymph:
    def __init__(self, rank, element="Dream") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True

        dice = {"martial": 0, "magic": 4}
        abl = Characters.setAbilities(rank, type, {"boons": ["Wreath"], "hindrances": ["Compel", "Confound"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Compel", "Confound", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Compel", "Confound", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Nymph", rank, stats, type)


class bull:
    def __init__(self, rank, element="Holy") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        dice = {"martial": 4, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Gore", "Kick"], "hindrances": ["Bind"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bind", "Gore", "Kick"])]
        else: abl["specialty"] = [random.choice(["Bind", "Gore", "Kick"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Bull", rank, stats, type)

class obelisk:
    def __init__(self, rank, element="Holy") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["planted"] = True, True
        stats["avoidance"], stats["hp"], stats["speed"] = "min", "max", "min"

        dice = {"martial": 0, "magic": 4}
        abl = Characters.setAbilities(rank, type, {"areas": ["Slip"], "attacks": ["Bring"], "boons": ["Veil"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Slip", "Veil"])]
        else: abl["specialty"] = [random.choice(["Bring", "Slip", "Veil"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Infuse"]

        self.ch = Characters.character(abl, cndt, dice, element, "Obelisk", rank, stats, type)

class sphinx:
    def __init__(self, rank, element="Holy") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["winged"] = True, True
        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 2}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bash", "Claw"], "boons": ["Wreath"]})

        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1
            abl["mastery"] = [random.choice(["Bash", "Claw", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Bash", "Claw", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Sphinx", rank, stats, type)


class wisp:
    def __init__(self, rank, element="Dream") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["sapient"], cndt["winged"] = False, True
        stats["avoidance"], stats["hp"], stats["speed"] = "max", "low", "max"

        dice = {"martial": 0, "magic": 2}
        abl = Characters.setAbilities(rank, type, {"hindrances": ["Compel", "Confound", "Seal"]})

        if rank == "Greater":
            dice["magic"] += 3
            abl["mastery"] = [random.choice(["Compel", "Confound", "Seal"])]
        else: abl["specialty"] = [random.choice(["Compel", "Confound", "Seal"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Wisp", rank, stats, type)


class grotesquery:
    def __init__(self, rank, element="Rot") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True        
        stats["avoidance"], stats["hp"], stats["speed"] = "low", "max", "low"

        dice = {"martial": 4, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bash", "Stab"], "boons": ["Guard"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bash", "Stab", "Guard"])]
        else: abl["specialty"] = [random.choice(["Bash", "Stab", "Guard"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Grotesquery", rank, stats, type)

class shadow:
    def __init__(self, rank, element="Rot") -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"],  stats["speed"] = "max", "low"

        dice = {"martial": 0, "magic": 4}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bring"], "hindrances": ["Confound", "Stun"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Heal"])]
        else: abl["specialty"] = [random.choice(["Bring", "Heal"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Screen"]

        self.ch = Characters.character(abl, cndt, dice, element, "Shadow", rank, stats, type)
        
class slime:
    def __init__(self, rank, element="Rot") -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["avoidance"], stats["speed"] = "min", "low"

        dice = {"martial": 1, "magic": 3}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Spit"], "boons": ["Wreath"], "hindrances": ["Drain"]})

        if rank == "Greater":
            dice["martial"] += 1
            dice["magic"] += 1
            abl["mastery"] = [random.choice(["Drain", "Spit", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Drain", "Spit", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Slime", rank, stats, type)


class naga:
    def __init__(self, rank, element=random.choice(["Dream", "Holy"])) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        stats["speed"] = "high"

        dice = {"martial": 2, "magic": 2}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Bash"], "hindrances": ["Bind", "Compel"]})

        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1
            abl["mastery"] = [random.choice(["Bash", "Bind", "Compel"])]
        else: abl["specialty"] = [random.choice(["Bash", "Bind", "Compel"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Naga", rank, stats, type)

class rakshasa:
    def __init__(self, rank, element=random.choice(["Flame", "Rot"])) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        stats["hp"] = "max"

        dice = {"martial": 4, "magic": 0}
        abl = Characters.setAbilities(rank, type, {"attacks": ["Stab"], "boons": ["Guard"], "reactions": ["Riposte"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Guard", "Stab", "Riposte"])]
        else: abl["specialty"] = [random.choice(["Guard", "Stab", "Riposte"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Rakshasa", rank, stats, type)

class mask:
    def __init__(self, rank, element=random.choice(["Flame", "Ice"])) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["winged"] = True
        stats["avoidance"], stats["speed"] = "high", "min"

        dice = {"martial": 3, "magic": 1}
        abl = Characters.setAbilities(rank, type, {"areas": ["Slip"], "attacks": ["Bring"], "boons": ["Guard"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Slip", "Veil"])]
        else: abl["specialty"] = [random.choice(["Bring", "Slip", "Veil"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Mask", rank, stats, type)

class yogi:
    def __init__(self, rank, element=random.choice(["Ice", "Holy"])) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["social"] = True, True
        stats["avoidance"], stats["hp"], stats["speed"] = "high", "max", "low"

        dice = {"martial": 0, "magic": 4}
        abl = Characters.setAbilities(rank, type, {"boons": ["Focus", "Veil"], "hindrances": ["Confound"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Confound", "Focus"])]
        else: abl["specialty"] = [random.choice(["Bring", "Confound", "Focus"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Yogi", rank, stats, type)