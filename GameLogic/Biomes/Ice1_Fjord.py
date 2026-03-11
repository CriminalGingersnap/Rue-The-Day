from Characters import Elementals
from . import Wild1_Pass as Pass, Wild2_Bay as Bay
import random

# The fjord cuts between the wilds and the Feywood. Players need to navigate around the water to reach that biome.
# Players can access the Feywood from the glacier.

def randomEncounters(encounterRoll, environment) -> list:
    encounterGroup, element = [], "Ice"

    match encounterRoll:
        case 2: encounterGroup = randomElementals("dancer", environment, element, False)
        case 3: encounterGroup = randomElementals("hulk", environment, element, False)
        case 4: encounterGroup = randomElementals("wisps", environment, element, False)
        case 5: encounterGroup = Bay.randomBeasts("bear", environment, element)
        case 6: encounterGroup = Bay.randomBeasts("moose", environment, element)
        case 7: encounterGroup = Pass.randomBeasts("wasp", environment, "Toxin")
        case 8: encounterGroup = Pass.randomBeasts("hound", environment, "Flame")
        case 9: encounterGroup = Pass.randomBeasts("hound", environment, element)
        case 10: encounterGroup = Pass.randomBeasts("urchin", environment, element)
        case 11: encounterGroup = Pass.randomBeasts("deer", environment, element)
        case 12: encounterGroup = Pass.randomBeasts("rabbit", environment, element)

    if (environment["Diamonds"] == "King"):
        encounterGroup += [Elementals.wisp(element, "Random").ch]

    for i in len(encounterGroup): encounterGroup[i].name += "[" + str(i) + "]"

    return encounterGroup

def randomElementals(type, environment, element, majorBiome):
    elementalList, rankOptions = [], getElementalRankOptions(majorBiome, environment)
    quantity = Pass.getQuantity(environment, rankOptions)

    match type:
        case "dancer":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.dancer(element, rankChoice).ch]
        case "hulk":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.dancer(element, rankChoice).ch]
        case "wisp":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.wisp(element, rankChoice).ch]

    return elementalList


def getElementalRankOptions(majorBiome, environment):
    rankOptions = ["Lesser"]
    if majorBiome and (environment["Spades"] == "King"): rankOptions += ["Greater"]

    return rankOptions