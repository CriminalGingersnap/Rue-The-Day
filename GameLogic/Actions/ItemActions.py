import Systems.PlayerSelect as Select
from . import BoonActions as Boons
from Abilities import Items_Use as Use
import random


def itemAction(fighter, groups, battleMap) -> None:
    while fighter.itemUse > 0:
        itemChoice = "None"

        if fighter.rank == "player": itemChoice = pcSelectItem(fighter, battleMap)
        else: itemChoice = npcSelectItem(fighter, groups)

        if itemChoice != "None": Use.execute(fighter, itemChoice, groups, battleMap)


def pcSelectItem(fighter, battleMap) -> str:
    itemOptions = getInventory(fighter, battleMap)
    categoryOptions, objectOptions = ["None"], ["None"]

    if itemOptions["Total"] == 0:
        return "None"
    else:
        Select.waitPrint("Select item:")
        
        for category in itemOptions:
            if len(itemOptions[category]) > 0: categoryOptions += [category]

        categorySelection = Select.makeSelection(categoryOptions)
        for object in itemOptions[categorySelection]: objectOptions += [object]

        item = Select.makeSelection(objectOptions)
        item = item.split('(')[0]

        if item != "None": depleteItem(fighter, item, categorySelection)

        return [categorySelection, item]
        

def npcSelectItem(fighter, groups):
    itemOptions = getInventory(fighter)
    itemOptions.remove("Total")
    objectPreferences, enemyDmgTypes = [], []
    allowList = blockList = ["Burn", "Freeze", "Dream", "Rot", "Venom"]

    if fighter.atrb["cur_hp"] < (fighter.atrb["base_hp"] * .6): objectPreferences += ["Vigor"]

    for enemy in groups["fightingEnemies"]: enemyDmgTypes += Boons.enemyDamageTypes(enemy)
    
    if fighter.atrb["base_mag"] > 0:
        weaponDmgTypes = fighter.equipment["weapon"]["dmgTypes"]
        blockList -= weaponDmgTypes
        allowList -= blockList
    
    if all("Burn" in [enemyDmgTypes, allowList]) and ("Freeze" not in enemyDmgTypes):
        objectPreferences += ["Flameblood"]
    if all("Freeze" in [enemyDmgTypes, allowList]) and ("Burn" not in enemyDmgTypes):
        objectPreferences += ["Iceblood"]
    if any(dType in enemyDmgTypes for dType in ["Crush", "Dream", "Pierce"]):
        if ("Dream" in allowList) and ("Rot" not in enemyDmgTypes): objectPreferences += ["Feyblood"]
    if any(dType in enemyDmgTypes for dType in ["Rot", "Venom"]):
        if ("Rot" in allowList) and ("Holy" not in enemyDmgTypes): objectPreferences += ["Corpseblood"]
        if "Venom" in allowList: objectPreferences += ["Toxinblood"]

    objectChoice = random.choice(objectPreferences)

    for category in itemOptions:
        if objectChoice in itemOptions[category]: categoryOptions += [category]
        
    categoryChoice = random.choice(categoryOptions)

    return [categoryChoice, objectChoice]


def hasItems(fighter) -> bool:
    hasItems = False
    if fighter.type in "human":
        itemOptions = getInventory(fighter)
        if itemOptions["Total"] > 0: return True

    return hasItems

def getInventory(fighter) -> dict:
    items = {
        "Stones": [],
        "Dusts": [],
        "Gourd": [],
        "Pills": [],
        "Tinctures": [],
        "Total": 0  
    }   

    dusts = fighter.inventory["Vials"]["Contents"]["Dusts"]
    tinctures = fighter.inventory["Vials"]["Contents"]["Tinctures"]
    pills = fighter.inventory["Pill Box"]["Contents"]["Pills"]
    stones = fighter.inventory["Pill Box"]["Contents"]["Stones"]
    gourd = fighter.inventory["Gourd"]["Contents"]

    if dusts["Neutral"] > 0:
        items["Dusts"] += ["Neutral" + "(" + str(dusts["Neutral"]) + ")"]
        items["Total"] += 1
    
    for stone in stones:
        if stones[stone] > 0:
            items["Stones"] += [stone + "(" + str(stones[stone]) + ")"]
            items["Total"] += 1
    
    if fighter.atrb["base_elm"] != "Corpse":
        for drink in gourd:
            if gourd[drink] > 0:
                items["Gourd"] += [drink + "(" + str(gourd[drink]) + ")"]
                items["Total"] += 1
        for pill in pills:
            if pills[pill] > 0:
                items["Pills"] += [pill + "(" + str(pills[pill]) + ")"]
                items["Total"] += 1
        for tincture in tinctures:
            if tinctures[tincture] > 0:
                items["Tinctures"] += [tincture + "(" + str(tinctures[tincture]) + ")"]
                items["Total"] += 1

    return items


def depleteItem(fighter, item, category):
    if category in ["Pills" | "Stones"]:
        fighter.inventory["Pill Box"]["Contents"][category][item] -= 1
    elif category in ["Dusts", "Tinctures"]:
        fighter.inventory["Vials"]["Contents"][category][item] -= 1
    elif category == "Gourd":
        fighter.inventory["Gourd"]["Contents"][category][item] -= 1