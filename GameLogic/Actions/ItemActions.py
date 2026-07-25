from Systems import PlayerSelect as Select
from . import ItemActions_NPC as NPC
from Abilities import Items_Use as Use
from Maps import Movement


def itemAction(fighter, groups, battleMap) -> None:
    inventory = getInventory(fighter)

    if inventory["Total"] > 0:
        del inventory["Total"]
        selection = "None"

        if fighter.props["rank"] == "player": selection = pcSelectItem(fighter.props["job"], inventory)
        else: selection = NPC.npcSelectItem(fighter, groups, inventory)

        if selection != "None":
            category, item, application = selection[0], selection[1], selection[2],

            if category == "Echo": fighter.inv["echo"] = "None"
            elif category != "Standard": fighter.inv[category][item] -= 1

            target = getTarget(fighter, groups, application)
            Use.execute(target, category, item, application, groups, battleMap)


def pcSelectItem(job, inventory) -> str:
    options, item = ["None"], None

    for category in list(inventory.keys()):
        if category == "Echo": options += ["Echo"]
        elif len(inventory[category]) > 1: options += [category]
        elif len(inventory[category]) == 1: options += [category + " -> " + inventory[category][0]]

    answer = Select.pickOption(options, "item category")

    if answer == "None": return answer
    elif answer == "Echo": return ["echo", "spirit", "Animate"]
    elif answer == "Standard": return ["standard", "", "Plant"]
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


def getTarget(fighter, groups, application) -> list:
    target = fighter

    if (application == "Extract") and (fighter.props["rank"] == "player"):
        reachable = []

        for target in  groups["fightingAllies"]:
            distance = Movement.getTargetDistance(fighter, target)
            if distance <= 1: reachable += [target]

        if len(reachable) > 1:
            target = Select.targetSelect(reachable)

    return target


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
        "Standard": None,
        "Total": 0  
    } 

    cores = fighter.inv["cores"]
    pearls = fighter.inv["pearls"]
    echo = fighter.inv["echo"]
    standard = fighter.inv["standard"]

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

    if (standard != "None") and not standard.cndt["Planted"]:
        items["Standard"] = [standard.props["rank"] + " " + echo.props["job"]]
        items["Total"] += 1
    else: del items["Standard"]

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