from Systems import Equipment, PlayerSelect as Select, Inventory
import random, copy


class character:
    def __init__(self, abl, cndt, dice, elm, job, rank, stats, type)-> None:
        self.atrb = setAttributes(stats, cndt, elm, dice, type)
        self.abl, self.cndt = abl, cndt

        dicts = setDicts()
        self.commits, self.effects, self.itemEffects = dicts[0], dicts[1], dicts[2]

        self.equip = Equipment.setEquipment(abl["attacks"], cndt, elm, job, rank, abl["specialty"] + abl["mastery"], type)
        self.inv = Inventory.setInventory(elm, self.atrb["base_hp"], job, rank, type)

        favored = ""
        if type in ["elemental", "totem"]: favored = "human"
        else:
            types = ["beast", "bird", "insect", "invertebrate", "reptile"]
            if cndt["sapient"]: types += ["elemental", "human", "totem"]
            favored = random.choice(types)

        name = rank + " " + job
        self.props = {"favored": favored, "initials": "", "job": job, "name": name, "rank": rank, "type": type}

        self.attackQueue, self.pos = [], []
        self.sightMap = [[], [], [], [], [], [], [], [], [], [], [], []]

        Select.quickPrint(self.props["name"] + " instantiated!")

     
def setAbilities(type, additions) -> dict:
    abilities = {"areas": [], "attacks": [], "boons": [], "hindrances": [], "reactions": [], "specialty": [], "mastery": []}
    
    abilities.update(additions)
    if type == "human": abilities["areas"] += ["Inventory"]

    abilityList = abilities["areas"] + abilities["attacks"] + abilities["boons"] + abilities["hindrances"]
    if type not in ["human", "elemental"]: abilities["specialty"] = [random.choice(abilityList)]

    return abilities


def setAttributes(stats, cndt, elm, dice, type):
    av_range = {"min": random.randint(1,3), "low": random.randint(4,6), "mid": random.randint(7,9), "high": random.randint(10,12), "max": random.randint(13,15)}
    hp_range = {"min": 6, "low": random.randint(7,12), "mid": random.randint(13,18), "high": random.randint(19,24), "max": random.randint(25,30), "boss": 36}
    sp_range = {"min": 0, "low": random.randint(2,3), "mid": random.randint(4,5), "high": random.randint(6,7), "max": random.randint(8,9)}

    av, hp, sp = av_range[stats["avoidance"]], hp_range[stats["hp"]], sp_range[stats["speed"]]
    halfHealth, quarterHealth = hp // 2, hp // 4
    endurance = halfHealth
    corruption, fatigue, injury = 0, random.choice([0, 0, 1]), random.choice([0, 0, 0, 0, 0, 1])

    if cndt["lifeless"]:
        cndt["skittish"] = False
        if type != "totem": cndt["social"] = False
        stats["resist"].update({"Bleed": "immune", "Dream": "immune", "Holy": "normal", "Toxic": "immune"})
        endurance *= 3
    elif type == "human": corruption = random.choice([0, 0, 0, 0, 0, 1])

    attributes = {"base_av": av, "cur_av": av,
                   "base_hp": hp, "cur_hp": hp, "half_hp": halfHealth, "quart_hp": quarterHealth,
                    "base_sp": sp, "cur_sp": sp,
                     "base_elm": elm, "cur_elm": elm,
                      "base_mar": dice["martial"], "base_mag": dice["magic"], "cur_mar": dice["martial"], "cur_mag": dice["magic"],
                       "nat_res": copy.deepcopy(stats["resist"]), "cur_res": copy.deepcopy(stats["resist"]),
                        "endurance": endurance, "stamina": endurance, "tolerance": endurance,
                         "corruption": corruption, "fatigue": fatigue, "injury": injury}
    
    return attributes


def setTraits():
    conditions = {"armored": False, "aquatic": False, "blitzing": False,
                    "dead": False, "inviolable": False, "lifeless": False,
                     "massive": False, "planted": False,
                      "reposed": False, "running": False,
                       "skittish": False, "social": False,
                        "sapient": False, "submerged": False,
                         "winged": False}
    
    resistances = {"Bleed": "normal", "Flame": "normal", "Crush": "normal",
                    "Dream": "normal", "Ice": "normal", "Holy": "immune",
                     "Pierce": "normal", "Rot": "normal", "Toxic": "normal"} 

    return [conditions, resistances]


def setDicts():
    commitDict = {"targets": [], "additional": None}
    effectDict = {"dice": 0, "source": None, "ability": None, "additional": None}
    itemDict = {"duration": 0, "potency": 0, "additional": None}

    commitments = {"Compel": copy.deepcopy(commitDict), "Confound": copy.deepcopy(commitDict),
                    "Drain": copy.deepcopy(commitDict),
                     "Focus": copy.deepcopy(commitDict), "Fortify": copy.deepcopy(commitDict),
                      "Guard": copy.deepcopy(commitDict), "Heal": copy.deepcopy(commitDict),
                       "Rally": copy.deepcopy(commitDict),
                        "Stun": copy.deepcopy(commitDict), "Seal": copy.deepcopy(commitDict),
                         "Veil": copy.deepcopy(commitDict), "Wreath": copy.deepcopy(commitDict)}

    effects = {"Compel": copy.deepcopy(effectDict), "Confound": copy.deepcopy(effectDict),
                "Drain": copy.deepcopy(effectDict),
                 "Focus": copy.deepcopy(effectDict), "Fortify": copy.deepcopy(effectDict),
                  "Guard": copy.deepcopy(effectDict), "Heal": copy.deepcopy(effectDict),
                   "Rally": copy.deepcopy(effectDict),
                    "Stun": copy.deepcopy(effectDict), "Seal": copy.deepcopy(effectDict),
                     "Veil": copy.deepcopy(effectDict), "Wreath": copy.deepcopy(effectDict)}

    itemEffects = {"Animate": copy.deepcopy(itemDict), "Invigorate": copy.deepcopy(itemDict),
                    "Imbue": copy.deepcopy(itemDict), "Obscure": copy.deepcopy(itemDict)}

    return [commitments, effects, itemEffects]