from Systems import PlayerSelect as Select
from . import AreaActions, AttackActions, BoonActions, HindranceActions
from Abilities import Area_Set as Area, AttackAbilities as Attacks, Boons_Set as Boons, Hindrances_Set as Hinder
import random


def npcAction(fighter, groups, battleMap) -> None:
    reachable, fightingAllies, fightingEnemies = groups["reachable"], groups["fightingAllies"], groups["fightingEnemies"]
    actionOptions = []

    areaChoice = AreaActions.npcSelectArea(fighter, fightingEnemies)
    if areaChoice != "None": actionOptions += ["Area"]

    attackChoice, attackTarget = "None", AttackActions.npcSelectAttackTarget(fighter, reachable["attackReachable"], False)
    if attackTarget != "None":
        attackChoice = AttackActions.npcSelectAttack(fighter, attackTarget)
        if attackChoice != "None": actionOptions += ["Attack", "Attack"]

    boonChoice, boonTarget = BoonActions.npcSelectBoon(fighter, fightingEnemies), "None"
    if boonChoice != "None":
        boonTarget = BoonActions.npcSelectBoonTarget(fighter, reachable["boonReachable"], boonChoice)
        if boonTarget != "None": actionOptions += ["Boon"]
    
    hindranceTarget, hindranceChoice = "None", HindranceActions.npcSelectHindrance(fighter, reachable["hinderReachable"], fightingAllies)
    if hindranceChoice != "None":
        hindranceTarget = AttackActions.npcSelectAttackTarget(fighter, reachable["hinderReachable"], False)
        if hindranceTarget != "None": actionOptions += ["Hindrance"]

    if len(actionOptions) > 0:
        match random.choice(actionOptions):
            case "Area":
                dice = Boons.blitzCommit(fighter, "cur_mag")
                Area.execute(fighter, dice, groups, areaChoice, battleMap)
            case "Attack": Attacks.commitDice(attackChoice, fighter, attackTarget)
            case "Boon": Boons.commitDice(fighter, boonTarget, boonChoice)
            case "Hinder": Hinder.commitDice(fighter, hindranceTarget, hindranceChoice)
    elif not fighter.cndt["blitzing"]:
        Select.waitPrint(fighter.props["name"] + " foregoes action.")