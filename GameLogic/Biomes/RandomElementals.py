from Characters import Elementals
from . import RandomCreatures as Creatures
import random


def elementals(elementalType, element, majorBiome, diceBudget):
    elementalList, firstElemental = [], True

    while diceBudget > 0:
        rankOptions = getElementalRankOptions(majorBiome, diceBudget, elementalType, firstElemental)
        rankChoice, elemental, elementalType = random.choice(rankOptions[0]), None, rankOptions[1]

        match elementalType:
            case "dancer": elemental = Elementals.dancer(element, rankChoice).ch
            case "hulk": elemental = Elementals.hulk(element, rankChoice).ch
            case "wraith": elemental = Elementals.wraith(element, rankChoice).ch

            case "hive": elemental = Elementals.hive(element, rankChoice).ch
            case "ooze": elemental = Elementals.ooze(element, rankChoice).ch
            case "puffer": elemental = Elementals.puffer(element, rankChoice).ch

            case "satyr": elemental = Elementals.satyr(element, rankChoice).ch
            case "ogre": elemental = Elementals.ogre(element, rankChoice).ch
            case "nymph": elemental = Elementals.nymph(element, rankChoice).ch

            case "bull": elemental = Elementals.bull(element, rankChoice).ch
            case "obelisk": elemental = Elementals.obelisk(element, rankChoice).ch
            case "sphinx": elemental = Elementals.sphinx(element, rankChoice).ch

            case "wisp": elemental = Elementals.wisp(element, rankChoice).ch

            case "grotesquery": elemental = Elementals.grotesquery(element, rankChoice).ch

        diceBudget -= (elemental.atrb["base_mag"] + elemental.atrb["base_mar"])
        elementalList += [elemental]

    return elementalList

def getElementalRankOptions(majorBiome, diceBudget, elementalType, firstElemental):
    rankOptions = []

    if diceBudget > 2: rankOptions += ["Lesser"]
    if (diceBudget > 4) and majorBiome: rankOptions += ["Greater"]

    if len(rankOptions) == 0:
        if firstElemental:
            firstElemental = False
            rankOptions += ["Lesser"]
        else: elementalType, rankOptions = "wisp", ["Lesser"]

    return [rankOptions, elementalType]