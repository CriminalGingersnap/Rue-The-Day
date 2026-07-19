import Systems.PlayerSelect as Select
from . import BoonActions as Boons
from Abilities import Items_Use as Use
import random


def itemAction(fighter, groups, battleMap) -> None:
    inventory = getInventory(fighter)

    if inventory["Total"] > 0:
        del inventory["Total"]
        selection = "None"

        if fighter.props["rank"] == "player": selection = pcSelectItem(fighter.props["job"], inventory)
        else: selection = npcSelectItem(fighter, groups, inventory)

        if selection != "None":
            category, item, application = selection[0], selection[1], selection[2],
            fighter.inv[category][item] -= 1
            Use.execute(fighter, category, item, application, groups, battleMap)


def pcSelectItem(job, inventory) -> str:
    options, item = ["None"], None

    for category in list(inventory.keys()):
        if category == "Echo": options += ["Echo"]
        elif len(inventory[category]) > 1: options += [category]
        elif len(inventory[category]) == 1: options += [category + " -> " + inventory[category][0]]

    answer = Select.pickOption(options, "item category")

    if answer == "None": return answer
    elif answer == "Echo": return ["echo", "spirit", "Animate"]
    elif "->" in answer:
        category = answer.split(" -> ")[0]
        item = answer.split(" -> ")[1]
    else:
        category = answer
        item = Select.pickOption(["None"] + inventory[category], "item")

    if item != "None":
        options = ["Detonate", "Extract"]
        if job == "Paladin": del options["Extract"]
        application = Select.pickOption(options, "application")
        return [category.lower(), item, application]


def npcSelectItem(fighter, groups, inventory) -> str:
    preferences, enemyDmgTypes = {"Detonate": [], "Extract": []}, []
    blockList = allowlist = ["Flame", "Dream", "Ice", "Holy", "Rot"]

    if fighter.props["job"] == "Paladin": allowlist = []
    elif fighter.atrb["base_mag"] > 0:
        blockList -= fighter.equip["weapon"]["dmgTypes"]
        allowlist -= blockList

    if fighter.atrb["cur_hp"] <= (fighter.atrb["half_hp"]): preferences["Extract"] += ["Bleed"]
    else: preferences["Detonate"] += ["Bleed"]

    for enemy in groups["fightingEnemies"]:
        enemyDmgTypes += enemy.equip["weapon"]["dmgTypes"]
    
    if ("Flame" in enemyDmgTypes) and ("Ice" not in enemyDmgTypes):
        if "Flame" in allowlist: preferences["Extract"] += ["Flame"]
        preferences["Detonate"] += ["Ice"]
    elif ("Ice" in enemyDmgTypes) and ("Flame" not in enemyDmgTypes):
        if "Ice" in allowlist: preferences["Extract"] += ["Ice"]
        preferences["Detonate"] += ["Flame"]

    if any(dType in enemyDmgTypes for dType in ["Crush", "Pierce"]) and not any(dType in enemyDmgTypes for dType in ["Dream", "Rot"]):
        if "Dream" in allowlist: preferences["Extract"] += ["Dream"]

    if "Rot" in enemyDmgTypes:
        if "Holy" in allowlist: preferences["Extract"] += ["Holy"]
        if "Holy" not in enemyDmgTypes: preferences["Detonate"] += ["Holy"]
        if "Rot" in allowlist: preferences["Extract"] += ["Rot"]

    if "Toxic" in enemyDmgTypes:
        if ("Holy" not in enemyDmgTypes) and ("Rot" in allowlist): preferences["Extract"] += ["Rot"]

    choices, selection = [], "None"

    if "Echo" in inventory:
        choices += [["echo", "spirit", "Animate"]]
        del inventory["Echo"]

    for category in inventory:
        for item in preferences["Detonate"]:
            if item in inventory[category]: choices += [[category.lower(), item, "Detonate"]]
        for item in preferences["Extract"]:
            if item in inventory[category]: choices += [[category.lower(), item, "Extract"]]
    
    if len(choices) > 0: selection = random.choice(choices)

    return selection


def hasItems(fighter) -> bool:
    hasItems = False
    if fighter.props["type"] in "human":
        itemOptions = getInventory(fighter)
        if itemOptions["Total"] > 0: return True

    return hasItems

def getInventory(fighter) -> dict:
    items = {
        "Cores": [],
        "Pearls": [],
        "Echo": None,
        "Total": 0  
    } 

    cores = fighter.inv["cores"]
    pearls = fighter.inv["pearls"]
    echo = fighter.inv["echo"]

    for core in cores:
        if cores[core] > 0: 
            items["Cores"] += [core]
            items["Total"] += 1
    for pearl in pearls:
        if pearls[pearl] > 0:
            items["Pearls"] += [pearl]
            items["Total"] += 1

    if len(items["Cores"]) == 0: del items["Cores"]
    if len(items["Pearls"]) == 0: del items["Pearls"]

    if echo != "None":
        items["Echo"] = [echo.props["rank"] + " " + echo.props["job"]]
        items["Total"] += 1
    else: del items["Echo"]

    return items


def swapShield(fighter) -> None:
    Select.waitPrint(fighter.name + " exchanges " + fighter.equip["shield"] + " for " + fighter.inv["spare"]["shield"] + ".")

    tempShield = fighter.inv["spare"]["shield"]
    fighter.inv["spare"]["shield"] = fighter.equip["shield"]
    fighter.equip["shield"] = tempShield

def swapWeapon(fighter) -> None:
    Select.waitPrint(fighter.name + " exchanges " + fighter.equip["weapon"] + " for " + fighter.inv["spare"]["weapon"] + ".")

    tempWeapon = fighter.inv["spare"]["weapon"]
    fighter.inv["spare"]["weapon"] = fighter.equip["weapon"]
    fighter.equip["weapon"] = tempWeapon