from Characters import Elementals
from . import MetamorphosisBiomes as Metamorphosis, KingKillerBiomes as Kingdom, BenedictionBiomes as Benediction
from Systems import Roll, PlayerSelect as Select
import random


def setFoes(biome, budgets) -> list:
    Select.waitPrint("Rolling to determine encounter number.")
    Select.waitPrint("First roll:")
    roll1, roll2 = Roll.roll(None, 1, None, None), 0

    if biome not in ["Northern Stronghold", "Northern Road", "Southern Stronghold", "Southern Road"]:
        Select.waitPrint("Second roll:")
        roll2 = Roll.roll(None, 2, None, None)
    else: roll2 = roll1

    rolls = [roll1, roll2]
    rollNum, groups = 0, [[], []]
    
    for roll in rolls:
        budget = budgets[rollNum]
        members = []
        match biome:
            case "Wildlands Pass": members = Metamorphosis.passEncounters(roll, budget)
            case "Wildlands Bay": members = Metamorphosis.bayEncounters(roll, budget)
            case "Frozen Fjord": members = Metamorphosis.fjordEncounter(roll, budget)
            case "Frozen Glacier": members = Metamorphosis.glacierEncounters(roll, budget)
            case "Dreamwood Periphery": members = Metamorphosis.peripheryEncounters(roll, budget)
            case "Dreamwood Depths": members = Metamorphosis.depthsEncounters(roll, budget)
            case "Burning Peninsula": members = Metamorphosis.peninsulaEncounters(roll, budget)
            case "Burning Volcano": members = Metamorphosis.volcanoEncounters(roll, budget)

            case "Northern Stronghold": members = Kingdom.strongholdEncounters(roll, rollNum, budget)
            case "Northern Road": members = Kingdom.outlierEncounters(roll, rollNum, "Road", budget)
            case "Marshland": members = Kingdom.marshEncounters(roll, budget)
            case "Outlaw Camp": members = Kingdom.outlierEncounters(roll, rollNum, "Camp", budget)
            case "Unsettled": members = Kingdom.unsettledEncounters(roll, budget)

            case "Dream Sea-Cave": members = Benediction.seaCaveEncounters(roll, budget)
            case "Holy Scrubland": members = Benediction.scrublandEncounters(roll, budget)
            case "Holy Desert": members = Benediction.desertEncounters(roll, budget)
            case "Rot Encroachment": members = Benediction.encroachmentEncounter(roll, budget)
            case "Rot Locus": members = Benediction.locusEncounter(roll, budget)
            case "Shoreline": members = Benediction.shoreEncounters(roll, budget)

            # case "Southern Stronghold": members = Infestation.strongholdEncounters(roll, index)
            # case "Southern Road": members = Infestation.outlierEncounters(roll, index)
            
        memberIndex = 1
        for member in members:
            member.name += "[" + str(memberIndex) + "]"
            memberIndex += 1
        
        groups = members
        rollNum += 1

    return groups