from . import Damage, Sort
import random, copy

nullKit = {"name": "None", "modifier": 0,  "element": "Basic", "tier": "Standard"}
nullWeapon = {"name": "None", "modifier": 0, "dmgTypes": [], "reach": 1, "twoHanded": False, "tier": "Standard"}

noviceLong, noviceShort = ["Fishing Spear", "Plank", "Scythe", "Stick"], ["Dagger", "Hand Wrap", "Rock", "Wood Axe"]
noviceBlunt, noviceSharp = ["Hand Wrap", "Plank", "Rock", "Stick"], ["Dagger", "Fishing Spear", "Scythe", "Wood Axe"]
proLong, proShort = ["Spear", "Staff"], ["Axe", "Club", "Mace", "Sword"]
proBlunt, proSharp = ["Club", "Mace", "Staff"], ["Axe", "Spear", "Sword"]


def setEquipment(attacks, cndt, element, job, rank, specialties, type) -> list:
    global nullKit, nullWeapon

    equipment = {"armor": copy.deepcopy(nullKit),
                  "shield": copy.deepcopy(nullKit),
                   "weapon": copy.deepcopy(nullWeapon)}

    if type  == "human":
        equipment["weapon"] = setWeapon(job, element, rank, specialties)
        equipment["armor"] = setKit(job, False, equipment["weapon"]["modifier"])
        equipment["shield"] = setKit(job, equipment["weapon"]["twoHanded"], equipment["armor"]["modifier"] + equipment["weapon"]["modifier"])
        updateKit(equipment, job, rank)

    else:
        equipment["weapon"]["modifier"], equipment["weapon"]["dmgTypes"] = 1, [element]

        if cndt["armored"]: equipment["armor"]["modifier"] = 2
        if cndt["massive"]: equipment["weapon"]["reach"] = equipment["weapon"]["modifier"] = 2
        if type == "elemental": equipment["weapon"]["reach"], equipment["weapon"]["modifier"] = 8, 3

        for attack in attacks:
            attackDmg = Damage.identifyDamageType(element, attack)
            if attackDmg not in equipment["weapon"]["dmgTypes"]: equipment["weapon"]["dmgTypes"] += [attackDmg]

    return equipment


def setKit(job, twoHanded, burden) -> list:
    kit = copy.deepcopy(nullKit)
    options = []

    if twoHanded: kit["name"] = "None"
    else:
        capacity = 3 - burden
        if job in ["Brute", "Knight"]: capacity += 1

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
        equipment["armor"]["tier"] = random.choice(["Standard", "Standard", "Standard", "Standard", "Standard", "Masterwork"])
        equipment["weapon"]["tier"] = random.choice(["Standard", "Standard", "Standard", "Standard", "Standard", "Masterwork"])
        
        if equipment["shield"]["name"] != "None": equipment["shield"]["element"] = "Dream"
        elif not equipment["weapon"]["twoHanded"]:
            equipment["shield"]["name"] = "Talisman"
            equipment["shield"]["element"] = random.choice(["Holy", "Flame", "Ice", "Rot"])
            equipment["shield"]["tier"] = random.choice(["Standard", "Standard", "Standard", "Standard", "Standard", "Masterwork"])

        for tool in [equipment["armor"], equipment["shield"], equipment["weapon"]]:
            if tool["tier"] == "Masterwork": tool["modifier"] *= 2


def setWeapon(job, element, rank, specialties) -> list:
    weapon = copy.deepcopy(nullWeapon)
    weapon["twoHanded"] = random.choice([True, False])

    match job:
        case "Mage" | "Witch":
            weapon.update({"reach": 8, "dmgTypes": [element]})

            if weapon["twoHanded"]:
                if rank == "Novice": weapon["name"] = "Rag on Stick"
                else: weapon["name"] = "Banner"
            else:
                if rank == "Novice": weapon["name"] = "Rag"
                else: weapon["name"] = "Flag"

        case "Archer" | "Dragonslayer":
            weapon.update({"reach": 8, "twoHanded": True, "dmgTypes": ["Pierce"]})

            if rank == "Novice": weapon["name"] = "Training Bow"
            elif job == "Archer": weapon["name"] = "Long Bow"
            else:
                weapon["name"] = "Pennant Bow"
                weapon["dmgTypes"] += [element]

        case "Brute" | "Knight":
            longMelee, shortMelee, bluntMelee, sharpMelee = [], [], [], []

            if rank == "Novice":
                longMelee, shortMelee = noviceLong, noviceShort
                bluntMelee, sharpMelee = noviceBlunt, noviceSharp
            else:
                longMelee, shortMelee = proLong, proShort
                bluntMelee, sharpMelee = proBlunt, proSharp

            meleeOptions = []
            if "Bash" in specialties: meleeOptions += bluntMelee
            elif "Stab" in specialties: meleeOptions += sharpMelee
            else: meleeOptions = bluntMelee + sharpMelee

            if weapon["twoHanded"]:
                longOptions = list(set(meleeOptions).intersection(longMelee))
                weapon.update({"name": random.choice(longOptions), "reach": 2})
            else:
                shortOptions = list(set(meleeOptions).intersection(shortMelee))
                weapon["name"] = random.choice(shortOptions)

            if weapon["name"] in bluntMelee: weapon["dmgTypes"] += ["Crush"]
            if weapon["name"] in sharpMelee: weapon["dmgTypes"] += ["Pierce"]

        case "Doctor": weapon["name"] = "Bag"

        case "Paladin": weapon.update({"reach": 8, "name": "Sling", "dmgTypes": ["Crush"]})

    if rank == "Novice": weapon["modifier"], weapon["tier"] = 0, "Junk"
    elif weapon["twoHanded"]: weapon["modifier"] += 1

    return weapon