from . import PlayerSelect as Select
import random, time


def roll(fighter, dice, ability, dType) -> int:
    total = 0
    if dice > 0: total = castDice(dice)
    if fighter != None: total += mods(fighter, ability, dType)
    
    Select.quickPrint("Total: ", '')
    time.sleep(Select.waitTime * 2)
    Select.quickPrint(str(total) + "\n")

    return total


def mods(fighter, ability, dType) -> int:
    phrase, mod = " | ", 0

    if ability in fighter.abl["specialty"]:
        mod += 1
        phrase += "+1 (Specialty) | "
    elif ability in fighter.abl["mastery"]:
        mod += 2
        phrase += "+2 (Mastery) | "

    if dType == "magic":
        weapon = fighter.equip["weapon"]["modifier"]        
        if weapon > 0:
            mod += weapon
            phrase += "+" + str(weapon) + " (Weapon) | "

        if fighter.itemEffects["Imbue"]["duration"] > 0:
            mod += fighter.itemEffects["Imbue"]["potency"]
            phrase += "+" + fighter.itemEffects["Imbue"]["potency"] + " (Imbue) | "

    elif (dType == "martial") and (fighter.itemEffects["Invigorate"]["duration"] > 0):
        mod += fighter.itemEffects["Invigorate"]["potency"]
        phrase += "+" + fighter.itemEffects["Invigorate"]["potency"] + " (Invigoration) | "

    if fighter.atrb["fatigue"] > 0:
        mod -= fighter.atrb["fatigue"]
        phrase += "-" + str(fighter.atrb["fatigue"]) + " (Fatigue) | "
    if fighter.atrb["injury"] > 0:
        mod -=  fighter.atrb["injury"]
        phrase += "-" + str(fighter.atrb["injury"]) + " (Injury) | "
    
    if fighter.atrb["corruption"] > 0:
        if random.choice([True, False]):
            mod += fighter.atrb["corruption"]
            phrase += "+"
        else:
            mod -= fighter.atrb["corruption"]
            phrase += "-"
        phrase += str(fighter.atrb["corruption"]) + " (Corruption) | "

    Select.waitPrint("Modifiers: " + str(mod) + phrase)
    return mod


def castDice(dice) -> int:
    total, faces = 0, ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
    
    for die in range(dice):
        roll = random.randint(1, 6)
        Select.quickPrint("Roll " + str(die + 1) + ": ", '')
        time.sleep(Select.waitTime * 2)
        Select.quickPrint(faces[roll - 1] + "    | " + str(roll))

        total += roll
    return total    


def printRemainingDice(fName, dice, dType) -> None:
    endPhrase = ""
    if dice == 0: endPhrase = fName + " has expended all " + dType + " dice."
    elif dice == 1: endPhrase = fName + " retains 1 " + dType + " die."
    else: endPhrase = fName + " retains " + str(dice) + " " +  dType + " dice."

    Select.waitPrint(endPhrase)