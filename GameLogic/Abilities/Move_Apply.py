
from Systems import Roll, Conditions, PlayerSelect as Select
from Abilities import Boons_Set as Boons
from . import Attacks_Martial as Martial, Area_Set as Area

stationaryAbilities = ["Inventory", "Enchant", "Evade", "Examine", "Set"]


def execute(fighter, groups, ability, battleMap) -> None: 
    reachable = groups["reachable"]
    visibleTargets = reachable["visibleAllies"] + reachable["visibleEnemies"]

    match ability:
        case "Enchant": Area.enchant(fighter, battleMap, 1)
        case "Examine": applyExamine(visibleTargets)
        case "Evade": applyEvade(fighter)
        case "Inventory": applyInventory(fighter)
        case "Set": applySet(fighter)

    fighter.atrb["cur_sp"] = 0


def applyEvade(fighter) -> None:
    fighter.commitments["Guard"]["targets"] += [fighter]
    fighter.effects["Guard"]["source"] = fighter
    fighter.effects["Guard"]["ability"] = "Evade"
    fighter.effects["Guard"]["dice"] += 1

    Boons.boonComment(fighter, fighter, "Evade")


def applySet(fighter) -> None:
    fighter.atrb["cur_mar"] += 1
    Select.waitPrint(fighter.name + " sets in place!")    


def applyInventory(fighter) -> None:
    phrase = ""

    if "Quick Inventory" in fighter.abl["boons"]:
        fighter.itemUse = 2
        phrase = "access two items!"
    else: 
        fighter.itemUse = 1    
        phrase = "access an item!"
    
    Select.waitPrint(fighter.name + " opens their inventory to " + phrase)


def applyExamine(visibleTargets) -> None:
    examinee = Select.targetSelect(visibleTargets)

    if examinee != "None":
        Select.waitPrint("\n" + examinee.name + "'s base stats:")
        av, reach = Martial.getBaseAv("Stab", "Pierce", examinee), examinee.equipment["weapon"]["reach"]
        hp, stamina, speed, tolerance = examinee.atrb["cur_hp"], examinee.atrb["stamina"],  examinee.atrb["base_sp"], examinee.atrb["tolerance"]
        strAV, strHP, strStamina, strSpeed, strTolerance, strReach = str(av), str(hp), str(stamina), str(speed), str(tolerance), str(reach)
        
        if av < 10: strAV += " "
        if hp < 10: strHP += " "
        if speed < 10: strSpeed += " "
        if stamina < 10: strStamina += " "
        if tolerance < 10: strTolerance += " "

        armorStatement, shieldStatement, weaponStatement  = "", "", ""
        
        if (examinee.cndt["armored"]):
            armorStatement = "Naturally armored. "
        elif examinee.equipment["armor"]["name"] != None:
            armorStatement = "Wearing " + examinee.equipment["armor"]["name"] + " armor. "
        else: armorStatement = "Unarmored."

        if examinee.equipment["shield"]["name"] != None:
            shieldStatement = "Carrying a " + examinee.equipment["shield"]["name"] + " shield. "
        if examinee.equipment["weapon"]["name"] != None:
            article = "a "
            if examinee.equipment["weapon"]["name"][0] in ["A", "E", "I", "O", "U", "Y"]: article = "an "
            weaponStatement = "Wielding " + article + examinee.equipment["weapon"]["name"] + ". "

        Select.waitPrint("Avoidance: " + strAV + " | " + armorStatement + shieldStatement)
        Select.waitPrint("Health: " + strHP)
        Select.waitPrint("Reach: " + strReach + " | "  + weaponStatement)
        Select.waitPrint("Speed: " + strSpeed)
        Select.waitPrint("Stamina: " + strStamina + "   | Fatigue: " + str(examinee.atrb["fatigue"]))
        Select.waitPrint("Tolerance: " + strTolerance + " | Corruption: " + str(examinee.atrb["corruption"]))

        Select.waitPrint("\nCommitments: ")
        for commitment in examinee.commitments:
            if len(examinee.commitments[commitment]["targets"]) > 0:
                Select.quickPrint(commitment + " -> ")
                for target in examinee[commitment]["targets"]:
                    Select.quickPrint(target.name, end = " | ")

        Select.waitPrint("\nEffects: ")
        for effect in examinee.effects:
            if examinee.effects[effect]["dice"] > 0:
                Select.quickPrint(effect + " <- " + examinee.effects[effect]["source"].name, end = " | ")

        Select.waitPrint("\nItem Effects:")
        for effect in examinee.itemEffects:
            if examinee.itemEffects[effect]["duration"] > 0:
                Select.quickPrint(effect + " (" + str(examinee.itemEffects[effect]["duration"]) + ")", end = " | ")

        Select.waitPrint("\nPending actions: " + str(len(examinee.actionQueue)) + " | " + "Remaining movement: " + str(examinee.atrb["cur_sp"]))
        Select.waitPrint("Element: " + examinee.atrb["cur_elm"] + " | " + "Rank: " + examinee.atrb["rank"])
        Select.waitPrint("Magic Dice: " + str(examinee.atrb["base_mag"]) + " | Martial Dice: " + str(examinee.atrb["base_mar"]) + "\n")