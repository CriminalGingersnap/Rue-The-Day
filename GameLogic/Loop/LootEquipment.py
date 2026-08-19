from Systems import PlayerSelect as Select, Equipment
from Loop import CombatPhases as Phases
import copy


def lootEquipment(players, humans) -> None:
    armorList, shieldList, weaponList = [], [], []
    setOptions(players + humans, armorList, shieldList, weaponList)

    for player in players:
        carryWeight = player.atrb["base_sp"] - 1
        if player.inv["standard"] != "None": carryWeight -= 2

        compatibleJobs = []
        if player.props["job"] in ["Archer", "Dragonslayer"]: compatibleJobs += ["Archer", "Dragonslayer"]
        elif player.props["job"] in ["Brute", "Knight"]: compatibleJobs += ["Brute", "Knight"]
        elif player.props["job"] in ["Mage", "Witch"]: compatibleJobs += ["Mage", "Witch"]
        else: compatibleJobs += [player.props["job"]]

        carryWeight = selectWeapon(player, weaponList, carryWeight)
        selectDefense(player, armorList, shieldList, carryWeight)

def setOptions(humans, armorList, shieldList, weaponList) -> None:    
    for human in humans:
        if human.equip["armor"]["name"] != "None": armorList += [setKitName(human.equip["armor"])]
        if human.equip["shield"]["name"] != "None": shieldList += [setKitName(human.equip["shield"])]
        if human.equip["weapon"]["name"] != "None": weaponList += [setWeaponName(human.equip["weapon"])]

        if human.inv["spares"]["shield"]["name"] != "None": shieldList += [setKitName(human.inv["spares"]["shield"])]
        if human.inv["spares"]["weapon"]["name"] != "None": weaponList += [setWeaponName(human.inv["spares"]["weapon"])]


def selectWeapon(player, weaponList, carryWeight) -> int:
    if len(weaponList) == 1:
        updateWeapon(player, "inventory", weaponList[0])
        weaponName = player.equip["weapon"]["tier"] + " " + player.equip["weapon"]["dmgTypes"][0] + " " + player.equip["weapon"]["name"]
        Select.clearPrint(weaponName + " selected for " + player.props["name"] + " due to being the only compatible option.")

    elif len(weaponList) > 1:
        weaponChoice = Select.pickOption(weaponList, player.props["name"] + "'s primary weapon")
        updateWeapon(player, "equipment", weaponChoice)
        weaponList.remove(setWeaponName(player.equip["weapon"]))

        if len(weaponList) > 1:
            weaponChoice = Select.pickOption(["None"] + weaponList, player.props["name"] + "'s spare weapon")
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
        Select.clearPrint("No usable shields.")
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
    kit = None
    match storage:
        case "equipment": kit = player.equip[kitType]
        case "inventory": kit = player.inv["spares"][kitType]

    if kitChoice == "None": kit = copy.deepcopy(Equipment.nullKit)
    else:
        kit["tier"] = kitChoice.split(" ")[0]
        kit["name"] = kitChoice.split(" ")[1]
        kit["element"] = kitChoice.split(": ")[1]

        match kit["name"]:
            case "Heavy": kit["modifier"] = 3
            case "Medium": kit["modifier"] = 2
            case "Light": kit["modifier"] = 1

        if kit["tier"] == "Masterwork": kit["modifier"] *= 2


def updateWeapon(player, storage, weaponChoice):
    weapon = None
    match storage:
        case "equipment": weapon = player.equip["weapon"]
        case "inventory": weapon = player.inv["spares"]["weapon"]

    if weaponChoice == "None": weapon = copy.deepcopy(Equipment.nullWeapon)
    else:
        weapon["tier"] = weaponChoice.split(" ")[0]
        weapon["name"] = weaponChoice.split(" ")[1]
        weapon["dmgTypes"] = [weaponChoice.split(": ")[1]]

        if any(twoHanded in weaponChoice for twoHanded in ["Banner", "Long Bow", "Pennant Bow"] + Equipment.proLong):
            weapon["modifier"] = 2
        elif any(oneHanded in weaponChoice for oneHanded in ["Bag", "Flag", "Sling"] + Equipment.proShort):
            weapon["modifier"] = 1
        else: weapon["modifier"] = 0

        if weapon["tier"] == "Masterwork": weapon["modifier"] *= 2


def setKitName(kit) -> str: return kit["tier"] + " " + kit["name"] + ": " + kit["element"]
def setWeaponName(weapon) -> str: return weapon["tier"] + " " + weapon["name"] + ": " + weapon["dmgTypes"][0]