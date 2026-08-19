from Systems import PlayerSelect as Select, Inventory


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


def updateStones(player, stock):
    cap = 10
    player.inv["cores"], player.inv["pearls"] = Inventory.cores, Inventory.pearls
    
    printCap(player, cap)
    coreUpdates = Select.listSelection(stock["cores"], cap, "Assign cores to " + player.props["name"])
    for core in coreUpdates:
        player.inv["cores"][core] += 1
        stock["cores"].remove(core)

    if cap > 0:
        printCap(player, cap)
        pearlUpdates = Select.listSelection(stock["pearls"], cap, "Assign pearls to " + player.props["name"])
        for pearl in pearlUpdates:
            player.inv["pearls"][pearl] += 1
            stock["pearls"].remove(pearl)
            cap -= 1


def printCap(player, cap):
    phrase = player.props["name"] + " can carry " + str(cap) + " more "
    if cap == 1: Select.clearPrint(phrase + "stone.")
    else: Select.clearPrint(phrase + "stones.")