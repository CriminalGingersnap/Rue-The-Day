import Actions.AttackActions as AttackActions
from . import AttackAbilities as Attacks
from Systems import PlayerSelect as Select
from Characters import AggressiveBeasts, Insects
from Maps import Map_Populate as pMap, Movement
import random


def applyRiposte(principal, enemy, commitment) -> None:
    source = principal.effects[commitment]["source"]
    dice = principal.effects[commitment]["dice"]
    ability = principal.effects[commitment]["additional"]
    
    attackChoice, proceed = None, True
    distance = Movement.getTargetDistance(source, enemy)

    if (dice > 0) and (distance <= 2 <= source.equip["weapons"]["reach"]):
        if any(reaction in source.abl["reactions"] for reaction in ["Riposte", "Flare"]):
            expense = 0

            if source.props["rank"] == "player":
                match ability:
                    case "Bind" | "Guard": proceed = Select.yesNo("Trigger riposte?")
                    case "Wreath": proceed = Select.yesNo("Trigger flare?")

                if proceed:
                    attackChoice = AttackActions.pcSelectAttack(source)
                    Select.waitPrint("Expend dice (" + str(dice) + "):")
                    expense = Select.takeInput(1, dice)
            else:
                attackChoice = AttackActions.npcSelectAttack(source, enemy)
                expense = random.randint(1, dice)

            if proceed:
                Attacks.execute(source, enemy, attackChoice, expense)
                principal.effects[ability]["dice"] -= expense


def applyPheromones(fighter, allies):
    if (fighter.props["job"] == "Ant") and not fighter.cndt["calling"]["used"]:
        Select.waitPrint("The dead " + fighter.props["name"] + " releases pheromones!")
        socialRoll(fighter, allies)
        
def applyReinforcements(fighter, allies, battleMap):
    if fighter.cndt["calling"]["quantity"] > 0:
        delay, quantity = fighter.cndt["calling"]["delay"], fighter.cndt["calling"]["quantity"]

        if delay == 1:
            Select.waitPrint("Enemy reinforcements incoming!")
        elif delay == 0:
            Select.slowPrint(str(quantity) + " enemy reinforcements arrive!")

            if fighter.props["job"] == "Ant":
                for newMember in quantity:
                    ant = Insects.ant().ch
                    allies += [ant]
                    pMap.firstPlacement(battleMap, ant)
            elif fighter.props["job"] == "Hound":
                for newMember in quantity:
                    hound = AggressiveBeasts.hound(fighter.element).ch
                    allies += [hound]
                    pMap.firstPlacement(battleMap, hound)
            
            for ally in allies:
                fighter.cndt["calling"]["quantity"] = 0
                fighter.cndt["calling"]["used"] = True
        fighter.cndt["calling"]["delay"] -= 1

def applySocial(fighter, allies):
    if fighter.props["job"] == "Hound":
        if not any(ally.props["type"] == "human" for ally in allies):
            if fighter.cndt["social"] and not fighter.cndt["calling"]["used"]:
                Select.waitPrint(fighter.props["name"] + " howls to the rest of its pack!")
                socialRoll(fighter, allies)
               

def socialRoll(fighter, allies):
    Select.waitPrint("Rolling quantity (secret).")
    Select.waitPrint("Rolling delay (secret).")
    quantity, delay = random.randint(1, 6), random.randint(1, 6)

    if fighter.props["job"] == "Ant":
        Select.waitPrint("Both quantity and delay double for ants.")
        delay *= 2
        quantity *= 2

    for ally in allies:
        ally.cndt["calling"]["delay"] = delay
        ally.cndt["calling"]["quantity"] = quantity
        if ally.props["job"] == fighter.props["job"]: ally.cndt["calling"]["used"] = True