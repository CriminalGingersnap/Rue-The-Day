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
        case "wraith":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.wraith(element, rankChoice).ch]

        case "hive":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.hive(element, rankChoice).ch]
        case "ooze":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.ooze(element, rankChoice).ch]
        case "puffer":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.puffer(element, rankChoice).ch]

        case "satyr":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.satyr(element, rankChoice).ch]
        case "ogre":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.ogre(element, rankChoice).ch]
        case "nymph":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.nymph(element, rankChoice).ch]

        case "bull":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.bull(element, rankChoice).ch]
        case "obelisk":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.obelisk(element, rankChoice).ch]
        case "spinx":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.sphinx(element, rankChoice).ch]

        case "wisp":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.wisp(element, rankChoice).ch]

        case "grotesquery":
            for i in quantity:
                rankChoice = random.choice(rankOptions)
                elementalList += [Elementals.grotesquery(element, rankChoice).ch]

    return elementalList

def getElementalRankOptions(majorBiome, environment):
    rankOptions = ["Lesser"]
    if majorBiome and (environment["Spades"] == "King"): rankOptions += ["Greater"]

    return rankOptions