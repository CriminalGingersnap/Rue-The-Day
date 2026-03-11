from Characters import AggressiveBeasts, AvoidantBeasts, Elementals, Invertebrates, Insects, Reptiles
from . import Wild1_Pass as Pass
import random

# Deep wild lowlands between the mountains and the fjord. Coniferous trees. Pervasive light mist.

def randomEncounters(encounterRoll, environment) -> list:
    encounterGroup, element = [], "Basic"

    match encounterRoll:
        case 2: encounterGroup = Pass.randomSoldiers("elite", environment)
        case 3: encounterGroup = randomBeasts("bear", environment, element)
        case 4: encounterGroup = randomBeasts("wyrm", environment, "Toxin")
        case 5: encounterGroup = randomBeasts("moose", environment, element)
        case 6: encounterGroup = Pass.randomBeasts("lizard", environment, "Basic")
        case 7: encounterGroup = Pass.randomBeasts("wasp", environment, "Toxin")
        case 8: encounterGroup = Pass.randomBeasts("beetle", environment, "Basic")
        case 9: encounterGroup = Pass.randomBeasts("isopod", environment, "Basic")
        case 10: encounterGroup = Pass.randomBeasts("urchin", environment, "Basic")
        case 11: encounterGroup = Pass.randomBeasts("deer", environment, "Basic")
        case 12: encounterGroup = Pass.randomBeasts("rabbit", environment, "Basic")

    if (environment["Diamonds"] == "King") and (encounterRoll != 2):
        encounterGroup += [Elementals.wisp("Random", "Random").ch]

    for i in len(encounterGroup): encounterGroup[i].name += "[" + str(i) + "]"

    return encounterGroup


def randomBeasts(type, environment, element) -> list:
    beastList, rankOptions = [], Pass.getAnimalRankOptions(environment)
    quantity = Pass.getQuantity(environment, rankOptions)

    match type:
        case "bear":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.bear(element, rankChoice).ch]
        case "moose":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                beastList += [AggressiveBeasts.moose(element, rankChoice).ch]
        case "wyrm":
            for i in quantity: 
                rankChoice = random.choice(rankOptions)
                beastList += [Reptiles.wyrm(element, rankChoice)]

    return beastList