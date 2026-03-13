from Characters import Elementals
from . import MetamorphosisBiomes as Metamorphosis, KingKillerBiomes as Kingdom, BenedictionBiomes as Benediction
from Systems import Roll, PlayerSelect as Select
import random


def setFoes(biome, faceCards) -> list:
    Select.waitPrint("Rolling dice to determine encounter number.")
    Select.waitPrint("Group 1 roll:")
    roll1 = Roll.roll(None, 1, None, None)
    Select.waitPrint("Group 2 roll:")
    roll2 = Roll.roll(None, 2, None, None)

    rolls = [roll1, roll2]
    index, groups = 0, [[], []]
    
    for roll in rolls:
        members = []
        match biome:
            case "Pass": members = Metamorphosis.passEncounters(roll, faceCards)
            case "Bay": members = Metamorphosis.bayEncounters(roll, faceCards)
            case "Fjord": members = Metamorphosis.fjordEncounter(roll, faceCards)
            case "Glacier": members = Metamorphosis.glacierEncounters(roll, faceCards)
            # case "GhostWood": members = Metamorphosis.ghostWoodEncounters(roll, faceCards)
            case "Peninsula": members = Metamorphosis.peninsulaEncounters(roll, faceCards)
            case "Volcano": members = Metamorphosis.volcanoEncounters(roll, faceCards)

            # case "Kingdom": members = KingdomBiomes.kingdomEncounters(roll, faceCards)
            # case "Marsh": members = KingdomBiomes.marshEncounters(roll, faceCards)
            # case "Outlaw": members = KingdomBiomes.outlawEncounters(roll, faceCards)
            # case "Shoreline": members = KingdomBiomes.shorelineEncounters(roll, faceCards)
            # case "Unsettled": members = KingdomBiomes.hillEncounters(roll, faceCards)

            # case "SeaCave": members = Benediction.seaCaveEncounters(roll, faceCards)
            # case "DeadTown": members = Benediction.deadTownEncounters(roll, faceCards)
            # case "Scrubland": members = Benediction.scrublandEncounters(roll, faceCards)
            # case "Desert": members = Benediction.desertEncounters(roll, faceCards)
            # case "BurialValley": members = Benediction.valleyEncounters(roll, faceCards)

        match faceCards["Diamonds"]:
            case "King":
                if () and random.choice([False, False, True]):
                    members += [Elementals.wisp(faceCards, "Random").ch]
            case "Queen":
                if () and random.choice([False, False, False, False, False, True]):
                    members += [Elementals.wisp(faceCards, "Random").ch]

        for i in len(members): members[i].name += "[" + str(i) + "]"
        groups[index] = members
        index += 1

    return groups