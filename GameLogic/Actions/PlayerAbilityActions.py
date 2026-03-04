from Systems import PlayerSelect as Select
from . import AttackActions as Attack, BoonActions as Boon, HindranceActions as Hindrance
from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder


def chooseAction(fighter, reachable) -> str:
    usableAttacks = Attack.usableAttacks(fighter, reachable["attackReachable"])
    usableBoons = Boon.usableBoons(fighter)
    usableHindrances = Hindrance.usableHindrances(fighter, reachable["hinderReachable"])

    actionOptions = []

    if (fighter.atrb["cur_mag"] > 0) or (fighter.atrb["cur_mar"] > 0):
        if len(usableBoons) > 0:
            if len(usableBoons) == 1:
                if len(reachable["boonReachable"]) == 1: actionOptions += ["Boon -> " + usableBoons[0] + " -> " + reachable["boonReachable"][0].name]
                else: actionOptions += ["Boon -> " + usableBoons[0]]
            else: actionOptions += ["Boon"]
        if len(usableAttacks) > 0:
            if len(usableAttacks) == 1:
                if len(reachable["attackReachable"]) == 1: actionOptions += ["Attack -> " + usableAttacks[0] + " -> " + reachable["attackReachable"][0].name]
                else: actionOptions += ["Attack -> " + usableAttacks[0]]
            else: actionOptions += ["Attack"]
        if len(usableHindrances) > 0:
            if len(usableHindrances) == 1:
                if len(reachable["hinderReachable"]) == 1: actionOptions += ["Hindrance -> " + usableHindrances[0] + " -> " + reachable["hinderReachable"][0].name]
                else: actionOptions += ["Hindrance -> " + usableHindrances[0]]
            else: actionOptions += ["Hinder"]
       
    Select.waitPrint("\nChoose " + fighter.name + "'s Ability Action:")
    choice =  Select.makeSelection(actionOptions + ["End Turn"])
    
    if "Boon" in choice: choice = "Boon"
    elif "Attack" in choice: choice = "Attack"
    elif "Hinder" in choice: choice = "Hinder"

    return choice


def takeAction(fighter, actionChoice, reachable) -> None:
    match actionChoice:
        case "Attack":
            attackChoice = Attack.pcSelectAttack(fighter, reachable["attackReachable"])
            attackTarget = Select.targetSelect(reachable["attackReachable"])
            Attacks.commitDice(attackChoice, fighter, attackTarget)

        case "Boon":
            boonChoice = Boon.pcSelectBoon(fighter)
            boonTarget = Boon.pcSelectBoonTarget(reachable["boonReachable"])
            Boons.commitDice(fighter, boonTarget, boonChoice)
        
        case "Hinder":
            hindranceChoice = Hindrance.pcSelectHindrance(fighter, reachable["hinderReachable"])
            hindranceTarget = Select.targetSelect(reachable["hinderReachable"])
            Hinder.commitDice(fighter, hindranceTarget, hindranceChoice)