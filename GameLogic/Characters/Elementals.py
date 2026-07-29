from . import Characters, Humans
import random


def setElementalResistance(element, stats):
    if element == "Random": element = random.choice(["Dream", "Flame", "Ice"])
    
    match element:
        case "Holy": stats["resist"]["Holy"] = "immune"
        case "Rot": stats["resist"]["Holy"] = "vulnerable"
        case "Dream":
            stats["resist"]["Crush"], stats["resist"]["Pierce"] = "immune", "immune"
            stats["resist"]["Rot"] = "vulnerable"
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
    traits[1].update({"Pierce": "immune", "Rot": "immune"})
    stats = {"avoidance": "mid", "hp": "high", "resist": traits[1], "speed": "mid"}
    cndt = traits[0]
    cndt["lifeless"], cndt["sapient"] = True, True

    setElementalResistance(element, stats) 

    return [stats, cndt, type, rank]


class dancer:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        
        stats["avoidance"] = "high"
        stats["resist"]["Crush"] = "vulnerable"
        stats["speed"] = "max"

        dice = {"martial": 3, "magic": 0}
        abl = Characters.setAbilities(type, {"attacks": ["Stab"], "hindrances": ["Bind"], "reactions": ["Riposte"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bind", "Stab"])]
        else: abl["specialty"] = [random.choice(["Bind", "Stab"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Dancer", rank, stats, type)
        
class hulk: # it walks on three legs like a strand beast
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "low"
        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, {"attacks": ["Ram"], "boons": ["Guard", "Wreath"]})
        
        if rank == "Greater":
            dice["martial"] += 1
            dice["magic"] += 1
            abl["mastery"] = [random.choice(["Guard", "Ram", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Guard", "Ram", "Wreath"])]
        
        self.ch = Characters.character(abl, cndt, dice, element, "Hulk", rank, stats, type)

class wraith:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["winged"] = True

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, {"attacks": ["Bring"], "boons": ["Heal"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Heal"])]
        else: abl["specialty"] = [random.choice(["Bring", "Heal"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Screen"]

        self.ch = Characters.character(abl, cndt, dice, element, "Wraith", rank, stats, type)
        

class hive:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["planted"] = True, True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        dice = {"martial": 1, "magic": 2}
        abl = Characters.setAbilities(type, {"attacks": ["Bodkin", "Broadhead"], "boons": ["Wreath"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bodkin", "Broadhead", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Bodkin", "Broadhead", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Sprite Hive", rank, stats, type)

class ooze:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "low"
        stats["speed"] = "low"

        dice = {"martial": 1, "magic": 2}
        abl = Characters.setAbilities(type, {"attacks": ["Pinch"], "boons": ["Regenerate"], "hindrances": ["Harry"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Harry", "Pinch", "Regenerate"])]
        else: abl["specialty"] = [random.choice(["Harry", "Pinch", "Regenerate"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Ooze", rank, stats, type)

class puffer:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["winged"] = True

        stats["resist"]["Pierce"] = "vulnerable"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, {"attacks": ["Bring"], "boons": ["Guard"], "reactions": ["Riposte"]})

        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1
            abl["mastery"] = [random.choice(["Bring", "Guard"])]
        else: abl["specialty"] = [random.choice(["Bring", "Guard"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Puffer Fish", rank, stats, type)


class satyr:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "high"
        stats["speed"] = "high"

        dice = {"martial": 3, "magic": 0}
        abl = Characters.setAbilities(type, {"attacks": ["Broadhead", "Sling"], "boons": ["Conceal"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Broadhead", "Conceal", "Sling"])]
        else: abl["specialty"] = [random.choice(["Broadhead", "Conceal", "Sling"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Satyr", rank, stats, type)

class ogre:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        
        stats["avoidance"] = "low"
        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, {"areas": ["Slip"], "attacks": ["Bash"], "boons": ["Regenerate"]})

        if rank == "Greater": 
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bash", "Confuse", "Slip"])]
        else: abl["specialty"] = [random.choice(["Bash", "Confuse", "Slip"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Ogre", rank, stats, type)

class nymph:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["aquatic"] = True

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, {"boons": ["Wreath"], "hindrances": ["Compel", "Confound"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Compel", "Confound", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Compel", "Confound", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Nymph", rank, stats, type)


class bull:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        dice = {"martial": 3, "magic": 0}
        abl = Characters.setAbilities(type, {"attacks": ["Gore", "Kick"], "hindrances": ["Bind"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bind", "Gore", "Kick"])]
        else: abl["specialty"] = [random.choice(["Bind", "Gore", "Kick"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Bull", rank, stats, type)

class obelisk:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["planted"] = True, True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, {"attacks": ["Bring"], "boons": ["Veil"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Veil"])]
        else: abl["specialty"] = [random.choice(["Bring", "Veil"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Shroud"]

        self.ch = Characters.character(abl, cndt, dice, element, "Obelisk", rank, stats, type)

class sphinx:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"], cndt["winged"] = True, True

        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Claw"], "boons": ["Wreath"]})

        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1
            abl["mastery"] = [random.choice(["Bash", "Claw", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Bash", "Claw", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Sphinx", rank, stats, type)


class wisp:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["sapient"], cndt["winged"] = False, True
        stats["avoidance"], stats["hp"], stats["speed"] = "max", "low", "max"

        dice = {"martial": 0, "magic": 1}
        abl = Characters.setAbilities(type, {"hindrances": ["Compel", "Confound", "Seal"]})

        if rank == "Greater":
            dice["magic"] += 3
            abl["mastery"] = [random.choice(["Compel", "Confound", "Seal"])]
        else: abl["specialty"] = [random.choice(["Compel", "Confound", "Seal"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Wisp", rank, stats, type)



class grotesquery:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True        
        stats["avoidance"], stats["hp"], stats["speed"]  = "low", "max", "low"

        dice = {"martial": 3, "magic": 0}
        abl = Characters.setAbilities(type, {"attacks": ["Bash", "Stab"], "boons": ["Guard"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bash", "Stab", "Guard"])]
        else: abl["specialty"] = [random.choice(["Bash", "Stab", "Guard"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Grotesquery", rank, stats, type)

class shadow:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        
        stats["avoidance"] = "max"
        stats["speed"] = "low"

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, {"attacks": ["Bring"], "hindrances": ["Confuse", "Confound"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Heal"])]
        else: abl["specialty"] = [random.choice(["Bring", "Heal"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Screen"]

        self.ch = Characters.character(abl, cndt, dice, element, "Shadow", rank, stats, type)
        
class slime:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "min"
        stats["speed"] = "low"

        dice = {"martial": 1, "magic": 2}
        abl = Characters.setAbilities(type, {"attacks": ["Spit"], "boons": ["Wreath"], "hindrances": ["Drain"]})

        if rank == "Greater":
            dice["martial"] += 1
            dice["magic"] += 1
            abl["mastery"] = [random.choice(["Drain", "Spit", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Drain", "Spit", "Wreath"])]

        self.ch = Characters.character(abl, cndt, dice, element, "Slime", rank, stats, type)
