from Systems import PlayerSelect as Select, Inventory, Equipment
from Actions import ItemActions as Items
import copy


def searchAll(players, enemies) -> None:
    if Select.yesNo("Reorganize party inventory?"): sortItems(players)
    if Select.yesNo("Loot enemies?"): lootFoes(enemies)


def sortItems(players):
    playerStock = getStock(players)
    for player in players:
        player.inv["cores"] = copy.deepcopy(Inventory.cores)
        player.inv["pearls"] = copy.deepcopy(Inventory.pearls)
        cap = player.inv["Capacity"]

        Select.waitPrint("Items not selected by any party member will be lost.")
        updateStones(player, playerStock, cap)

def updateStones(player, stock, cap):
    phrase = player.props["name"] + " can carry " + cap + " more "
    if cap == 1: Select.waitPrint(phrase + "item.")
    else: Select.waitPrint(phrase + "items.")

    if cap > 0:
        pearlUpdates = Select.listSelection(stock["pearls"], cap, "Assign pearls to " + player.props["name"] + ".")
        for pearl in pearlUpdates:
            player.inv["pearls"][pearl] += 1
            stock.remove(pearl)
            cap -= 1

    if cap > 0:
        coreUpdates = Select.listSelection(stock["cores"], cap, "Assign cores to " + player.props["name"] + ".")
        for core in coreUpdates:
            player.inv["cores"][core] += 1
            stock.remove(core)


def lootFoes(players, enemies):
    humans, nonHumans = [], []

    for enemy in enemies:
        if enemy.props["type"] == "human": humans += [enemy]
        elif enemy.props["rank"] == "Ascendant": continue
        else: nonHumans += enemy
    
    if len(humans) > 0:
        Select.waitPrint("Searching enemies for useful items.")
        if Select.yesNo("Swap equipment?"): lootEquipment(players, humans)
        lootSimple(players, humans)
    if len(nonHumans) > 0:
        lootEchos(players, nonHumans)
        lootSimple(nonHumans)


def lootSimple(players, enemies) -> None:
    stock = getStock(enemies)    
    for player in players:
        inventory = Items.getInventory(player)
        allowance = player.inv["Capacity"] - inventory["Total"]

        updateStones(player, stock, allowance)


def lootEquipment(players, humans) -> None:
    nullKit = copy.deepcopy(Equipment.nullKit)
    nullWeapon = copy.deepcopy(Equipment.nullWeapon)

    for player in players:
        compatibleJobs, carryWeight = [], player.atrb["base_sp"] - 1
        armorList, shieldList, weaponList = [], [], []

        if player.equip["armor"]["name"] != "None": armorList += [player.equip["armor"]]
        if player.equip["shield"]["name"] != "None": shieldList += [player.equip["shield"]]
        if player.equip["weapon"]["name"] != "None": weaponList += [enemy.equip["weapon"]]
        if player.inv["spares"]["shield"]["name"] != "None": shieldList += [player.inv["spares"]["shield"]]
        if player.inv["spares"]["weapon"]["name"] != "None": weaponList += [player.inv["spares"]["weapon"]]

        if player.props["job"] in ["Archer", "Dragonslayer"]: compatibleJobs += ["Archer", "Dragonslayer"]
        elif player.props["job"] in ["Brute", "Knight"]: compatibleJobs += ["Brute", "Knight", "Warlock"]
        elif player.props["job"] in ["Mage", "Warlock"]: compatibleJobs += ["Mage", "Warlock"]
        else: compatibleJobs += [player.props["job"]]

        for enemy in humans:
            if enemy.equip["armor"]["name"] != "None":
                if not (enemy.equip["armor"]["modifier"] > carryWeight): armorList += [enemy.equip["armor"]]
            if enemy.equip["shield"]["name"] != "None":
                if not (enemy.equip["shield"]["modifier"] > carryWeight): shieldList += [enemy.equip["shield"]]
            if enemy.equip["weapon"]["name"] != "None":
                if enemy.props["job"] in compatibleJobs: weaponList += [enemy.equip["weapon"]]
        
        if len(weaponList) == 1:
            player.equip["weapon"] = weaponList[0]
            Select.waitPrint(player.equip["weapon"]["name"] + " selected due to being the only compatible option.")
        elif len(weaponList) > 1:
            player.equip["weapon"] = Select.pickOption(weaponList, "primary weapon")
            weaponList.remove(player.equip["weapon"])
            player.inv["spares"]["weapon"] = Select.pickOption([nullWeapon] + weaponList, "spare weapon")

        carryWeight -= (player.equip["weapon"]["modifier"] + player.inv["spares"]["weapon"]["modifier"])

        for armor in armorList:
            if armor["modifier"] > carryWeight: armorList.remove[armor]
        if len(armorList) > 0: player.equip["armor"] = Select.pickOption([nullKit] + armorList, "armor")
        carryWeight -= player.equip["armor"]["modifier"]
        
        if player.equip["weapon"]["twoHanded"]: shieldList = []
        else:
            for shield in shieldList:
                if shield["modifier"] > carryWeight: shieldList.remove[shield]

            if len(shieldList) == 0:
                player.equip["shield"] = nullKit
                Select.waitPrint("No usable shields.")
            else:
                player.equip["shield"] = Select.pickOption([nullKit] + shieldList, "primary shield")
                shieldList.remove(player.equip["shield"])
                if len(shieldList) > 0:
                    player.inv["spares"]["shield"] = Select.pickOption([nullKit] + shieldList, "spare shield")


def lootEchos(players, nonHumans) -> None:
    recentDead = []
    for enemy in nonHumans:
        if not (enemy.cndt["lifeless"] or (enemy.type in ["insect", "invertebrate"])): recentDead += [enemy]

    if len(recentDead) > 0:
        Select.waitPrint("Echos of the slain linger within their fallen bodies.")            
        for player in players:
            if Select.yesNo("Bind a new echo to " + player.props["name"] + "?"):
                echo = Select.targetSelect(recentDead)
                Inventory.setLifeless(echo)
                echo.props["rank"] = "player"
                player.inv["echo"] = echo
                
                del nonHumans[enemy]
                del recentDead[enemy]


def getStock(party) -> dict:    
    stock = {"cores": [], "pearls": []}

    for fighter in party:
        for pearl in fighter.inv["pearls"]:
            for quantity in range(fighter.inv["pearls"][pearl]): stock["pearls"] += [pearl]
        for core in fighter.inv["cores"]:
            for quantity in range(fighter.inv["cores"][core]): stock["cores"] += [core]

    stock.sort()
    return stock