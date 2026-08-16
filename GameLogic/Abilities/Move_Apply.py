
from Systems import PlayerSelect as Select
from . import Attacks_Martial as Martial, Boons_Set as Boons
from Actions import ItemActions
from Maps import Map_Print as Print
import random


stationaryAbilities = ["Evade", "Examine", "Inventory -> Access", "Inventory", "Swap Shield", "Swap Weapon"]


def execute(fighter, groups, ability, battleMap, itemSelection="None") -> None: 
    reachable = groups["reachable"]
    visibleTargets = reachable["visibleAllies"] + reachable["visibleEnemies"]

    match ability:
        case "Evade":
            trueBoon = Boons.boonComment(fighter, fighter, ability)
            Boons.setBuff(fighter, fighter, 1, ability, trueBoon)
        case "Examine": applyExamine(visibleTargets, battleMap)
        case "Inventory -> Access": ItemActions.itemAction(fighter, groups, battleMap, itemSelection)
        case "Inventory": rummageInventory(fighter, groups, battleMap, itemSelection)
        case "Swap Shield": ItemActions.swapShield(fighter)
        case "Swap Weapon": ItemActions.swapWeapon(fighter)

    fighter.atrb["cur_sp"] = 0


def rummageInventory(fighter, groups, battleMap, itemSelection):    
    searchIntensity = ""
    if fighter.props["rank"] == "player": searchIntensity = Select.pickOption(["Access", "Rummage"], "search intensity")
    else: searchIntensity = random.choice(["Access", "Access", "Rummage"])
    
    ItemActions.itemAction(fighter, groups, battleMap, itemSelection)
    if searchIntensity == "Rummage":
        ItemActions.itemAction(fighter, groups, battleMap, itemSelection)
        fighter.atrb["cur_mag"], fighter.atrb["cur_mar"] = 0, 0


def applyExamine(visibleTargets, battleMap) -> None:
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
        Select.quickPrint("Reach:     " + strReach + " | "  + weaponStatement)
        Select.quickPrint("Speed:     " + strSpeed)
        Select.quickPrint("Health:    " + strHP + " | Injury: " + str(examinee.atrb["injury"]))
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
                Select.quickPrint(commitment, ending = " -> ")
                for target in examinee.commits[commitment]["targets"]:
                    Select.quickPrint(target.props["name"], ending = " | ")
                print()

        Select.waitPrint("\nConditions: ")
        for condition in examinee.cndt:
            if examinee.cndt[condition] == True:
                Select.quickPrint(condition, ending = " | ")

        if Select.yesNo("\n\nView " + examinee.props["name"] + "'s sight map?"):
            Print.printSightMap(battleMap, examinee.sightMap, examinee.props["name"] + "'s Sight Map")
            input("\n\nPress Enter to continue")

        Select.waitPrint("")