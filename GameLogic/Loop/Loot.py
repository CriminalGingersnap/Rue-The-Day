from Systems import PlayerSelect as Select, Inventory
from Actions import ItemActions as Items
from . import LootEquipment, LootStones, LootSummons, CombatPhases as Phases
import copy


def searchAll(playersGroup, enemies) -> None:
    groupInv, players = playersGroup["inventory"], playersGroup["members"]
    if Select.yesNo("Reorganize party inventory?"): sortItems(players)
    if Select.yesNo("Loot enemies?"): lootFoes(groupInv, players, enemies)


def sortItems(players):
    playerStock = LootStones.getStock(players)
    standards = ["None"]
    for player in players:
        Select.waitPrint("Assign stones to " + player.props["name"] + ".")
        Select.quickPrint("Items not selected by any party member will be lost.")
        player.inv["cores"] = copy.deepcopy(Inventory.cores)
        player.inv["pearls"] = copy.deepcopy(Inventory.pearls)
        cap = player.inv["Capacity"]
        LootStones.updateStones(player, playerStock, cap)

        standard = player.inv["standard"] 
        if standard != "None": standards += [standard]

    for player in players:
        player.inv["standard"] = "None"
        carryWeight = player.atrb["base_sp"] - Phases.getSpeedLoss(player)

        if (len(standards) > 0) and (carryWeight > 2):
            Select.waitPrint("Assign a standard to " + player.props["name"])
            Select.quickPrint("Items not selected by any party member will be lost.")

            standard = Select.targetSelect(standards)
            player.inv["standard"] = standard
            
            del standard[standard]


def lootFoes(groupInv, players, enemies):
    humans, standards, creatures, boss = [], ["None"], [], None

    for enemy in enemies:
        if enemy.props["type"] == "human": humans += [enemy]
        elif enemy.props["job"] == "standard": standards += [enemy]
        elif enemy.props["rank"] == "Ascendant": boss = enemy
        else: creatures += [enemy]
    
    if len(humans) > 0:
        Select.waitPrint("Searching enemies for useful items.")
        if Select.yesNo("Swap equipment?"): LootEquipment.lootEquipment(players, humans)
    if len(standards) > 1: LootSummons.lootStandards(players, standards)
    if len(creatures) > 0: LootSummons.lootEchos(players, creatures)
    if boss != None: groupInv += [boss.inv["shards"]]

    lootSimple(players, humans + standards + creatures)


def lootSimple(players, enemies) -> None:
    Select.waitPrint("Carve and pry open those foes which are not human. Rob those which are.")
    stock = LootStones.getStock(enemies)
    for player in players:
        inventory = Items.getInventory(player)
        allowance = player.inv["Capacity"] - inventory["Total"]

        LootStones.updateStones(player, stock, allowance)