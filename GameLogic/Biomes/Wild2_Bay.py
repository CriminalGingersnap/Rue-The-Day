from Characters import AggressiveBeasts, AvoidantBeasts, Elementals, Invertebrates, Insects, Reptiles
from . import Wild1_Pass as Pass
import random

# Deep wild lowlands between the mountains and the fjord. Coniferous trees. Pervasive light mist.

def randomEncounters(encounterRoll, environment):
    encounterGroup, element = [], "Basic"

    match encounterRoll:
        case 2: encounterGroup = Pass.randomSoldiers("elite", environment)
        case 3: encounterGroup = randomBeasts("bear", environment, element)
        case 4: encounterGroup = randomBeasts("wyrm", environment, "Toxin")
        case 5: encounterGroup = randomBeasts("moose", environment, element)
        case 6: encounterGroup = randomBeasts("lizard", environment, element)
        case 7: encounterGroup = Pass.randomBeasts("wasp", environment)
        case 8: encounterGroup = Pass.randomBeasts("beetle", environment)
        case 9: encounterGroup = Pass.randomBeasts("isopod", environment)
        case 10: encounterGroup = Pass.randomBeasts("urchin", environment)
        case 11: encounterGroup = Pass.randomBeasts("deer", environment)
        case 12: encounterGroup = Pass.randomBeasts("rabbit", environment)

    if (environment["Diamonds"] == "King") and (encounterRoll != 2):
        encounterGroup += [Elementals.wisp().ch]

    for i in len(encounterGroup): encounterGroup[i].name += "[" + str(i) + "]"

    return encounterGroup


def randomBeasts(type, environment, element) -> list:
    quantity *= 2
    beastList, rankOptions = [], Pass.getAnimalRankOptions(environment)

    match type:
        case "bear":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.bear(element, rankChoice).ch]
        case "moose":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.moose(element, rankChoice).ch]
        case "lizard":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.lizard(element, rankChoice).ch]
        case "wyrm":
            for i in quantity: 
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.wyrm(element, rankChoice)]

    return beastList