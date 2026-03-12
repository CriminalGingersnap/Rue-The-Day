from Characters import Elementals
from . import Wild1_Pass as Pass, Wild2_Bay as Bay
import random

# The fjord cuts between the wilds and the Feywood. Players need to navigate around the water to reach that biome.
# Players can access the Feywood from the glacier.

def randomEncounters(roll, environment) -> list:
    members, element = [], "Ice"

    match roll:
        case 2: members = randomElementals("dancer", environment, element, False)
        case 3: members = randomElementals("hulk", environment, element, False)
        case 4: members = randomElementals("wisps", environment, element, False)
        case 5: members = Bay.randomBeasts("bear", environment, element)
        case 6: members = Bay.randomBeasts("moose", environment, element)
        case 7: members = Pass.randomBeasts("wasp", environment, "Toxin")
        case 8: members = Pass.randomBeasts("hound", environment, "Flame")
        case 9: members = Pass.randomBeasts("hound", environment, element)
        case 10: members = Pass.randomBeasts("urchin", environment, element)
        case 11: members = Pass.randomBeasts("deer", environment, element)
        case 12: members = Pass.randomBeasts("rabbit", environment, element)

    if (environment["Diamonds"] == "King"):
        members += [Elementals.wisp(element, "Random").ch]

    for i in len(members): members[i].name += "[" + str(i) + "]"

    return members

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
                elementalList += [Elementals.hulk(element, rankChoice).ch]
        case "wisp":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.wisp(element, rankChoice).ch]

    return elementalList


def getElementalRankOptions(majorBiome, environment):
    rankOptions = ["Lesser"]
    if majorBiome and (environment["Spades"] == "King"): rankOptions += ["Greater"]

    return rankOptions