from Actions import Sort
from Abilities import Boons_Set as Boons, Hindrances_Set as Hinder, Area_Apply as Area
from Maps import Map
from . import Effects, PlayerSelect as Select


def checkReach(fighter, battleMap) -> None:
    for commitment in fighter.commitments:
        if len(fighter.commitments[commitment]["targets"]) > 0:
            targets = fighter.commitments[commitment]["targets"]
            
            Map.hideShrouded(fighter, targets, fighter.sightMap)
            reachable = Sort.sortReachable(fighter, targets, targets)
            
            if commitment in Boons.magicBoons + Boons.martialBoons:
                reachable = reachable["boonReachable"]
            elif commitment in Hinder.magicHindrance + Hinder.martialHindrance:
                reachable = reachable["hinderReachable"]

            for target in targets:
                if target not in reachable:
                    removeCommitment(fighter, target, commitment, battleMap)
                

def clearCommitments(fighter, battleMap):
    for commitment in fighter.commitments:
        if len(fighter.commitments[commitment]["targets"]) > 0:
            for target in fighter.commitments[commitment]["targets"]:
                removeCommitment(fighter, target, commitment, battleMap)


def removeCommitment(fighter, target, commitment, battleMap):
    # if commitment in ["Bless", "Hex", "Mark", "Ready"]:
    #     spaces = fighter.commitments[commitment]["additional"]
    #     for space in spaces:
    #         row = space[0], column = space[1]
    #         Area.setAtmosphere("_", row, column, battleMap)
    Select.waitPrint("Commitment " + commitment + " terminates on " + target.name + ".")
    Effects.removeEffect(target, commitment)
    
    fighter.commitments[commitment] = {"targets": [], "additional": None}