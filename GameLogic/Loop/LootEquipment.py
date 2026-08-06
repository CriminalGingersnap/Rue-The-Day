from Systems import PlayerSelect as Select, Equipment
import copy


def lootEquipment(players, humans) -> None:
    for player in players:
        compatibleJobs, carryWeight = [], player.atrb["base_sp"] - 1
        armorList, shieldList, weaponList = [], [], []

        if player.inv["standard"] != "None": carryWeight -= 2

        setOptions(player, humans, armorList, shieldList, weaponList, carryWeight, compatibleJobs)
        selectWeapon(player, weaponList, carryWeight)
        selectDefense(player, armorList, shieldList)


def setOptions(player, humans, armorList, shieldList, weaponList, carryWeight, compatibleJobs) -> None:
    if player.equip["armor"]["name"] != "None": armorList += [player.equip["armor"]]
    if player.equip["shield"]["name"] != "None": shieldList += [player.equip["shield"]]
    if player.equip["weapon"]["name"] != "None": weaponList += [player.equip["weapon"]]

    if player.inv["spares"]["shield"]["name"] != "None": shieldList += [player.inv["spares"]["shield"]]
    if player.inv["spares"]["weapon"]["name"] != "None": weaponList += [player.inv["spares"]["weapon"]]

    if player.props["job"] in ["Archer", "Dragonslayer"]: compatibleJobs += ["Archer", "Dragonslayer"]
    elif player.props["job"] in ["Brute", "Knight"]: compatibleJobs += ["Brute", "Knight"]
    else: compatibleJobs += [player.props["job"]]
    
    for enemy in humans:
        if enemy.equip["armor"]["name"] != "None":
            if not (enemy.equip["armor"]["modifier"] > carryWeight): armorList += [enemy.equip["armor"]]
        if enemy.equip["shield"]["name"] != "None":
            if not (enemy.equip["shield"]["modifier"] > carryWeight): shieldList += [enemy.equip["shield"]]
        if enemy.equip["weapon"]["name"] != "None":
            if enemy.props["job"] in compatibleJobs: weaponList += [enemy.equip["weapon"]]


def selectWeapon(player, weaponList, carryWeight) -> None:
    if len(weaponList) == 1:
        player.equip["weapon"] = weaponList[0]
        Select.waitPrint(player.equip["weapon"]["name"] + " selected due to being the only compatible option.")

    elif len(weaponList) > 1:
        nullWeapon = copy.deepcopy(Equipment.nullWeapon)

        player.equip["weapon"] = Select.pickOption(weaponList, "primary weapon")
        weaponList.remove(player.equip["weapon"])
        player.inv["spares"]["weapon"] = Select.pickOption([nullWeapon] + weaponList, "spare weapon")

    carryWeight -= (player.equip["weapon"]["modifier"] + player.inv["spares"]["weapon"]["modifier"])


def selectDefense(player, armorList, shieldList) -> None:
    nullKit = copy.deepcopy(Equipment.nullKit)

    for armor in armorList:
        if armor["element"] != "Dream":
            if armor["modifier"] > carryWeight: armorList.remove[armor]
    if len(armorList) > 0:
        player.equip["armor"] = Select.pickOption([nullKit] + armorList, "armor")

    if player.equip["armor"]["element"] != "Dream":
        carryWeight -= player.equip["armor"]["modifier"]
    
    if player.equip["weapon"]["twoHanded"]: shieldList = []
    else:
        for shield in shieldList:
            if shield["element"] != "Dream":
                if shield["modifier"] > carryWeight: shieldList.remove[shield]

        if len(shieldList) == 0:
            player.equip["shield"] = nullKit
            Select.waitPrint("No usable shields.")
        else:
            player.equip["shield"] = Select.pickOption([nullKit] + shieldList, "primary shield")
            shieldList.remove(player.equip["shield"])
            if len(shieldList) > 0:
                player.inv["spares"]["shield"] = Select.pickOption([nullKit] + shieldList, "spare shield")