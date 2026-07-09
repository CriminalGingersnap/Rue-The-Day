from Abilities import DamageTypes as Damage
import random

# talismans absorb a set amount of elemental damage before being destroyed.

def setEquipment(type, job, rank, element, cndt, skills) -> list:
    equipment = {"armor": {"name": None, "modifier": 0, "element": "Basic"},
                  "shield": {"name": None, "modifier": 0},
                   "weapon": {"name": None, "modifier": 0, "reach": 1}}

    if type  == "human":
        equipment["armor"] = setKit(job, False, 0)
        equipment["weapon"] = setWeapon(job, element, skills)
        equipment["shield"] = setKit(job, equipment["weapon"]["twoHanded"], equipment["armor"]["modifier"])

        if job == "Paladin": equipment["armor"]["element"] = "Blessed"
        elif rank in ["Elite", "Master"]:
            equipment["armor"]["element"] = random.choice(["Flame", "Fey", "Ice", "Toxin"])

    elif type in ["elemental", "totem"]:
        equipment["weapon"]["reach"] = 8
    else:
        if cndt["armored"]: equipment["armor"] = {"modifier": 2}
        if cndt["massive"]: equipment["weapon"]["reach"] = 2

    return equipment


def setKit(job, twoHanded, burden) -> list:
    kit = {"name": "", "modifier": 0, "element": "Basic"}
    options = []

    if twoHanded:
        kit["name"] = None
    else:
        capacity = 2 - burden
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

def setWeapon(job, element, skills) -> list:
    longMelee, shortMelee = ["Poleaxe", "Spear", "Staff"], ["Axe", "Mace", "War Pick"]
    bluntMelee, sharpMelee = ["Mace", "Poleaxe", "Staff", "War Pick"], ["Axe", "Poleaxe", "Spear", "War Pick"]
    elementList = ["Ice", "Flame", "Fey", "Corpse", "Blessed"]

    weapon = {"name": "", "twoHanded": False, "modifier": 1, "dmgTypes": [], "reach": 1}

    isTwoHanded = random.choice([True, False])
    weapon["twoHanded"] = isTwoHanded
    if isTwoHanded: weapon["modifier"] += 1

    if job == "Mage":
        weapon["reach"], weapon["name"] = 8, element
        weaponElements = [element]
        elementList.remove(element)

        if isTwoHanded: weaponElements += [random.choice(elementList)]

        for elm in weaponElements:
            dmgType = Damage.convertElmToDmg(elm)
            weapon["dmgTypes"] += [dmgType]

        if isTwoHanded: weapon["name"] = weapon["dmgTypes"][1] + " " + weapon["name"] + " Banner"
        else: weapon["name"] += " Flag"
    
    elif job in ["Brute", "Knight"]:
        if isTwoHanded:
            weapon["name"] = random.choice(longMelee)
            weapon["reach"] = 2
        else: weapon["name"] = random.choice(shortMelee)

        if weapon["name"] in bluntMelee: weapon["dmgTypes"] += ["Crush"]
        if weapon["name"] in sharpMelee: weapon["dmgTypes"] += ["Pierce"]
    
    elif job == "Archer":
        weapon["reach"] = 8
        weapon["twoHanded"] = True
        weapon["name"] = "Bow"
        weapon["dmgTypes"] += ["Pierce"]
        
    elif job == "Dragonslayer":
        weapon["reach"] = 8
        weapon["twoHanded"] = True
        weapon["name"] = "Pennant Bow"
        weapon["dmgTypes"] += ["Pierce", element]

    elif job == "Paladin":
        weapon["reach"] = 8
        weapon["twoHanded"] = False
        weapon["name"] = "Sling"
        weapon["dmgTypes"] += ["Crush", "Holy"]

    elif job == "Warlock":
        weaponName = random.choice(longMelee)
        if weaponName in bluntMelee: weapon["dmgTypes"] += ["Crush"]
        if weaponName in sharpMelee: weapon["dmgTypes"] += ["Pierce"]
        weapon["name"] = "Pennant" + weaponName

        weapon["reach"] = 8
        weapon["twoHanded"] = True
        weapon["dmgTypes"] += [element]

    return weapon