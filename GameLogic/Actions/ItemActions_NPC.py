import random


def npcSelectItem(fighter, groups, inventory) -> str:
    preferences, enemyDmgTypes = {"Detonate": [], "Extract": []}, []
    blockList = allowlist = ["Flame", "Dream", "Ice", "Holy", "Rot"]

    if fighter.props["job"] == "Paladin": allowlist = []
    elif fighter.atrb["base_mag"] > 0:
        blockList.remove(fighter.equip["weapon"]["dmgTypes"])
        allowlist.remove(blockList)

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