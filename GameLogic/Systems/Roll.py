from . import PlayerSelect as Select, Conditions
import Abilities.AttackAbilities as Attacks
import random, time


def roll(fighter, dice, ability, dType) -> int:
    if dice > 0: total = castDice(dice, False)
    total = changeTotal(fighter, dice, ability, dType)
    
    print("Total: ", end='')
    time.sleep(Select.waitTime * 2)
    print(str(total) + "\n")

    return total


def changeTotal(fighter, dice, ability, dType) -> int:
    phrase, mod = " | ", dice
    
    if ability in fighter.abl["specialty"]:
        mod += 1
        phrase += "+1 (Specialty) | "
    elif ability in fighter.abl["mastery"]:
        mod += 2
        phrase += "+2 (Mastery) | "

    if dType == "magic":
        if fighter.atrb["corruption"] > 0:
            if random.choice([True, False]):
                mod += fighter.atrb["corruption"]
                phrase += "+"
            else:
                mod -= fighter.atrb["corruption"]
                phrase += "-"
            phrase += str(fighter.atrb["corruption"]) + " (Instability) | "
    
    if dType == "martial":            
        if fighter.atrb["injury"] > 0:
            mod -=  fighter.atrb["injury"]
            phrase += "-" + str(fighter.atrb["injury"]) + " (Injury) | "
        if fighter.itemEffects["Invigorate"]["duration"] > 0:
            mod += fighter.itemEffects["Invigorate"]["potency"]
            phrase += "+" + fighter.itemEffects["Invigorate"]["potency"] + " (Invigoration) | "
    
    if fighter.atrb["fatigue"] > 0:
        mod -= fighter.atrb["fatigue"]
        phrase += "-" + str(fighter.atrb["fatigue"]) + " (Fatigue) | "

    mod = max(0, mod)

    Select.waitPrint("Modifiers: " + str(mod) + phrase)

    return dice * mod


def castDice(dice) -> int:
    total, faces = 0, ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
    
    for die in range(dice):
        roll = random.randint(1, 6)
        print("Roll " + str(die + 1) + ": ", end='')
        time.sleep(Select.waitTime * 2)
        print(faces[roll - 1])

        total += roll
    return total    


def printRemainingDice(fName, dice, dType) -> None:
    endPhrase = ""
    if dice == 0: endPhrase = fName + " has expended all " + dType + " dice."
    elif dice == 1: endPhrase = fName + " retains 1 " + dType + " die."
    else: endPhrase = fName + " retains " + str(dice) + " " +  dType + " dice."

    Select.waitPrint(endPhrase)