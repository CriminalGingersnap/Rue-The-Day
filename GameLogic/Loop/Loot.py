from Systems import PlayerSelect as Select, Inventory
from Actions import ItemActions as Items
from . import LootEquipment
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
    humans, standards, creatures = [], [], []

    for enemy in enemies:
        if enemy.props["type"] == "human": humans += [enemy]
        elif enemy.props["job"] == "standard": standards += [enemy]
        elif enemy.props["rank"] == "Ascendant": continue
        else: creatures += enemy
    
    if len(humans) > 0:
        Select.waitPrint("Searching enemies for useful items.")
        if Select.yesNo("Swap equipment?"): LootEquipment.lootEquipment(players, humans)
    if len(standards) > 0: lootStandards(players, standards)
    if len(creatures) > 0: lootEchos(players, creatures)

    lootSimple(players, humans + standards + creatures)


def lootSimple(players, enemies) -> None:
    Select.waitPrint("Carve and pry open foes which are not human. Rob those which are.")
    stock = getStock(enemies)
    for player in players:
        inventory = Items.getInventory(player)
        allowance = player.inv["Capacity"] - inventory["Total"]

        updateStones(player, stock, allowance)


def lootStandards(players, standards):
    Select.waitPrint("Broken standards can be repaired.")
    for player in players:
        speedLoss = (player.equip["armor"]["modifier"] + player.equip["shield"]["modifier"] + player.equip["weapon"]["modifier"] 
                        + player.inv["spares"]["shield"]["modifier"] + player.inv["spares"]["weapon"]["modifier"])
        carryWeight = player.atrb["base_sp"] - speedLoss

        if carryWeight > 2:
            if Select.yesNo("Equip a new standard to " + player.props["name"] + "?"):
                standard = Select.targetSelect(standards)
                standard.props["rank"] = "player"
                player.inv["standard"] = standard
                standard.cndt["planted"] = False
                
                del standard[standard]


def lootEchos(players, creatures) -> None:
    recentDead = []
    for enemy in creatures:
        if not (enemy.cndt["lifeless"] or (enemy.type in ["insect", "invertebrate"])): recentDead += [enemy]

    if len(recentDead) > 0:
        Select.waitPrint("Echos of the slain linger within their fallen bodies.")
        for player in players:
            if Select.yesNo("Bind a new echo to " + player.props["name"] + "?"):
                echo = Select.targetSelect(recentDead)
                Inventory.setLifeless(echo)
                echo.props["rank"] = "player"
                player.inv["echo"] = echo
                
                del creatures[enemy]
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