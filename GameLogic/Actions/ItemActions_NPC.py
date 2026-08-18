from Abilities import Area_Locate as Locate
from Maps import Movement
import random


def npcSelectItem(fighter, groups, inventory) -> str:
    preferences, enemyDmgTypes, closeDmgTypes = {"Detonate": [], "Extract": []}, [], []
    blockList = allowList = ["Flame", "Ice", "Holy", "Rot"]

    if fighter.props["job"] == "Paladin": allowList = []
    elif fighter.atrb["base_mag"] > 0:
        blockList.remove(fighter.equip["weapon"]["dmgTypes"][0])
        allowList.remove(blockList)

    for enemy in groups["fightingEnemies"]:
        enemyDmgTypes += enemy.equip["weapon"]["dmgTypes"]
        if Movement.getTargetDistance(fighter, enemy) <= 4:
            closeDmgTypes += enemy.equip["weapon"]["dmgTypes"]

    setExtractPreferences(fighter, preferences, enemyDmgTypes, allowList)
    setDetonationPreferences(fighter, groups, preferences, closeDmgTypes)
    
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


def setExtractPreferences(fighter, preferences, enemyDmgTypes, allowList):
    if fighter.atrb["cur_hp"] <= (fighter.atrb["half_hp"]):
        preferences["Extract"] += ["Bleed"]

    if fighter.atrb["corruption"] <= 1:
        if "Flame" in allowList:
            if ("Flame" in enemyDmgTypes) and ("Ice" not in enemyDmgTypes):
                preferences["Extract"] += ["Flame"]

        if "Ice" in allowList:
            if ("Ice" in enemyDmgTypes) and ("Flame" not in enemyDmgTypes):
                preferences["Extract"] += ["Ice"]

        if "Dream" in allowList:
            if any(dType in enemyDmgTypes for dType in ["Crush", "Pierce"]):
                preferences["Extract"] += ["Dream"]

        if ("Rot" in allowList) and ("Holy" not in enemyDmgTypes):
            if "Rot" in enemyDmgTypes:
                if "Holy" in allowList: preferences["Extract"] += ["Holy"]
                preferences["Extract"] += ["Rot"]

            if "Toxic" in enemyDmgTypes: preferences["Extract"] += ["Rot"]


def setDetonationPreferences(fighter, groups, preferences, closeDmgTypes):
    range = 4
    if "Sling" == fighter.equip["weapon"]["name"]: range = fighter.equip["weapon"]["reach"]
    
    if Locate.findSpace(fighter, groups, range, "stone") != "None":
        if "Flame" in closeDmgTypes: preferences["Detonate"] += ["Ice"]
        elif "Ice" in closeDmgTypes: preferences["Detonate"] += ["Flame"]

        if "Rot" in closeDmgTypes: preferences["Detonate"] += ["Holy"]
        else: preferences["Detonate"] += ["Rot"]