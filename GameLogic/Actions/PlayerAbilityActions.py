from Systems import PlayerSelect as Select
from . import AttackActions as Attack, BoonActions as Boon, HindranceActions as Hindrance, DonateActions as Donate
from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder


def chooseAction(fighter, reachable) -> str:
    usableAttacks = Attack.usableAttacks(fighter, reachable[1])
    usableBoons = Boon.usableBoons(fighter)
    usableHindrances = Hindrance.usableHindrances(fighter, reachable[2])

    actionOptions = []

    if (fighter.atrb["cur_mag"] > 0) or (fighter.atrb["cur_mar"] > 0):
        if len(usableBoons) > 0:
            if len(usableBoons) == 1: actionOptions += ["Boon -> " + usableBoons[0]]
            else: actionOptions += ["Boon"]
        if len(usableAttacks) > 0:
            if len(usableAttacks) == 1: actionOptions += ["Attack -> " + usableAttacks[0]]
            else: actionOptions += ["Attack"]
        if len(usableHindrances) > 0:
            if len(usableHindrances) == 1: actionOptions += ["Hindrance -> " + usableHindrances[0]]
            else: actionOptions += ["Hinder"]
        
        donateOptions = Donate.checkOptions(fighter, reachable[0], reachable[1] + reachable[2])
        if len(donateOptions) > 0: actionOptions += ["Donate"]

    Select.waitPrint("\nChoose " + fighter.name + "'s Ability Action:")
    choice =  Select.makeSelection(actionOptions + ["End Turn"])
    
    if "Boon" in choice: choice = "Boon"
    elif "Attack" in choice: choice = "Attack"
    elif "Hinder" in choice: choice = "Hinder"

    return choice


def takeAction(fighter, actionChoice, reachable) -> None:
    match actionChoice:
        case "Attack":
            attackChoice = Attack.pcSelectAttack(fighter, reachable[1], True)
            attackTarget = Select.targetSelect(reachable[1])
            Attacks.commitDice(attackChoice, fighter, attackTarget)

        case "Boon":
            boonChoice = Boon.pcSelectBoon(fighter)
            boonTarget = Boon.pcSelectBoonTarget(fighter, reachable[0], boonChoice)
            Boons.execute(fighter, boonTarget, boonChoice)
        
        case "Hinder":
            hindranceChoice = Hindrance.pcSelectHindrance(fighter, reachable[2])
            hindranceTarget = Select.targetSelect(reachable[2])
            Hinder.execute(fighter, hindranceTarget, hindranceChoice)

        case "Donate":
            donateOptions = Donate.checkOptions(fighter, reachable[0], reachable[1] + reachable[2])
            donateChoice = Donate.chooseDonation(fighter, donateOptions)
            Donate.donate(fighter, donateChoice[0], donateChoice[1])