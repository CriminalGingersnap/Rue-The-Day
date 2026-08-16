from Abilities import Boons_Set as Boons, Hindrances_Set as Hinder
from Maps import Map_Update as uMap
from . import Effects, PlayerSelect as Select, Sort


def checkReach(fighter) -> None:
    for commitment in fighter.commits:
        if len(fighter.commits[commitment]["targets"]) > 0:
            targets = fighter.commits[commitment]["targets"]
            
            uMap.hideVeiled(fighter, targets, fighter.sightMap)
            reachable = Sort.sortReachable(fighter, targets, targets)
            
            if commitment in Boons.magicBoons + Boons.martialBoons:
                reachable = reachable["boonReachable"]
            elif commitment in Hinder.magicHindrances + Hinder.martialHindrances:
                reachable = reachable["hinderReachable"]

            for target in targets:
                if target not in reachable:
                    Select.waitPrint("\n" + target.props["name"] + " is out of reach.")
                    removeCommitment(fighter, target, commitment)
                

def clearCommitments(fighter):
    for commitment in fighter.commits:
        if len(fighter.commits[commitment]["targets"]) > 0:
            for target in fighter.commits[commitment]["targets"]:
                if target.effects[commitment]["source"] == fighter:
                    removeCommitment(fighter, target, commitment)


def removeCommitment(fighter, target, commitment):
    if (fighter != target) and (commitment not in ["Drain", "Fortify", "Heal", "Rally"]):
        Select.waitPrint("Commitment " + commitment + " terminated by " + fighter.props["name"] + ".")
    else: print()
    
    Effects.removeEffect(target, commitment)
    fighter.commits[commitment] = {"targets": [], "additional": None}