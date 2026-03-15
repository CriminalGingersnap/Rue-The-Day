from Systems import Equipment, PlayerSelect as Select
import random, copy


class character:
    def __init__(self, abl, dice, cndt, stats, job, elm, type, inv, rank)-> None:
        self.inventory, self.job, self.rank, self.type = inv, job, rank, type
        self.name = rank + " " + job + "(" + elm + ")"

        self.atrb = setAttributes(rank, stats, cndt, elm, dice)
        self.abl, self.cndt = abl, cndt

        self.equipment = Equipment.setEquipment(type, job, elm, cndt["armored"], cndt)

        dicts = setDicts()
        self.commitments = dicts[0]
        self.effects = dicts[1]
        self.itemEffects = dicts[2]

        self.actionQueue, self.position = [], []
        self.itemUse = 0
        self.skills = {"Tracking": False, "Alchemy": False, "Augury": False}

        self.sightMap = [[], [], [], [], [], [], [], [], [], [], [], []]
        self.initials = job[0] + job[-2]

        Select.waitPrint(self.name + " instantiated!")

     
def setAbilities(type, additions) -> dict:
    abilities = {"areas": [], "attacks": [], "boons": [], "hindrances": [], "items": [], "reactions": [], "specialty": [], "mastery": []}
    abilities.update(additions)
    if (type == "human") and ("Quick Inventory" not in abilities["boons"]): abilities["boons"] += ["Inventory"]

    abilityList = abilities["attacks"] + abilities["boons"] + abilities["hindrances"] + abilities["reactions"]
    if type not in ["human", "elemental"]: abilities["specialty"] = random.choice(abilityList)
    if type == "elemental": abilities["mastery"] = random.choice(abilityList)

    return abilities


def setAttributes(rank, stats, cndt, elm, dice):
    av_range = {"min": 0, "low": random.randint(1,3), "mid": random.randint(4,6), "high": random.randint(7,9), "max": random.randint(10,12)}
    hp_range = {"min": 6, "low": random.randint(9,12), "mid": random.randint(15,18), "high": random.randint(21,24), "max": random.randint(31,36), "boss": 60}
    sp_range = {"min": 0, "low": random.randint(1,3), "mid": random.randint(3,5), "high": random.randint(5,7), "max": random.randint(7,9)}

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
                         "corruption": 0, "fatigue": 0, "injury": 0,
                          "rank": rank}
    
    return attributes


def setTraits():
    conditions = {"aggressive": False, "armored": False, "aquatic": False,
                    "calling": {"delay": 0, "quantity": 0, "used": False},
                     "dead": False, "inviolable": False,
                      "lifeless": False, "massive": False,
                       "reposed": False, "running": False,
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