from . import PlayerSelect as Select
from Maps import Movement
import random, time


def roll(fighter, target, dice, ability, dType) -> int:
    total = 0
    if dice > 0: total = castDice(dice)
    if fighter != None:
        distancePenalty = Movement.getTargetDistance(fighter, target) // 2
        total += mods(fighter, distancePenalty, ability, dType)
    
    Select.quickPrint("Total: ", '')
    time.sleep(Select.longWait * 2)
    Select.quickPrint(str(total) + "\n")

    return total


def mods(fighter, distancePenalty, ability, dType) -> int:
    phrase, mod = " | ", 0

    if distancePenalty > 0:
        mod -= distancePenalty
        phrase += "-" + str(distancePenalty) + " (Distance) | "

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
            phrase += "+" + str(fighter.itemEffects["Imbue"]["potency"]) + " (Imbue) | "

    elif (dType == "martial") and (fighter.itemEffects["Invigorate"]["duration"] > 0):
        mod += fighter.itemEffects["Invigorate"]["potency"]
        phrase += "+" + str(fighter.itemEffects["Invigorate"]["potency"]) + " (Invigoration) | "

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

    if fighter.cndt["submerged"] and not fighter.cndt["aquatic"]:
        mod -= 3
        phrase += "-3 (Submerged) | "

    spacer = " "
    if mod < 0: spacer = ""
    Select.waitPrint("Modifiers: " + str(mod) + spacer + phrase)
    return mod


def castDice(dice) -> int:
    total, faces = 0, ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
    
    for die in range(dice):
        roll = random.randint(1, 6)
        Select.quickPrint("Roll " + str(die + 1) + ": ", '')
        time.sleep(Select.longWait)
        Select.quickPrint(faces[roll - 1] + "     | " + str(roll))

        total += roll
    return total    


def printRemainingDice(fName, dice, dType) -> None:
    endPhrase = ""
    if dice == 0: endPhrase = fName + " has expended all " + dType + " dice."
    elif dice == 1: endPhrase = fName + " retains 1 " + dType + " die."
    else: endPhrase = fName + " retains " + str(dice) + " " +  dType + " dice."

    Select.waitPrint(endPhrase)