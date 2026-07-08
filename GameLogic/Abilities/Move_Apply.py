
from Systems import PlayerSelect as Select, Conditions
from . import Attacks_Martial as Martial, Boons_Set as Boons
from Actions import ItemActions

stationaryAbilities = ["Inventory", "Empower", "Evade", "Examine", "Set"]


def execute(fighter, groups, ability, battleMap) -> None: 
    reachable = groups["reachable"]
    visibleTargets = reachable["visibleAllies"] + reachable["visibleEnemies"]

    match ability:
        case "Empower": applyEmpower(visibleTargets)
        case "Examine": applyExamine(visibleTargets)
        case "Evade": applyEvade(fighter)
        case "Inventory": ItemActions.itemAction(fighter, groups, battleMap)
        case "Set": applySet(fighter)

    fighter.atrb["cur_sp"] = 0


def applyEmpower(fighter) -> None:
    Conditions.decrementTolerance(fighter, fighter.atrb["cur_mag"])
    fighter.atrb["cur_mar"] += fighter.atrb["cur_mag"]
    fighter.atrb["cur_mag"] = 0
    Select.waitPrint(fighter.props["name"] + " empowers their body with magic!")  


def applyEvade(fighter) -> None:
    fighter.commits["Guard"]["targets"] += [fighter]
    fighter.effects["Guard"]["source"] = fighter
    fighter.effects["Guard"]["ability"] = "Evade"
    fighter.effects["Guard"]["dice"] += 1

    Boons.boonComment(fighter, fighter, "Evade")   


def applySet(fighter) -> None:
    fighter.atrb["cur_mar"] += 1
    Select.waitPrint(fighter.props["name"] + " sets in place!") 


def applyExamine(visibleTargets) -> None:
    examinee = Select.targetSelect(visibleTargets)

    if examinee != "None":
        Select.waitPrint("\n" + examinee.props["name"] + "'s base stats:")
        av, reach = Martial.getBaseAv("Stab", "Pierce", examinee), examinee.equip["weapon"]["reach"]
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
        elif examinee.equip["armor"]["name"] != None:
            armorStatement = "Wearing " + examinee.equip["armor"]["name"] + " armor. "
        else: armorStatement = "Unarmored."

        if examinee.equip["shield"]["name"] != None:
            shieldStatement = "Carrying a " + examinee.equip["shield"]["name"] + " shield. "
        if examinee.equip["weapon"]["name"] != None:
            article = "a "
            if examinee.equip["weapon"]["name"][0] in ["A", "E", "I", "O", "U", "Y"]: article = "an "
            weaponStatement = "Wielding " + article + examinee.equip["weapon"]["name"] + ". "

        Select.waitPrint("Avoidance: " + strAV + " | " + armorStatement + shieldStatement)
        Select.waitPrint("Health: " + strHP)
        Select.waitPrint("Reach: " + strReach + " | "  + weaponStatement)
        Select.waitPrint("Speed: " + strSpeed)
        Select.waitPrint("Stamina: " + strStamina + "   | Fatigue: " + str(examinee.atrb["fatigue"]))
        Select.waitPrint("Tolerance: " + strTolerance + " | Corruption: " + str(examinee.atrb["corruption"]))

        Select.waitPrint("\nCommitments: ")
        for commitment in examinee.commits:
            if len(examinee.commits[commitment]["targets"]) > 0:
                Select.quickPrint(commitment + " -> ")
                for target in examinee[commitment]["targets"]:
                    Select.quickPrint(target.props["name"], end = " | ")

        Select.waitPrint("\nEffects: ")
        for effect in examinee.effects:
            if examinee.effects[effect]["dice"] > 0:
                Select.quickPrint(effect + " <- " + examinee.effects[effect]["source"].props["name"], end = " | ")

        Select.waitPrint("\nItem Effects:")
        for effect in examinee.itemEffects:
            if examinee.itemEffects[effect]["duration"] > 0:
                Select.quickPrint(effect + " (" + str(examinee.itemEffects[effect]["duration"]) + ")", end = " | ")

        Select.waitPrint("\nPending actions: " + str(len(examinee.actionQueue)) + " | " + "Remaining movement: " + str(examinee.atrb["cur_sp"]))
        Select.waitPrint("Element: " + examinee.atrb["cur_elm"] + " | " + "Rank: " + examinee.atrb["rank"])
        Select.waitPrint("Magic Dice: " + str(examinee.atrb["base_mag"]) + " | Martial Dice: " + str(examinee.atrb["base_mar"]) + "\n")