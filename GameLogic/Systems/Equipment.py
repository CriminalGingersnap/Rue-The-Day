from . import Damage
import random, copy

nullKit = {"name": "None", "modifier": 0,  "element": "Basic"}
nullWeapon = {"name": "None", "modifier": 0, "dmgTypes": [], "reach": 1}

def setEquipment(attacks, cndt, element, job, rank, skills, type) -> list:
    global nullKit, nullWeapon

    equipment = {"armor": copy.deepcopy(nullKit),
                  "shield": copy.deepcopy(nullKit),
                   "weapon": copy.deepcopy(nullWeapon)}

    if type  == "human":
        equipment["weapon"] = setWeapon(job, element, skills)
        equipment["armor"] = setKit(job, False, equipment["weapon"]["modifier"])
        equipment["shield"] = setKit(job, equipment["weapon"]["twoHanded"], equipment["armor"]["modifier"] + equipment["weapon"]["modifier"])
        updateKit(equipment, job, rank)

    else:
        equipment["weapon"]["modifier"] = 1
        equipment["weapon"]["dmgTypes"] = [element]
        for attack in attacks:
            attackDmg = Damage.identifyDamageType(element, attack)
            if attackDmg not in equipment["weapon"]["dmgTypes"]: equipment["weapon"]["dmgTypes"] += [attackDmg]
        if cndt["armored"]: equipment["armor"]["modifier"] = 2
        if cndt["massive"]:
            equipment["weapon"]["reach"] = 2
            equipment["weapon"]["modifier"] = 2
        if type in ["elemental", "totem"]: equipment["weapon"]["reach"] = 8
        if type == "elemental": equipment["weapon"]["modifier"] = 3      

    return equipment


def setKit(job, twoHanded, burden) -> list:
    kit = copy.deepcopy(nullKit)
    options = []

    if twoHanded: kit["name"] = "None"
    else:
        capacity = 3 - burden
        if job in ["Brute", "Knight"]: capacity += 2

        if capacity > 0:
            options += ["Light"]
            if capacity > 1: options += ["Medium"]
            if capacity > 2: options += ["Heavy"]

            kit["name"] = random.choice(options)

            match kit["name"]:
                case "Heavy": kit["modifier"] = 3
                case "Medium": kit["modifier"] = 2
                case "Light": kit["modifier"] = 1

    return kit

def updateKit(equipment, job, rank):    
    if job == "Paladin": equipment["armor"]["element"] = "Holy"
    elif rank in ["Adept", "Elite", "Master"]:
        equipment["armor"]["element"] = random.choice(["Dream", "Flame", "Ice", "Rot"])

        if (not equipment["weapon"]["twoHanded"]) and (equipment["shield"]["name"] == "None"):
            equipment["shield"]["name"] = "Talisman"
            equipment["shield"]["element"] = random.choice(["Dream", "Holy", "Flame", "Ice", "Rot"])


def setWeapon(job, element, skills) -> list:
    longMelee, shortMelee = ["Poleaxe", "Spear", "Staff"], ["Axe", "Mace", "War Pick"]
    bluntMelee, sharpMelee = ["Mace", "Poleaxe", "Staff", "War Pick"], ["Axe", "Poleaxe", "Spear", "War Pick"]

    meleeOptions = []
    if "Bash" in skills: meleeOptions += bluntMelee
    if "Stab" in skills: meleeOptions += sharpMelee
    if not any(meleeSkill in skills for meleeSkill in ["Bash", "Stab"]):
        meleeOptions = bluntMelee + sharpMelee

    weapon = {"name": "", "twoHanded": False, "modifier": 1, "dmgTypes": [], "reach": 1}
    isTwoHanded = random.choice([True, False])

    match job:
        case "Mage":
            elementList = ["Dream", "Flame", "Holy", "Ice", "Rot"]
            weapon.update({"reach": 8, "name": element, "dmgTypes": element})

            if isTwoHanded:
                elementList.remove(element)
                weapon["dmgTypes"] += [random.choice(elementList)]
                weapon["name"] = weapon["dmgTypes"][1] + " " + weapon["name"] + " Banner"
            else: weapon["name"] += " Flag"

        case "Archer" | "Dragonslayer":
            weapon.update({"reach": 8, "twoHanded": True, "dmgTypes": ["Pierce"]})

            if job == "Archer": weapon["name"] = "Long Bow"
            else:
                weapon["name"] = "Pennant Bow"
                weapon["dmgTypes"] += [element]

        case "Brute" | "Knight":
            if isTwoHanded:
                longOptions = list(set(meleeOptions).intersection(longMelee))
                weapon.update({"name": random.choice(longOptions), "reach": 2})
            else:
                shortOptions = list(set(meleeOptions).intersection(shortMelee))
                weapon["name"] = random.choice(shortOptions)

            if weapon["name"] in bluntMelee: weapon["dmgTypes"] += ["Crush"]
            if weapon["name"] in sharpMelee: weapon["dmgTypes"] += ["Pierce"]

        case "Doctor": weapon["name"] = "Bag"

        case "Paladin": weapon.update({"reach": 8, "name": "Sling", "dmgTypes": ["Crush", "Holy"]})

    if weapon["twoHanded"]: weapon["modifier"] += 1
    if any(dmgType in weapon["dmgTypes"] for dmgType in ["Crush", "Pierce"]): weapon["dmgTypes"] += ["Bleed"]

    return weapon