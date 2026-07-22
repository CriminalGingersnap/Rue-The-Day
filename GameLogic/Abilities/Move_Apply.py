
from Systems import PlayerSelect as Select, Conditions
from . import Attacks_Martial as Martial
from Actions import ItemActions

stationaryAbilities = ["Empower", "Evade", "Examine", "Inventory", "Set", "Swap Shield", "Swap Weapon"]


def execute(fighter, groups, ability, battleMap) -> None: 
    reachable = groups["reachable"]
    visibleTargets = reachable["visibleAllies"] + reachable["visibleEnemies"]

    match ability:
        case "Empower": applyEmpower(fighter)
        case "Examine": applyExamine(visibleTargets)
        case "Evade": applyEvade(fighter)
        case "Inventory": ItemActions.itemAction(fighter, groups, battleMap)
        case "Set": applySet(fighter)
        case "Swap Shield": ItemActions.swapShield(fighter)
        case "Swap Weapon": ItemActions.swapWeapon(fighter)

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

    Select.waitPrint(fighter.props["name"] + " prepares to evade!") 

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
        if reach < 10: strReach += " "
        if speed < 10: strSpeed += " "
        if stamina < 10: strStamina += " "
        if tolerance < 10: strTolerance += " "

        armorStatement, shieldStatement, weaponStatement  = "", "", ""
        
        if (examinee.cndt["armored"]):
            armorStatement = "Naturally armored. "
        elif examinee.equip["armor"]["name"] != "None":
            armorName = examinee.equip["armor"]["name"]
            if examinee.equip["armor"]["element"] != "Basic": armorName += " " + examinee.equip["armor"]["element"]
            armorStatement = "Wearing " + armorName + " armor. "
        else: armorStatement = "Unarmored."

        if examinee.equip["shield"]["name"] != "None":
            shieldName = examinee.equip["shield"]["name"]
            if shieldName == "Talisman": shieldName += " of " + examinee.equip["shield"]["element"] + " Protection"
            else: shieldName += " shield"
            shieldStatement = "Carrying a " + shieldName + ". "
        if examinee.equip["weapon"]["name"] != "None":
            article = "a "
            if examinee.equip["weapon"]["name"][0] in ["A", "E", "I", "O", "U", "Y"]: article = "an "
            weaponStatement = "Wielding " + article + examinee.equip["weapon"]["name"] + ". "

        Select.waitPrint("Avoidance: " + strAV + " | " + armorStatement + " " + shieldStatement)
        Select.quickPrint("Health:    " + strHP + " | Speed:     " + strSpeed)
        Select.quickPrint("Reach:     " + strReach + " | "  + weaponStatement)
        Select.quickPrint("Stamina:   " + strStamina + " | Fatigue: " + str(examinee.atrb["fatigue"]))
        Select.quickPrint("Tolerance: " + strTolerance + " | Corruption: " + str(examinee.atrb["corruption"]))
        Select.quickPrint("Magic Dice: " + str(examinee.atrb["base_mag"]) + " | Martial Dice: " + str(examinee.atrb["base_mar"]))
        Select.quickPrint("Element: " + examinee.atrb["cur_elm"])
        Select.quickPrint("Rank: " + examinee.props["rank"])

        Select.quickPrint("\nEffects: ")
        for effect in examinee.effects:
            if examinee.effects[effect]["dice"] > 0:
                Select.quickPrint(effect + " <- " + examinee.effects[effect]["source"].props["name"], ending = " | ")

        Select.quickPrint("\nItem Effects:")
        for effect in examinee.itemEffects:
            if examinee.itemEffects[effect]["duration"] > 0:
                Select.quickPrint(effect + " (" + str(examinee.itemEffects[effect]["duration"]) + ")", ending = " | ")

        Select.waitPrint("\nCommitments: ")
        for commitment in examinee.commits:
            if len(examinee.commits[commitment]["targets"]) > 0:
                Select.quickPrint(commitment + " -> ")
                for target in examinee[commitment]["targets"]:
                    Select.quickPrint(target.props["name"], ending = " | ")

        Select.waitPrint("\nConditions: ")
        for condition in examinee.cndt:
            if examinee.cndt[condition] == True:
                Select.quickPrint(condition, ending = " | ")

        input("\n\nPress Enter to continue")
        Select.waitPrint("")