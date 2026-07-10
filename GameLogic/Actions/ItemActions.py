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
    category = Select.pickOption(list(inventory.keys()), "item category")
    item = Select.pickOption(["None"] + inventory[category], "item")

    if item != "None":
        options = ["Detonate", "Extract"]
        if job == "Paladin": del options["Extract"]
        application = Select.pickOption(options, "application")
        return [category, item, application]

    return "None"


def npcSelectItem(fighter, groups, inventory) -> str:
    preferences, enemyDmgTypes = {"Detonate": [], "Extract": []}, []
    blockList = allowlist = ["Burn", "Dream", "Freeze", "Holy", "Rot", "Venom"]

    if fighter.props["job"] == "Paladin": allowlist = []
    elif fighter.atrb["base_mag"] > 0:
        blockList -= fighter.equip["weapon"]["dmgTypes"]
        allowlist -= blockList

    if fighter.atrb["cur_hp"] < (fighter.atrb["base_hp"] * .6): preferences += ["Sanguine"]

    for enemy in groups["fightingEnemies"]: enemyDmgTypes += Boons.enemyDamageTypes(enemy)
    
    if ("Burn" in enemyDmgTypes) and ("Freeze" not in enemyDmgTypes):
        if "Burn" in allowlist: preferences["Extract"] += ["Flame"]
        preferences["Detonate"] += ["Ice"]
    if ("Freeze" in enemyDmgTypes) and ("Burn" not in enemyDmgTypes):
        if "Freeze" in allowlist: preferences["Extract"] += ["Ice"]
        preferences["Detonate"] += ["Flame"]
    if any(dType in enemyDmgTypes for dType in ["Crush", "Dream", "Pierce"]) and ("Rot" not in enemyDmgTypes):
        if "Dream" in allowlist: preferences["Extract"] += ["Fey"]
    if any(dType in enemyDmgTypes for dType in ["Rot", "Venom"]):
        if ("Holy" not in enemyDmgTypes):
            if "Holy" in allowlist: preferences["Extract"] += ["Blessed"]
            if "Rot" in allowlist: preferences["Extract"] += ["Corpse"]
            preferences["Detonate"] += ["Blessed"]
        if "Venom" in allowlist: preferences["Extract"] += ["Toxin"]
    else: preferences["Detonate"] += ["Toxin"]

    choices, selection = [], "None"

    for category in inventory:
        for item in preferences["Detonate"]:
            if item in inventory[category]: choices += [[category, item, "detonate"]]
        for item in preferences["Extract"]:
            if item in inventory[category]: choices += [[category, item, "extract"]]
    
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
        "cores": [],
        "pearls": [],
        "Total": 0  
    } 

    cores = fighter.inv["cores"]
    pearls = fighter.inv["pearls"]

    for core in cores:
        if cores[core] > 0: 
            items["cores"] += [core]
            items["Total"] += 1
    for pearl in pearls:
        if pearls[pearl] > 0:
            items["pearls"] += [pearl]
            items["Total"] += 1

    if len(items["cores"]) == 0: del items["cores"]
    if len(items["pearls"]) == 0: del items["pearls"]

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