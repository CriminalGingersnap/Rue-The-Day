from Systems import PlayerSelect as Select
from . import AreaActions as Area, AttackActions as Attack, BoonActions as Boon, HindranceActions as Hindrance
from Abilities import Area_Set as Area, AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder


def playerAction(fighter, groups, battleMap) -> None:
    actionChoice = chooseAction(fighter, groups["reachable"])
    takeAction(fighter, actionChoice, groups, groups["reachable"], battleMap) 


def chooseAction(fighter, reachable) -> str:
    usableAreas = Area.usableAreas(fighter)
    usableAttacks = Attack.usableAttacks(fighter, reachable["attackReachable"])
    usableBoons = Boon.usableBoons(fighter)
    usableHindrances = Hindrance.usableHindrances(fighter, reachable["hinderReachable"])

    actionOptions = []

    if len(usableAttacks) == 1: actionOptions += ["Area -> " + usableAreas[0]]
    elif len(usableAreas) > 1: actionOptions += ["Area"]

    if len(usableAttacks) == 1:
        if len(reachable["attackReachable"]) == 1: actionOptions += ["Attack -> " + usableAttacks[0] + " -> " + reachable["attackReachable"][0].props["name"]]
        else: actionOptions += ["Attack -> " + usableAttacks[0]]
    elif len(usableAttacks) > 1: actionOptions += ["Attack"]

    if len(usableBoons) == 1:
        if len(reachable["boonReachable"]) == 1: actionOptions += ["Boon -> " + usableBoons[0] + " -> " + reachable["boonReachable"][0].props["name"]]
        else: actionOptions += ["Boon -> " + usableBoons[0]]
    elif len(usableBoons) > 1: actionOptions += ["Boon"]

    if len(usableHindrances) == 1:
        if len(reachable["hinderReachable"]) == 1: actionOptions += ["Hindrance -> " + usableHindrances[0] + " -> " + reachable["hinderReachable"][0].props["name"]]
        else: actionOptions += ["Hindrance -> " + usableHindrances[0]]
    elif len(usableHindrances) > 1: actionOptions += ["Hinder"]
       
    choice =  Select.pickOption(actionOptions + ["End Turn"], fighter.props["name"] + "'s ability action")
    
    if "Area" in choice: choice = "Area"
    if "Attack" in choice: choice = "Attack"
    elif "Boon" in choice: choice = "Boon"
    elif "Hinder" in choice: choice = "Hinder"

    return choice


def takeAction(fighter, actionChoice, groups, reachable, battleMap) -> None:
    match actionChoice:
        case "Area":
            areaChoice = Area.pcSelectArea(fighter)
            dice = Boons.blitzCommit(fighter, fighter.atrb["cur_mag"])
            Area.execute(fighter, dice, groups, areaChoice, battleMap)

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