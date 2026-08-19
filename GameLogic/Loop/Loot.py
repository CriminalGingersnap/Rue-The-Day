from Systems import PlayerSelect as Select
from Actions import ItemActions as Items
from . import LootEquipment, LootStones, LootSummons


def searchAll(playersGroup, enemies) -> None:
    groupInv, players = playersGroup["inventory"], [player for player in playersGroup["members"] if player.props["type"] == "human"]
    
    if Select.yesNo("Loot enemies?"):
        humans, standards, creatures, boss = [], [], [], None

        for player in players:
            if  player.inv["standard"] != "None": standards +=  player.inv["standard"] 

        for enemy in enemies:
            if enemy.props["type"] == "human": humans += [enemy]
            elif enemy.props["job"] == "standard": standards += [enemy]
            elif enemy.props["rank"] == "Ascendant": boss = enemy
            else: creatures += [enemy]
        
        if Select.yesNo("Swap equipment?"): LootEquipment.lootEquipment(players, humans)
        if len(standards) > 1: LootSummons.lootStandards(players, standards)
        if len(creatures) > 0: LootSummons.lootEchos(players, creatures)
        if boss != None: groupInv += [boss.inv["shards"]]

        stock = LootStones.getStock(players + humans + standards + creatures)
        for player in players: LootStones.updateStones(player, stock)