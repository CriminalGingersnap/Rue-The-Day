from Systems import PlayerSelect as Select, Equipment
from Loop import CombatPhases as Phases
import copy


def lootEquipment(players, humans) -> None:
    armorList, shieldList, weaponList = [], [], []
    setOptions(players + humans, armorList, shieldList, weaponList)

    for player in players:
        carryWeight = player.atrb["base_sp"] - 1
        if player.inv["standard"] != "None": carryWeight -= 2
        
        compatibleWeapons = []
        if player.props["job"] in ["Archer", "Dragonslayer"]: compatibleWeapons = ["Training-Bow", "Long-Bow", "Pennant-Bow"]
        elif player.props["job"] in ["Brute", "Knight"]: compatibleWeapons = Equipment.noviceBlunt + Equipment.noviceSharp + Equipment.proSharp + Equipment.proBlunt
        elif player.props["job"] in ["Mage", "Witch"]: compatibleWeapons = ["Banner", "Flag", "Rag-on-Stick", "Rag"]
        elif player.props["job"] == "Paladin": compatibleWeapons = ["Sling"]
        elif player.props["job"] == "Doctor": compatibleWeapons = ["Bag"]

        carryWeight = selectWeapon(player, weaponList, carryWeight, compatibleWeapons)
        selectDefense(player, armorList, shieldList, carryWeight)

def setOptions(humans, armorList, shieldList, weaponList) -> None:    
    for human in humans:
        if human.equip["armor"]["name"] != "None": armorList += [setKitName(human.equip["armor"])]
        if human.equip["shield"]["name"] != "None": shieldList += [setKitName(human.equip["shield"])]
        if human.equip["weapon"]["name"] != "None": weaponList += [setWeaponName(human.equip["weapon"])]

        if human.inv["spares"]["weapon"]["name"] != "None": weaponList += [setWeaponName(human.inv["spares"]["weapon"])]
        if human.inv["spares"]["shield"]["name"] != "None": shieldList += [setKitName(human.inv["spares"]["shield"])]


def selectWeapon(player, weaponList, carryWeight, compatibleWeapons) -> int:
    weaponOptions = [weapon for weapon in weaponList if any(compatibleNames in weapon for compatibleNames in compatibleWeapons)]

    if (len(weaponOptions) == 0): Select.clearPrint("No compatible weapons are available for " + player.props["name"] + ".")

    elif len(weaponOptions) > 1:
        weaponChoice = Select.pickOption(weaponOptions, player.props["name"] + "'s primary weapon")
        updateWeapon(player, "equipment", weaponChoice)
        weaponOptions.remove(setWeaponName(player.equip["weapon"]))
        weaponList.remove(setWeaponName(player.equip["weapon"]))

        if len(weaponOptions) > 1:
            weaponChoice = Select.pickOption(["None"] + weaponOptions, player.props["name"] + "'s spare weapon")
            updateWeapon(player, "inventory", weaponChoice)

    return carryWeight - (Phases.getEquipLoad(player.equip["weapon"]) + Phases.getEquipLoad(player.inv["spares"]["weapon"]))


def selectDefense(player, armorList, shieldList, carryWeight) -> None:
    for armor in armorList:
        updateKit(player, "equipment", armor, "armor")
        if Phases.getEquipLoad(player.equip["armor"]) > carryWeight: armorList.remove(armor)
    if len(armorList) > 0:
        armorChoice = Select.pickOption(["None"] + armorList, player.props["name"] + "'s armor")
        updateKit(player, "equipment", armorChoice, "armor")
        carryWeight -= Phases.getEquipLoad(player.equip["armor"])
    
    for shield in shieldList:
        updateKit(player, "equipment", shield, "shield")
        if Phases.getEquipLoad(player.equip["shield"]) > carryWeight: shieldList.remove(shield)

    if len(shieldList) == 0:
        Select.clearPrint("No usable shields are available for " + player.props["name"] + ".")
        updateKit(player, "equipment", "None", "shield")
    else:
        if not player.equip["weapon"]["twoHanded"]:
            shieldChoice = Select.pickOption(["None"] + shieldList, player.props["name"] + "'s primary shield")
            updateKit(player, "equipment", shieldChoice, "shield")

            if shieldChoice != "None":
                carryWeight -= Phases.getEquipLoad(player.equip["shield"])
                shieldList.remove(setKitName(player.equip["shield"]))

        if len(shieldList) > 0:
            spareChoice = Select.pickOption(["None"] + shieldList, player.props["name"] + "'s spare shield")
            updateKit(player, "inventory", spareChoice, "shield")


def updateKit(player, storage, kitChoice, kitType):
    kit = copy.deepcopy(Equipment.nullKit)

    if kitChoice != "None":
        kit["tier"] = kitChoice.split(" ")[0]
        kit["name"] = kitChoice.split(" ")[1].split(":")[0]
        kit["element"] = kitChoice.split(": ")[1]

        match kit["name"]:
            case "Heavy": kit["modifier"] = 3
            case "Medium": kit["modifier"] = 2
            case "Light": kit["modifier"] = 1

        if kit["tier"] == "Masterwork": kit["modifier"] *= 2

    match storage:
        case "equipment": player.equip[kitType] = kit
        case "inventory": player.inv["spares"][kitType] = kit


def updateWeapon(player, storage, weaponChoice):
    weapon = copy.deepcopy(Equipment.nullWeapon)

    if weaponChoice != "None":
        weapon["tier"] = weaponChoice.split(" ")[0]
        weapon["name"] = weaponChoice.split(" ")[1].split(":")[0]
        weapon["dmgTypes"] = [weaponChoice.split(": ")[1]]

        if any(twoHanded in weaponChoice for twoHanded in ["Banner", "Long-Bow", "Pennant-Bow"] + Equipment.proLong):
            weapon["modifier"] = 2
            weapon["twoHanded"] = True
        elif any(oneHanded in weaponChoice for oneHanded in ["Bag", "Flag", "Sling"] + Equipment.proShort):
            weapon["modifier"] = 1
        else:
            weapon["modifier"] = 0
            if any(twoHanded in weaponChoice for twoHanded in ["Rag-on-Stick", "Training-Bow"] + Equipment.noviceLong):
                weapon["twoHanded"] = True

        if weapon["tier"] == "Masterwork": weapon["modifier"] *= 2

    match storage:
        case "equipment": player.equip["weapon"] = weapon
        case "inventory": player.inv["spares"]["weapon"] = weapon


def setKitName(kit) -> str: return kit["tier"] + " " + kit["name"] + ": " + kit["element"]
def setWeaponName(weapon) -> str: return weapon["tier"] + " " + weapon["name"] + ": " + weapon["dmgTypes"][0]