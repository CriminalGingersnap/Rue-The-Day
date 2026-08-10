from Systems import PlayerSelect as Select
from . import AttackActions as Attack, BoonActions as Boon, HindranceActions as Hindrance
from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder


def playerAction(fighter, reachable) -> None:
    actionChoice = chooseAction(fighter, reachable)
    takeAction(fighter, actionChoice, reachable) 


def chooseAction(fighter, reachable) -> str:
    usableAttacks = Attack.usableAttacks(fighter, reachable["attackReachable"])
    usableBoons = Boon.usableBoons(fighter)
    usableHindrances = Hindrance.usableHindrances(fighter, reachable["hinderReachable"])

    actionOptions = []

    if len(usableAttacks) > 0:
            if len(usableAttacks) == 1:
                if len(reachable["attackReachable"]) == 1: actionOptions += ["Attack -> " + usableAttacks[0] + " -> " + reachable["attackReachable"][0].props["name"]]
                else: actionOptions += ["Attack -> " + usableAttacks[0]]
            else: actionOptions += ["Attack"]

    if len(usableBoons) > 0:
        if len(usableBoons) == 1:
            if len(reachable["boonReachable"]) == 1: actionOptions += ["Boon -> " + usableBoons[0] + " -> " + reachable["boonReachable"][0].props["name"]]
            else: actionOptions += ["Boon -> " + usableBoons[0]]
        else: actionOptions += ["Boon"]

    if len(usableHindrances) > 0:
        if len(usableHindrances) == 1:
            if len(reachable["hinderReachable"]) == 1: actionOptions += ["Hindrance -> " + usableHindrances[0] + " -> " + reachable["hinderReachable"][0].props["name"]]
            else: actionOptions += ["Hindrance -> " + usableHindrances[0]]
        else: actionOptions += ["Hinder"]
       
    choice =  Select.pickOption(actionOptions + ["End Turn"], fighter.props["name"] + "'s ability action")
    
    if "Attack" in choice: choice = "Attack"
    elif "Boon" in choice: choice = "Boon"
    elif "Hinder" in choice: choice = "Hinder"

    return choice


def takeAction(fighter, actionChoice, reachable) -> None:
    match actionChoice:
        case "Attack":
            attackChoice = Attack.pcSelectAttack(fighter, reachable["attackReachable"])
            attackTarget = Select.targetSelect(reachable["attackReachable"])
            Attacks.commitDice(attackChoice, fighter, attackTarget)

        case "Boon":
            boonChoice = Boon.pcSelectBoon(fighter, reachable["boonReachable"])
            boonTarget = Select.targetSelect(reachable["boonReachable"])
            Boons.commitDice(fighter, boonTarget, boonChoice)
        
        case "Hinder":
            hindranceChoice = Hindrance.pcSelectHindrance(fighter, reachable["hinderReachable"])
            hindranceTarget = Select.targetSelect(reachable["hinderReachable"])
            Hinder.commitDice(fighter, hindranceTarget, hindranceChoice)

        case "End Turn": fighter.cndt["blitzing"] = False