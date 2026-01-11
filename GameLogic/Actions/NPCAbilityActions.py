from Maps import Movement
from Systems import PlayerSelect as Select
from . import AttackActions, BoonActions, HindranceActions, DonateActions
from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder, Area_Set as Area
import random


def npcAction(fighter, groups, space) -> None:
    reachable, fightingAllies, fightingEnemies = groups[0], groups[1], groups[2]
    actionOptions = []
    
    boonChoice, boonTarget = BoonActions.npcSelectBoon(fighter, fightingEnemies), "None"
    if boonChoice != "None":
        boonTarget = BoonActions.npcSelectBoonTarget(fighter, reachable[0], boonChoice)
        if boonTarget != "None": actionOptions += ["Boon"]

    attackChoice, attackTarget = "None", AttackActions.npcSelectAttackTarget(fighter, reachable[1])
    if attackTarget != "None":
        attackChoice = AttackActions.npcSelectAttack(fighter, attackTarget)
        if attackChoice != "None": actionOptions += ["Attack"]
    
    hindranceTarget, hindranceChoice = "None", HindranceActions.npcSelectHindrance(fighter, reachable[2], fightingAllies)
    if hindranceChoice != "None":
        hindranceTarget = HindranceActions.npcSelectHindranceTarget(fighter, reachable[2], hindranceChoice)
        if hindranceTarget != "None": actionOptions += ["Hindrance"]

    donateOptions = DonateActions.checkOptions(fighter, reachable[0], reachable[1] + reachable[2])
    donateTarget, donateAbility = None, None
    if len(donateOptions) > 0:
        donateChoice = random.choice(donateOptions)
        donateTarget, donateAbility = donateChoice[0], donateChoice[1]
        actionOptions += ["Donate"]  

    if len(actionOptions) > 0:
        match random.choice(actionOptions):
            case "Attack": Attacks.commitDice(attackChoice, fighter, attackTarget)
            case "Boon": Boons.execute(fighter, boonTarget, boonChoice) # Add area options
            case "Hinder": Hinder.execute(fighter, hindranceTarget, hindranceChoice)
            case "Donate": DonateActions.donate(fighter, donateTarget, donateAbility)
    else:
        if any(dice > 0 for dice in [fighter.atrb["cur_mar"], fighter.atrb["cur_mag"]]):
            Select.waitPrint(fighter.name + " foregoes action.")