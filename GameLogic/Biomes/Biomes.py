from Characters import Elementals
from . import MetamorphosisBiomes as Metamorphosis, KingKillerBiomes as Kingdom, BenedictionBiomes as Benediction
from Systems import Roll, PlayerSelect as Select
import random


def setFoes(biome, faceCards) -> list:
    Select.waitPrint("Rolling to determine encounter number.")
    Select.waitPrint("First roll:")
    roll1, roll2 = Roll.roll(None, 1, None, None), 0

    if biome not in ["Northern Stronghold", "Northern Road", "Southern Stronghold", "Southern Road"]:
        Select.waitPrint("Second roll:")
        roll2 = Roll.roll(None, 2, None, None)
    else: roll2 = roll1

    rolls = [roll1, roll2]
    index, groups = 0, [[], []]
    
    for roll in rolls:
        members = []
        match biome:
            case "Wildlands Pass": members = Metamorphosis.passEncounters(roll, faceCards)
            case "Wildlands Bay": members = Metamorphosis.bayEncounters(roll, faceCards)
            case "Frozen Fjord": members = Metamorphosis.fjordEncounter(roll, faceCards)
            case "Frozen Glacier": members = Metamorphosis.glacierEncounters(roll, faceCards)
            case "Dreamwood Periphery": members = Metamorphosis.peripheryEncounters(roll, faceCards)
            case "Dreamwood Depths": members = Metamorphosis.depthsEncounters(roll, faceCards)
            case "Burning Peninsula": members = Metamorphosis.peninsulaEncounters(roll, faceCards)
            case "Burning Volcano": members = Metamorphosis.volcanoEncounters(roll, faceCards)

            # case "Northern Stronghold": members = Kingdom.strongholdEncounters(roll, faceCards, index)
            case "Northern Road": members = Kingdom.roadEncounters(roll, faceCards, index)
            case "Marshland": members = Kingdom.marshEncounters(roll, faceCards)
            # case "Outlaw Camp": members = Kingdom.outlawEncounters(roll, faceCards)
            case "Unsettled": members = Kingdom.unsettledEncounters(roll, faceCards)

            case "Dream Sea-Cave": members = Benediction.seaCaveEncounters(roll, faceCards)
            case "Holy Scrubland": members = Benediction.scrublandEncounters(roll, faceCards)
            case "Holy Desert": members = Benediction.desertEncounters(roll, faceCards)
            case "Rot Encroachment": members = Benediction.encroachmentEncounter(roll, faceCards)
            case "Rot Locus": members = Benediction.locusEncounter(roll, faceCards)
            case "Shoreline": members = Kingdom.shorelineEncounters(roll, faceCards)

            # case "Southern Stronghold": members = Infestation.strongholdEncounters(roll, faceCards, index)
            # case "Southern Road": members = Infestation.roadEncounters(roll, faceCards, index)

        for i in len(members): members[i].name += "[" + str(i) + "]"
        groups[index] = members
        index += 1

    return groups


def setBiome(worldMap):
    biome = ""

    worldMap.marker.position

    return biome