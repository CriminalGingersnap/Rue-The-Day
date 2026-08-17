from Systems import PlayerSelect as Select, Equipment
from Loop import CombatPhases as Phases
import copy


def lootEquipment(players, humans) -> None:
    for player in players:
        compatibleJobs, carryWeight = [], player.atrb["base_sp"] - 1
        armorList, shieldList, weaponList = [], [], []

        if player.inv["standard"] != "None": carryWeight -= 2

        setOptions(player, humans, armorList, shieldList, weaponList, carryWeight, compatibleJobs)
        carryWeight = selectWeapon(player, weaponList, carryWeight)
        selectDefense(player, armorList, shieldList, carryWeight)


def setOptions(player, humans, armorList, shieldList, weaponList, carryWeight, compatibleJobs) -> None:
    if player.equip["armor"]["name"] != "None":
        armorList += [player.equip["armor"]["tier"] + " " + player.equip["armor"]["name"] + " " + player.equip["armor"]["element"]]
    if player.equip["shield"]["name"] != "None":
        shieldList += [player.equip["shield"]["tier"] + " " + player.equip["shield"]["name"] + " " + player.equip["shield"]["element"]]
    if player.equip["weapon"]["name"] != "None":
        weaponList += [player.equip["weapon"]["tier"] + " " + player.equip["weapon"]["dmgTypes"][0] + " " + player.equip["weapon"]["name"]]

    if player.inv["spares"]["shield"]["name"] != "None":
        shieldList += [player.inv["spares"]["shield"]["tier"] + " " + player.inv["spares"]["shield"]["name"] + " " + player.inv["spares"]["shield"]["element"]]
    if player.inv["spares"]["weapon"]["name"] != "None":
        weaponList += [player.inv["spares"]["weapon"]["tier"] + " " + player.inv["spares"]["weapon"]["dmgTypes"][0] + " " + player.inv["spares"]["weapon"]["name"]]

    if player.props["job"] in ["Archer", "Dragonslayer"]: compatibleJobs += ["Archer", "Dragonslayer"]
    elif player.props["job"] in ["Brute", "Knight"]: compatibleJobs += ["Brute", "Knight"]
    elif player.props["job"] in ["Mage", "Witch"]: compatibleJobs += ["Mage", "Witch"]
    else: compatibleJobs += [player.props["job"]]
    
    for enemy in humans:
        if (enemy.equip["armor"]["name"] != "None") and not (Phases.getEquipLoad(enemy.equip["armor"]) > carryWeight):
            armorList += [enemy.equip["armor"]["tier"] + " " + enemy.equip["armor"]["name"] + " " + enemy.equip["armor"]["element"]]
        if (enemy.equip["shield"]["name"] != "None") and not (Phases.getEquipLoad(enemy.equip["shield"]) > carryWeight):
            shieldList += [enemy.equip["shield"]["tier"] + " " + enemy.equip["shield"]["name"] + " " + enemy.equip["shield"]["element"]]
        if (enemy.equip["weapon"]["name"] != "None") and (enemy.props["job"] in compatibleJobs):
            weaponList += [enemy.equip["weapon"]["tier"] + " " + enemy.equip["weapon"]["dmgTypes"][0] + " " + enemy.equip["weapon"]["name"]]


def selectWeapon(player, weaponList, carryWeight) -> int:
    if len(weaponList) == 1:
        updateWeapon(player, "inventory", weaponList[0])
        weaponName = player.equip["weapon"]["tier"] + " " + player.equip["weapon"]["dmgTypes"][0] + " " + player.equip["weapon"]["name"]
        Select.clearPrint(weaponName + " selected for " + player.props["name"] + " due to being the only compatible option.")

    elif len(weaponList) > 1:
        weaponChoice = Select.pickOption(weaponList, player.props["name"] + "'s primary weapon")
        updateWeapon(player, "equipment", weaponChoice)

        weaponList.remove(player.equip["weapon"])
        if len(weaponList) > 1:
            weaponChoice = Select.pickOption(["None"] + weaponList, player.props["name"] + "'s spare weapon")
            updateWeapon(player, "inventory", weaponChoice)

    return carryWeight - (Phases.getEquipLoad(player.equip["weapon"]) + Phases.getEquipLoad(player.inv["spares"]["weapon"]))


def selectDefense(player, armorList, shieldList, carryWeight) -> None:
    for armor in armorList:
        if Phases.getEquipLoad(armor) > carryWeight: armorList.remove[armor]
    if len(armorList) > 0:
        armorChoice = Select.pickOption(["None"] + armorList, player.props["name"] + "'s armor")
        updateKit(player, "equipment", armorChoice, "armor")
        carryWeight -= Phases.getEquipLoad(player.equip["armor"])
    
    if player.equip["weapon"]["twoHanded"]: shieldList = []
    else:
        for shield in shieldList:
            if Phases.getEquipLoad(shield) > carryWeight: shieldList.remove[shield]

    if len(shieldList) == 0:
        Select.clearPrint("No usable shields.")
        updateKit(player, "equipment", "None", "shield")
    else:
        shieldChoice = Select.pickOption(["None"] + shieldList, player.props["name"] + "'s primary shield")
        updateKit(player, "equipment", shieldChoice, "shield")
                
        shieldList.remove(player.equip["shield"])
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
        kit["element"] = kitChoice.split(" ")[2]

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
        weapon["dmgTypes"] = [weaponChoice.split(" ")[1]]
        weapon["name"] = weaponChoice.split(" ")[2]

        if any(twoHanded in weaponChoice for twoHanded in ["Banner", "Long Bow", "Pennant Bow"] + Equipment.proLong):
            weapon["modifier"] = 2
        elif any(oneHanded in weaponChoice for oneHanded in ["Bag", "Flag", "Sling"] + Equipment.proShort):
            weapon["modifier"] = 1
        else: weapon["modifier"] = 0

        if weapon["tier"] == "Masterwork": weapon["modifier"] *= 2
