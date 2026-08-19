from . import PlayerSelect as Select, Sort, Conditions
from Maps import Movement
import random, time


def getFlanking(fighter, target) -> bool:
    flanking = not Sort.isVisible(fighter, target.sightMap)
    if flanking:
        if fighter.props["rank"] == target.props["rank"] == "player": flanking = False
        else:
            fighterTeam = fighter.sightMap[fighter.pos[0]][fighter.pos[1]][2]
            targetTeam = target.sightMap[target.pos[0]][target.pos[1]][2]
            if fighterTeam == targetTeam: flanking = False

    return flanking


def roll(fighter, target, dice, ability, dType) -> int:
    total = 0
    if dice > 0: total = castDice(dice)
    if fighter != None:
        distancePenalty = Movement.getTargetDistance(fighter, target) // 2
        favoredType = (fighter.props["favored"] == target.props["type"]) and not (fighter == target)
        flanking = getFlanking(fighter, target)
        total = max(0, total + mods(fighter, distancePenalty, favoredType, flanking, ability, dType))
    
    Select.quickPrint("Total: ", '')
    time.sleep(Select.longWait * 2)
    Select.quickPrint(str(total) + "\n")

    if fighter != None: Conditions.decrementStamina(fighter, dice)

    return total


def mods(fighter, distancePenalty, favoredType, flanking, ability, dType) -> int:
    phrase, mod = " | ", 0

    if distancePenalty > 0:
        mod -= distancePenalty
        phrase += "-" + str(distancePenalty) + " (Distance) | "
    if favoredType:
        mod += 1
        phrase += "+1 (Favored) | "
    if flanking:
        mod += 1
        phrase += "+1 (Flanking) | "

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
            phrase += str(fighter.atrb["corruption"]) + " (Corruption) | "

        weapon = fighter.equip["weapon"]["modifier"]        
        if weapon > 0:
            mod += weapon
            phrase += "+" + str(weapon) + " (Weapon) | "

    if fighter.atrb["fatigue"] > 0:
        mod -= fighter.atrb["fatigue"]
        phrase += "-" + str(fighter.atrb["fatigue"]) + " (Fatigue) | "
    if fighter.atrb["injury"] > 0:
        mod -=  fighter.atrb["injury"]
        phrase += "-" + str(fighter.atrb["injury"]) + " (Injury) | "

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