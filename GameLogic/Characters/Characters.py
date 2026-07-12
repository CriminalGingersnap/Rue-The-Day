from Systems import Equipment, PlayerSelect as Select, Inventory
import random, copy


class character:
    def __init__(self, abl, dice, cndt, stats, job, elm, type, rank)-> None:
        self.atrb = setAttributes(stats, cndt, elm, dice)
        self.abl, self.cndt = abl, cndt

        dicts = setDicts()
        self.commits, self.effects, self.itemEffects = dicts[0], dicts[1], dicts[2]

        self.equip = Equipment.setEquipment(type, job, rank, elm, cndt, abl["specialty"] + abl["mastery"], abl["attacks"])
        self.inv = Inventory.setInventory(type, rank, elm, self.atrb["base_hp"])
        name, initials = rank + " " + job + "(" + elm + ")", job[0] + job[-2]
        self.props = {"job": job, "rank": rank, "type": type, "name": name, "initials": initials}

        self.actionQueue, self.position = [], []
        self.sightMap = [[], [], [], [], [], [], [], [], [], [], [], []]

        Select.waitPrint(self.props["name"] + " instantiated!")

     
def setAbilities(type, dice, additions) -> dict:
    abilities = {"areas": [], "attacks": [], "boons": ["Evade"], "hindrances": [], "reactions": [], "specialty": [], "mastery": []}
    
    if dice["martial"] > 0:
        abilities["areas"] += ["Set"]
        if dice["magic"] > 0:
            abilities["areas"] += ["Empower"]
    
    abilities.update(additions)
    if type == "human": abilities["boons"] += ["Inventory"]

    abilityList = abilities["attacks"] + abilities["boons"] + abilities["hindrances"] + abilities["reactions"]
    if type not in ["human", "elemental"]: abilities["specialty"] = [random.choice(abilityList)]
    elif type == "elemental": abilities["mastery"] = [random.choice(abilityList)]

    return abilities


def setAttributes(stats, cndt, elm, dice):
    av_range = {"min": random.randint(1,3), "low": random.randint(3,6), "mid": random.randint(6,9), "high": random.randint(9,12), "max": random.randint(12,15)}
    hp_range = {"min": 6, "low": random.randint(6,12), "mid": random.randint(12,18), "high": random.randint(18,24), "max": random.randint(24,30), "boss": 36}
    sp_range = {"min": 0, "low": random.randint(1,3), "mid": random.randint(4,5), "high": random.randint(5,7), "max": random.randint(7,9)}

    av, hp, sp = av_range[stats["avoidance"]], hp_range[stats["hp"]], sp_range[stats["speed"]]
    halfHealth, quarterHealth = hp // 2, hp // 4
    endurance = random.randint(quarterHealth, halfHealth)
    tolerance = endurance

    if cndt["lifeless"]:
        cndt["aggressive"], cndt["sapient"], cndt["social"] = True, False, False
        stats["resist"]["Bleed"], stats["resist"]["Dream"], stats["resist"]["Venom"] = "immune", "immune", "immune"
        endurance *= 3
    if elm == "Basic": tolerance *= 2

    attributes = {"base_av": av, "cur_av": av,
                   "base_hp": hp, "cur_hp": hp, "half_hp": halfHealth, "quart_hp": quarterHealth,
                    "base_sp": sp, "cur_sp": sp,
                     "base_elm": elm, "cur_elm": elm,
                      "base_mar": dice["martial"], "base_mag": dice["magic"], "cur_mar": dice["martial"], "cur_mag": dice["magic"],
                       "nat_res": copy.deepcopy(stats["resist"]), "cur_res": copy.deepcopy(stats["resist"]),
                        "endurance": endurance, "stamina": endurance, "tolerance": tolerance,
                         "corruption": 0, "fatigue": 0, "injury": 0,}
    
    return attributes


def setTraits():
    conditions = {"aggressive": False, "armored": False, "aquatic": False,
                    "calling": {"delay": 0, "quantity": 0, "used": False},
                     "endowed": False, "summoned": False,
                      "dead": False, "inviolable": False, "lifeless": False,
                       "massive": False, "reposed": False, "running": False,
                        "skittish": False, "social": False, "sapient": False}
    
    resistances = {"Bleed": "normal", "Burn": "normal", "Crush": "normal", "Dream": "normal",
                    "Freeze": "normal", "Holy": "immune", "Pierce": "normal",
                     "Rot": "normal","Venom": "normal"} 

    return [conditions, resistances]


def setDicts():
    commitDict = {"targets": [], "additional": None}
    effectDict = {"dice": 0, "source": None, "ability": None, "additional": None}
    itemDict = {"duration": 0, "potency": 0, "additional": None}

    commitments = {"Compel": copy.deepcopy(commitDict), "Disorient": copy.deepcopy(commitDict),
                    "Focus": copy.deepcopy(commitDict), "Guard": copy.deepcopy(commitDict),
                     "Misdirect": copy.deepcopy(commitDict),
                      "Seal": copy.deepcopy(commitDict), "Shroud": copy.deepcopy(commitDict),
                       "Wreath": copy.deepcopy(commitDict)}

    effects = {"Compel": copy.deepcopy(effectDict), "Disorient": copy.deepcopy(effectDict),
                "Focus": copy.deepcopy(effectDict), "Guard": copy.deepcopy(effectDict),
                 "Misdirect": copy.deepcopy(effectDict), "Seal": copy.deepcopy(effectDict),
                  "Shroud": copy.deepcopy(effectDict), "Wreath": copy.deepcopy(effectDict)}

    itemEffects = {"Animate": copy.deepcopy(itemDict), "Invigorate": copy.deepcopy(itemDict), "Imbue": copy.deepcopy(itemDict)}

    return [commitments, effects, itemEffects]