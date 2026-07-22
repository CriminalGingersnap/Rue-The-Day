from Maps import Movement
from Systems import PlayerSelect as Select
from . import AttackActions, BoonActions, HindranceActions
from Abilities import AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder, Area_Set as Area
import random


def npcAction(fighter, groups) -> None:
    reachable, fightingAllies, fightingEnemies = groups["reachable"], groups["fightingAllies"], groups["fightingEnemies"]
    actionOptions = []
    
    boonChoice, boonTarget = BoonActions.npcSelectBoon(fighter, fightingEnemies), "None"
    if boonChoice != "None":
        boonTarget = BoonActions.npcSelectBoonTarget(fighter, reachable["boonReachable"], boonChoice)
        if boonTarget != "None": actionOptions += ["Boon"]

    attackChoice, attackTarget = "None", AttackActions.npcSelectAttackTarget(fighter, reachable["attackReachable"], False)
    if attackTarget != "None":
        attackChoice = AttackActions.npcSelectAttack(fighter, attackTarget)
        if attackChoice != "None": actionOptions += ["Attack"]
    
    hindranceTarget, hindranceChoice = "None", HindranceActions.npcSelectHindrance(fighter, reachable["hinderReachable"], fightingAllies)
    if hindranceChoice != "None":
        hindranceTarget = AttackActions.npcSelectAttackTarget(fighter, reachable["hinderReachable"], False)
        if hindranceTarget != "None": actionOptions += ["Hindrance"]

    if len(actionOptions) > 0:
        match random.choice(actionOptions):
            case "Attack": Attacks.commitDice(attackChoice, fighter, attackTarget)
            case "Boon": Boons.commitDice(fighter, boonTarget, boonChoice) # Add area options
            case "Hinder": Hinder.commitDice(fighter, hindranceTarget, hindranceChoice)
    else:
        if any(dice > 0 for dice in [fighter.atrb["cur_mar"], fighter.atrb["cur_mag"]]):
            Select.waitPrint(fighter.props["name"] + " foregoes action.")