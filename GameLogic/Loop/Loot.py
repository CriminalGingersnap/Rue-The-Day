from Systems import PlayerSelect as Select, Inventory
from Actions import ItemActions as Items
import copy


def searchAll(players, enemies) -> None:
    if Select.yesNo("Reorganize party inventory?"): sortItems(players)
    if Select.yesNo("Loot enemies?"): lootFoes(enemies)


def sortItems(players):
    playerStock = getStock(players)
    for player in players:
        player.inv["Cores"] = copy.deepcopy(Inventory.cores)
        player.inv["Pearls"] = copy.deepcopy(Inventory.pearls)
        cap = player.inv["Capacity"]

        Select.waitPrint("Items not selected by any party member will be lost.")
        updateStones(player, playerStock, cap)

def updateStones(player, stock, cap):
    phrase = player.props["name"] + " can carry " + cap + " more "
    if cap == 1: Select.waitPrint(phrase + "item.")
    else: Select.waitPrint(phrase + "items.")

    pearlUpdates = Select.listSelection(stock["Pearls"], cap, "Assign pearls to " + player.props["name"] + ".")
    coreUpdates = Select.listSelection(stock["Cores"], cap, "Assign cores to " + player.props["name"] + ".")

    for pearl in pearlUpdates:
        player.inv["Pearls"][pearl] += 1
        stock.remove([pearl])
    for core in coreUpdates:
        player.inv["Cores"][core] += 1
        stock.remove([core])


def lootFoes(players, enemies):
    humans, nonHumans = [], []

    for enemy in enemies:
        if enemy.props["type"] == "human": humans += [enemy]
        elif enemy.props["rank"] == "Boss": continue
        else: nonHumans += enemy
    
    if len(humans) > 0: lootSimple(players, humans)
    if len(nonHumans) > 0:
        lootEchos(players, nonHumans)
        lootSimple(nonHumans)


def lootSimple(players, enemies) -> None:
    stock = getStock(enemies)    
    for player in players:
        inventory = Items.getInventory(player)
        allowance = player.inv["Capacity"] - inventory["Total"]

        updateStones(player, stock, allowance)

def lootEchos(players, nonHumans) -> None:
    if any(player.cndt["endowed"] for player in players):
        recentDead = []
        for enemy in nonHumans:
            if not enemy.cndt["lifeless"]: recentDead += [enemy]

        if len(recentDead) > 0:
            Select.waitPrint("Echos of the slain linger within their fallen bodies.")            
            for player in players:
                if (len(recentDead) > 0) and Select.yesNo("Bind a new echo to " + player.props["name"] + "?"):
                    echo = Select.targetSelect(recentDead)
                    echo.atrb["cur_hp"] = echo.atrb["base_hp"] = echo.atrb["half_hp"]
                    echo.cndt["summoned"], echo.props["rank"] = True, "player"
                    player.inv["Echos"] = echo
                    
                    del nonHumans[enemy]
                    del recentDead[enemy]


def getStock(party) -> dict:    
    stock = {"Cores": [], "Pearls": []}

    for fighter in party:
        for pearl in fighter.inv["Pearls"]:
            for quantity in fighter.inv["Pearls"][pearl]:
                stock["Pearls"] += [pearl]
        for core in fighter.inv["Cores"]:
            for quantity in fighter.inv["Cores"][core]:
                stock["Cores"] += [core]

    stock.sort()
    return stock