from Characters import Elementals
from . import RandomCreatures as Creatures
import random


def elementals(type, element, majorBiome, diceBudget):
    elementalList, rankOptions = [], getElementalRankOptions(majorBiome)

    while diceBudget > 0:
        rankChoice, elemental = random.choice(rankOptions), None
        match type:
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
            case "spinx": elemental = Elementals.sphinx(element, rankChoice).ch

            case "wisp": elemental = Elementals.wisp(element, rankChoice).ch

            case "grotesquery": elemental = Elementals.grotesquery(element, rankChoice).ch

        diceBudget -= (elemental.atrb["base_mag"] + elemental.atrb["base_mar"])
        elementalList += [elemental]

    return elementalList

def getElementalRankOptions(majorBiome):
    rankOptions = ["Lesser"]
    if majorBiome: rankOptions += ["Greater"]
    return rankOptions