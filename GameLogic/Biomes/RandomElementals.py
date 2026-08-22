from Characters import Elementals
from . import RandomCreatures as Creatures
import random


def elementals(elementalType, element, majorBiome, diceBudget):
    elementalList, firstElemental = [], True

    while diceBudget > 0:
        rankOptions = getElementalRankOptions(majorBiome, diceBudget, elementalType, firstElemental)
        rankChoice, elemental, elementalType = random.choice(rankOptions[0]), None, rankOptions[1]

        match elementalType:
            case "dancer": elemental = Elementals.dancer(rankChoice, element).ch
            case "tripod": elemental = Elementals.tripod(rankChoice, element).ch
            case "wraith": elemental = Elementals.wraith(rankChoice, element).ch

            case "balloon": elemental = Elementals.balloon(rankChoice, element).ch
            case "hive": elemental = Elementals.hive(rankChoice, element).ch
            case "ooze": elemental = Elementals.ooze(rankChoice, element).ch

            case "satyr": elemental = Elementals.satyr(rankChoice, element).ch
            case "ogre": elemental = Elementals.ogre(rankChoice, element).ch
            case "nymph": elemental = Elementals.nymph(rankChoice, element).ch

            case "bull": elemental = Elementals.bull(rankChoice, element).ch
            case "obelisk": elemental = Elementals.obelisk(rankChoice, element).ch
            case "sphinx": elemental = Elementals.sphinx(rankChoice, element).ch

            case "wisp": elemental = Elementals.wisp(rankChoice, element).ch

            case "grotesquery": elemental = Elementals.grotesquery(rankChoice, element).ch
            case "shadow": elemental = Elementals.shadow(rankChoice, element).ch
            case "slime": elemental = Elementals.slime(rankChoice, element).ch

            case "mask": elemental = Elementals.mask(rankChoice, element).ch
            case "naga": elemental = Elementals.naga(rankChoice, element).ch
            case "rakshasa": elemental = Elementals.rakshasa(rankChoice, element).ch
            case "yogi": elemental = Elementals.yogi(rankChoice, element).ch

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