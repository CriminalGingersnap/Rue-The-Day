from . import Characters, Humans
import random


def setElementalResistance(element, stats):
    if element == "Random":
        element = random.choice(["Fey", "Flame", "Ice"])
    
    elif element == "Blessed":
        stats["resist"]["Holy"] = "immune"
    if element == "Corpse":
        stats["resist"]["Holy"] = "vulnerable"
        stats["resist"]["Rot"] = "immune"
    if element == "Fey":
        stats["resist"]["Crush"], stats["resist"]["Pierce"] = "resistant", "resistant"
        stats["resist"]["Rot"] = "vulnerable"
    elif element == "Flame":
        stats["resist"]["Burn"] = "immune"
        stats["resist"]["Freeze"] = "vulnerable"
    elif element == "Ice":
        stats["resist"]["Freeze"] = "immune"
        stats["resist"]["Burn"] = "vulnerable"

def setCommon(element, rank) -> list:
    type = "elemental"
    if rank == "Random": rank = random.choice(["Lesser", "Greater"])

    traits = Characters.setTraits()
    traits[1].update({"Pierce": "immune", "Crush": "normal", "Dream": "resistant",
                       "Burn": "normal", "Freeze": "normal", "Venom": "immune",
                        "Holy": "normal", "Rot": "immune"})
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
        abl = Characters.setAbilities(type, dice, {"attacks": ["Stab"], "hindrances": ["Bind"], "reactions": ["Riposte"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bind", "Stab"])]
        else: abl["specialty"] = [random.choice(["Bind", "Stab"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Dancer", element, type, rank)
        
class hulk: # it walks on three legs like a strand beast
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "low"
        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Ram"], "boons": ["Guard", "Wreath"]})
        
        if rank == "Greater":
            dice["martial"] += 1
            dice["magic"] += 1
            abl["mastery"] = [random.choice(["Guard", "Ram", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Guard", "Ram", "Wreath"])]
        
        self.ch = Characters.character(abl, dice, cndt, stats, "Hulk", element, type, rank)

class wraith:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bring"], "boons": ["Heal"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Heal"])]
        else: abl["specialty"] = [random.choice(["Bring", "Heal"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Hex"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Wraith", element, type, rank)
        

class hive:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        dice = {"martial": 1, "magic": 2}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bodkin", "Sting"], "boons": ["Wreath"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bodkin", "Sting", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Bodkin", "Sting", "Wreath"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Sprite Hive", element, type, rank)

class ooze:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "low"
        stats["speed"] = "low"

        dice = {"martial": 1, "magic": 2}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Pinch"], "boons": ["Regenerate"], "hindrances": ["Harry"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Harry", "Pinch", "Regenerate"])]
        else: abl["specialty"] = [random.choice(["Harry", "Pinch", "Regenerate"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Ooze", element, type, rank)

class puffer:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["resist"]["Pierce"] = "vulnerable"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bring"], "boons": ["Guard"], "reactions": ["Riposte"]})

        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1
            abl["mastery"] = [random.choice(["Bring", "Guard"])]
        else: abl["specialty"] = [random.choice(["Bring", "Guard"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Puffer Fish", element, type, rank)


class satyr:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "high"
        stats["speed"] = "high"

        dice = {"martial": 3, "magic": 0}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Broadhead", "Sling"], "boons": ["Conceal"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Broadhead", "Conceal", "Sling"])]
        else: abl["specialty"] = [random.choice(["Broadhead", "Conceal", "Sling"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Satyr", element, type, rank)

class ogre:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True
        
        stats["avoidance"] = "low"
        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, dice, {"areas": ["Slip"], "attacks": ["Bash"], "boons": ["Regenerate"]})

        if rank == "Greater": 
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bash", "Disorient", "Slip"])]
        else: abl["specialty"] = [random.choice(["Bash", "Disorient", "Slip"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Ogre", element, type, rank)

class nymph:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, dice, {"boons": ["Wreath"], "hindrances": ["Compel", "Misdirect"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Compel", "Misdirect", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Compel", "Misdirect", "Wreath"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Nymph", element, type, rank)


class bull:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        dice = {"martial": 3, "magic": 0}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Gore", "Kick"], "hindrances": ["Bind"]})

        if rank == "Greater":
            dice["martial"] += 2
            abl["mastery"] = [random.choice(["Bind", "Gore", "Kick"])]
        else: abl["specialty"] = [random.choice(["Bind", "Gore", "Kick"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Bull", element, type, rank)

class obelisk:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["avoidance"] = "min"
        stats["hp"] = "max"
        stats["speed"] = "min"

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bring"], "boons": ["Shroud"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Shroud"])]
        else: abl["specialty"] = [random.choice(["Bring", "Shroud"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Hex"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Obelisk", element, type, rank)

class sphinx:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True

        stats["hp"] = "max"

        dice = {"martial": 2, "magic": 1}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bash", "Claw"], "boons": ["Wreath"]})

        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1
            abl["mastery"] = [random.choice(["Bash", "Claw", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Bash", "Claw", "Wreath"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Sphinx", element, type, rank)


class wisp:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["sapient"] = False
        stats["avoidance"], stats["hp"], stats["speed"] = "max", "low", "max"

        dice = {"martial": 0, "magic": 1}
        abl = Characters.setAbilities(type, dice, {"hindrances": ["Compel", "Misdirect", "Seal"]})

        if rank == "Greater":
            dice["magic"] += 3
            abl["mastery"] = [random.choice(["Compel", "Misdirect", "Seal"])]
        else: abl["specialty"] = [random.choice(["Compel", "Misdirect", "Seal"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Wisp", element, type, rank)



class grotesquery:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        cndt["massive"] = True        
        stats["avoidance"], stats["hp"], stats["speed"]  = "low", "max", "low"

        dice = {"martial": 3, "magic": 0}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bash", "Stab"], "boons": ["Guard"]})

        if rank == "Greater":
            dice["magic"] += 1
            dice["martial"] += 1

        abl["specialty"] = [random.choice(["Bash", "Stab", "Guard"])]
        if rank == "Greater":
            dice["magic"] += 3
            secondSpecialty = [random.choice(["Bash", "Stab", "Guard"])]
            Humans.correctSpecialties(abl, secondSpecialty)

        self.ch = Characters.character(abl, dice, cndt, stats, "Grotesquery", element, type, rank)

class shadow:
    def __init__(self, element, rank) -> None:        
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]
        
        stats["avoidance"] = "max"
        stats["speed"] = "low"

        dice = {"martial": 0, "magic": 3}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Bring"], "hindrances": ["Disorient", "Misdirect"]})
        
        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Bring", "Heal"])]
        else: abl["specialty"] = [random.choice(["Bring", "Heal"])]

        if element == "Holy": abl["areas"] += ["Bless"]
        else: abl["areas"] += ["Hex"]

        self.ch = Characters.character(abl, dice, cndt, stats, "Shadow", element, type, rank)
        
class slime:
    def __init__(self, element, rank) -> None:
        common = setCommon(element, rank)
        stats, cndt, type, rank = common[0], common[1], common[2], common[3]

        stats["avoidance"] = "min"
        stats["speed"] = "low"

        dice = {"martial": 1, "magic": 2}
        abl = Characters.setAbilities(type, dice, {"attacks": ["Pinch"], "boons": ["Wreath"], "hindrances": ["Harry"]})

        if rank == "Greater":
            dice["magic"] += 2
            abl["mastery"] = [random.choice(["Harry", "Pinch", "Wreath"])]
        else: abl["specialty"] = [random.choice(["Harry", "Pinch", "Wreath"])]

        self.ch = Characters.character(abl, dice, cndt, stats, "Slime", element, type, rank)
