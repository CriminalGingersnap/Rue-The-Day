from Systems import PlayerSelect as Select


def getStock(party) -> dict:    
    stock = {"cores": [], "pearls": []}

    for fighter in party:
        for pearl in fighter.inv["pearls"]:
            for quantity in range(fighter.inv["pearls"][pearl]): stock["pearls"] += [pearl]
        for core in fighter.inv["cores"]:
            for quantity in range(fighter.inv["cores"][core]): stock["cores"] += [core]

    stock["pearls"].sort()
    stock["cores"].sort()
    return stock


def updateStones(player, stock, cap):
    phrase = player.props["name"] + " can carry " + str(cap) + " more "
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