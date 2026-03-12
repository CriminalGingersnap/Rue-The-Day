from Characters import AggressiveBeasts, AvoidantBeasts, Elementals, Invertebrates, Insects, Reptiles
from . import Wild1_Pass as Pass
import random

# Deep wild lowlands between the mountains and the fjord. Coniferous trees. Pervasive light mist.

def randomEncounters(roll, environment) -> list:
    members, element = [], "Basic"

    match roll:
        case 2: members = Pass.randomSoldiers("elite", environment)
        case 3: members = randomBeasts("bear", environment, element)
        case 4: members = randomBeasts("moose", environment, element)
        case 5: members = randomBeasts("wyrm", environment, "Toxin")
        case 6: members = Pass.randomBeasts("lizard", environment, "Basic")
        case 7: members = Pass.randomBeasts("wasp", environment, "Toxin")
        case 8: members = Pass.randomBeasts("beetle", environment, "Basic")
        case 9: members = Pass.randomBeasts("isopod", environment, "Basic")
        case 10: members = Pass.randomBeasts("urchin", environment, "Basic")
        case 11: members = Pass.randomBeasts("deer", environment, "Basic")
        case 12: members = Pass.randomBeasts("rabbit", environment, "Basic")

    if (environment["Diamonds"] == "King") and (roll != 2):
        members += [Elementals.wisp("Random", "Random").ch]

    for i in len(members): members[i].name += "[" + str(i) + "]"

    return members


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