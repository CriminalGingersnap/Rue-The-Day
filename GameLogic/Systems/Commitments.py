from Actions import Sort
from Abilities import Boons_Set as Boons, Hindrances_Set as Hinder
from Maps import Map_Update as uMap
from . import Effects, PlayerSelect as Select


def checkReach(fighter) -> None:
    for commitment in fighter.commitments:
        if len(fighter.commitments[commitment]["targets"]) > 0:
            targets = fighter.commitments[commitment]["targets"]
            
            uMap.hideShrouded(fighter, targets, fighter.sightMap)
            reachable = Sort.sortReachable(fighter, targets, targets)
            
            if commitment in Boons.magicBoons + Boons.martialBoons:
                reachable = reachable["boonReachable"]
            elif commitment in Hinder.magicHindrances + Hinder.martialHindrances:
                reachable = reachable["hinderReachable"]

            for target in targets:
                if target not in reachable:
                    removeCommitment(fighter, target, commitment)
                

def clearCommitments(fighter):
    for commitment in fighter.commitments:
        if len(fighter.commitments[commitment]["targets"]) > 0:
            for target in fighter.commitments[commitment]["targets"]:
                removeCommitment(fighter, target, commitment)


def removeCommitment(fighter, target, commitment):
    Select.waitPrint("Commitment " + commitment + " terminates on " + target.props["name"] + ".")
    Effects.removeEffect(target, commitment)
    
    fighter.commitments[commitment] = {"targets": [], "additional": None}