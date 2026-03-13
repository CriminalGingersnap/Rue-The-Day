from Characters import Elementals
from . import RandomCreatures as Creatures
import random


def elementals(type, environment, element, majorBiome):
    elementalList, rankOptions = [], getElementalRankOptions(majorBiome, environment)
    quantity = Creatures.getQuantity(environment, rankOptions)

    match type:
        case "dancer":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.dancer(element, rankChoice).ch]
        case "hulk":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.hulk(element, rankChoice).ch]
        case "obelisk":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.obelisk(element, rankChoice).ch]
        case "ooze":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.ooze(element, rankChoice).ch]
        case "puffer":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.puffer(element, rankChoice).ch]
        case "wisp":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.wisp(element, rankChoice).ch]       

    return elementalList

def getElementalRankOptions(majorBiome, environment):
    rankOptions = ["Lesser"]
    if majorBiome and (environment["Spades"] == "King"): rankOptions += ["Greater"]

    return rankOptions