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

        categoryChoice = Select.makeSelection(categoryOptions)
        for object in itemOptions[categoryChoice]: objectOptions += [object]

        item = Select.makeSelection(objectOptions)
        item = item.split('(')[0]

        if item != "None": depleteItem(fighter, item, categoryChoice)

        return [categoryChoice, item]
        

def npcSelectItem(fighter, groups):
    heldItems = getInventory(fighter)
    itemPreferences, enemyDmgTypes = [], []
    allowList = blockList = ["Burn", "Freeze", "Dream", "Rot", "Venom"]

    if fighter.atrb["cur_hp"] < (fighter.atrb["base_hp"] * .6): itemPreferences += ["Vigor"]
    if fighter.atrb["base_mag"] > 0: itemPreferences += ["Corpse", "Flame", "Fey", "Ice", "Blessed", "Toxin"]


    for enemy in groups["fightingEnemies"]: enemyDmgTypes += Boons.enemyDamageTypes(enemy)
    
    if fighter.atrb["base_mag"] > 0:
        weaponDmgTypes = fighter.equipment["weapon"]["dmgTypes"]
        blockList -= weaponDmgTypes
        allowList -= blockList
    
    if all("Burn" in [enemyDmgTypes, allowList]) and ("Freeze" not in enemyDmgTypes):
        itemPreferences += ["Flameblood"]
    if all("Freeze" in [enemyDmgTypes, allowList]) and ("Burn" not in enemyDmgTypes):
        itemPreferences += ["Iceblood"]
    if any(dType in enemyDmgTypes for dType in ["Crush", "Dream", "Pierce"]):
        if ("Dream" in allowList) and ("Rot" not in enemyDmgTypes): itemPreferences += ["Feyblood"]
    if any(dType in enemyDmgTypes for dType in ["Rot", "Venom"]):
        if ("Rot" in allowList) and ("Holy" not in enemyDmgTypes): itemPreferences += ["Corpseblood"]
        if "Venom" in allowList: itemPreferences += ["Toxinblood"]


    categoryChoice, itemChoice = "", "None"
    categoryOptions, itemOptions = [], {
        "Dusts": [],
        "Gourd": [],
        "Pills": [],
        "Tinctures": []
    }   

    for category in itemOptions:
        for item in itemPreferences:
            if item in heldItems[category]:
                categoryOptions += [category]
                itemOptions[category] += [item]
    
    if len(categoryOptions) > 0:
        categoryChoice = random.choice(categoryOptions)
        itemChoice = random.choice(itemOptions[categoryChoice])

    if itemChoice != "None": depleteItem(fighter, itemChoice, categoryChoice)

    return [categoryChoice, itemChoice]


def hasItems(fighter) -> bool:
    hasItems = False
    if fighter.type in "human":
        itemOptions = getInventory(fighter)
        if itemOptions["Total"] > 0: return True

    return hasItems

def getInventory(fighter) -> dict:
    isPlayer = fighter.rank == "player"
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

    for dust in dusts:
        if dusts[dust] > 0:
            entry = dust
            if isPlayer: entry += "(" + str(dusts[dust]) + ")"
            items["Dusts"] += [entry]
            items["Total"] += 1

    for stone in stones:
        if stones[stone] > 0:
            entry = stone
            if isPlayer: entry += "(" + str(stones[stone]) + ")"
            items["Stones"] += [entry]
            items["Total"] += 1
    
    if fighter.atrb["base_elm"] != "Corpse":
        for drink in gourd:
            if gourd[drink] > 0:
                entry = drink
                if isPlayer: entry += "(" + str(gourd[drink]) + ")"
                items["Gourd"] += [entry]
                items["Total"] += 1
        for pill in pills:
            if pills[pill] > 0:
                entry = pill
                if isPlayer: entry += "(" + str(pills[pill]) + ")"
                items["Pills"] += [entry]
                items["Total"] += 1
        for tincture in tinctures:
            if tinctures[tincture] > 0:
                entry = tincture
                if isPlayer: entry += "(" + str(tinctures[tincture]) + ")"
                items["Tinctures"] += [entry]
                items["Total"] += 1

    return items


def depleteItem(fighter, item, category):
    if category in ["Pills" | "Stones"]:
        fighter.inventory["Pill Box"]["Contents"][category][item] -= 1
    elif category in ["Dusts", "Tinctures"]:
        fighter.inventory["Vials"]["Contents"][category][item] -= 1
    elif category == "Gourd":
        fighter.inventory["Gourd"]["Contents"][category][item] -= 1