from Abilities import DamageTypes as Damage
import random

# talismans absorb a set amount of elemental damage before being destroyed.

def setEquipment(type, job, element, natArmor, cndt) -> list:
    equipment = {"weapon": {"name": None, "modifier": 0, "reach": 1},
                  "armor": {"name": None, "modifier": 0},
                   "shield": {"name": None, "modifier": 0}}

    if type  == "human":
        equipment["armor"] = setKit(job, False, 0)
        equipment["weapon"] = setWeapon(job, element)
        equipment["shield"] = setKit(job, equipment["weapon"]["twoHanded"], equipment["armor"]["modifier"])
    elif type in ["elemental", "totem"]:
        equipment["weapon"]["reach"] = 12
    else:
        if natArmor: equipment["armor"] = {"modifier": 2}
        if cndt["massive"]: equipment["weapon"]["reach"] = 2

    return equipment


def setKit(job, twoHanded, burden) -> list:
    kit = {"name": "", "modifier": 0}
    options = []

    if twoHanded:
        kit["name"] = None
    else:
        capacity = 2 - burden
        if job == "Knight": capacity += 2

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

def setWeapon(job, element) -> list:
    weapon = {"name": "", "twoHanded": False, "modifier": 1, "dmgTypes": [], "reach": 1}

    isTwoHanded = random.choice([True, False])
    weapon["twoHanded"] = isTwoHanded
    if isTwoHanded: weapon["modifier"] += 1

    if job == "Mage":
        weapon["reach"], weapon["name"] = 10, element
        weaponElements, elementList = [element], ["Ice", "Flame", "Fey", "Corpse", "Blessed"]
        elementList.remove(element)

        if isTwoHanded: weaponElements += [random.choice(elementList)]

        for elm in weaponElements:
            dmgType = Damage.convertElmToDmg(elm)
            weapon["dmgTypes"] += [dmgType]

        if isTwoHanded: weapon["name"] = weapon["dmgTypes"][1] + " " + weapon["name"] + " Banner"
        else: weapon["name"] += " Flag"
    
    elif job in ["Brute", "Knight", "Warlock"]:
        longMelee, shortMelee = ["Poleaxe", "Spear", "Staff"], ["Axe", "Mace", "War Pick"]
        bluntMelee, sharpMelee = ["Mace", "Poleaxe", "Staff", "War Pick"], ["Axe", "Poleaxe", "Spear", "War Pick"]

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

    return weapon